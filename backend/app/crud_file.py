import base64
import os
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import UploadFile
from io import BytesIO
from app import models
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter


def create_watermark(watermark_text):
    # 创建一个字节流来保存PDF文件
    packet = BytesIO()

    # 创建一个PDF对象并写入水印文本
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 40)
    can.setFillColorRGB(200, 200, 200)  # 浅灰色
    can.saveState()
    can.translate(500, 300)
    can.rotate(45)  # 旋转水印
    can.drawCentredString(0, 0, watermark_text)
    can.restoreState()
    can.save()

    # 移动到字节流的开头
    packet.seek(0)

    return packet

def add_watermark(pdf_file, watermark_text):
    # 将 UploadFile 对象转换为字节流
    file_bytes = pdf_file.file.read()
    pdf_stream = BytesIO(file_bytes)

    reader = PdfReader(pdf_stream)
    writer = PdfWriter()

    # 创建水印PDF
    watermark_pdf = create_watermark(watermark_text)
    watermark_reader = PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    # 对每一页添加水印
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    # 将最终的PDF写入字节流
    output_stream = BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    return output_stream  # 返回修改后的 PDF 数据流


def upload_file(db: Session, file: UploadFile, file_tag: str, uploader_id: int, is_admin: int):
    if is_admin == 1:
        # 生成带水印的PDF数据流
        watermarked_pdf_stream = add_watermark(file, "慧至半径")

        # 保存PDF到指定目录
        save_directory = "./files"
        os.makedirs(save_directory, exist_ok=True)
        file_path = os.path.join(save_directory, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(watermarked_pdf_stream.read())

        # 保存文件信息到数据库
        db_file = models.File(filename=file.filename, file_tag = file_tag, uploader_id=uploader_id)
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file
    else:
        return {"message": "没有权限，文件上传失败"}


def delete_file(db: Session, file_id: int, is_admin: int):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if file and is_admin == 1:
        db.delete(file)
        db.commit()
        return {"message": "文件删除成功"}
    return {"message": "没有权限，文件删除失败"}


def get_files(db: Session, file_tag = None):
    if file_tag is not None:
        return db.query(models.File).filter(models.File.file_tag == file_tag).all()
    return db.query(models.File).all()

def get_all_file_tags(db: Session):
    tags = db.query(models.File.file_tag).distinct().all()
    tags = [tag[0] for tag in tags]
    return tags


def read_pdf_as_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
        return encoded_string.decode('utf-8')
    
def edit_file(db: Session, file_id: int, filename: str, file_tag: str, is_admin: int):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if file is None:
        return {"message": "文件不存在"}
    if is_admin != 1:
        return {"message": "没有权限，文件修改失败"}
    if file_tag is None:
        return {"message": "文件标签不能为空"}
    if change_file_name(file.filename, filename):
        file.file_tag = file_tag
        file.filename = filename
        db.commit()
        db.refresh(file)
        return file
    else:
        return {"message": "文件修改失败"}


def change_file_name(old_filename, new_filename):
    # specify the directory path and the old file name
    dir_path = './files'

    # construct the full file paths
    old_file_path = os.path.join(dir_path, old_filename)
    new_file_path = os.path.join(dir_path, new_filename)
    print(old_file_path, new_file_path)
    # check if the old file exists
    if os.path.exists(old_file_path):
        # rename the file
        os.rename(old_file_path, new_file_path)
        return True
    else:
        return False


def get_file_tag(db: Session, tag_id: int):
    return db.query(models.FileTag).filter(models.FileTag.id == tag_id).first()

def get_file_tags(db: Session):
    return db.query(models.FileTag).order_by(models.FileTag.sort_order).all()

def create_file_tag(db: Session, file_tag: str, is_admin: int):
    if is_admin != 1:
        return {"message": "没有权限，标签创建失败"}
    
    if file_tag.sort_order is None:
        # 如果没有提供 sort_order，则将其设为最大 sort_order + 1
        max_sort_order = db.query(func.max(models.FileTag.sort_order)).scalar()
        file_tag.sort_order = (max_sort_order + 1) if max_sort_order is not None else 0
    else:
        # 如果提供了 sort_order，则将该位置后的所有标签的 sort_order + 1
        db.query(models.FileTag).filter(
            models.FileTag.sort_order >= file_tag.sort_order
        ).update({models.FileTag.sort_order: models.FileTag.sort_order + 1})
    
    db_file_tag = models.FileTag(tag_name=file_tag.tag_name, sort_order=file_tag.sort_order)
    db.add(db_file_tag)
    db.commit()
    db.refresh(db_file_tag)
    return db_file_tag


def delete_file_tag_by_id(db: Session, tag_id: int, is_admin: int):
    tag = db.query(models.FileTag).filter(models.FileTag.id == tag_id).first()
    if tag and is_admin == 1:
        db.delete(tag)
        db.commit()

        # 删除后，重新排序
        remaining_tags = db.query(models.FileTag).order_by(models.FileTag.sort_order).all()
        for index, remaining_tag in enumerate(remaining_tags):
            remaining_tag.sort_order = index
        db.commit()
        
        return {"message": "标签删除成功"}
    return {"message": "没有权限，标签删除失败"}

def edit_file_tag(db: Session, file_tag_info: dict, is_admin: int):
    if is_admin != 1:
        return {"message": "没有权限，标签修改失败"}
    
    tag = db.query(models.FileTag).filter(models.FileTag.id == file_tag_info.id).first()
    if not tag:
        return {"message": "标签不存在"}

    # 更新 tag_name
    if file_tag_info.new_tag_name:
        tag.tag_name = file_tag_info.new_tag_name
    
    # 更新 sort_order
    if file_tag_info.new_sort_order is not None and file_tag_info.new_sort_order != tag.sort_order:
        # max_sort_order = db.query(func.max(models.FileTag.sort_order)).scalar()

        if file_tag_info.new_sort_order > tag.sort_order:
            # 将 sort_order 在 (tag.sort_order, new_sort_order] 范围内的标签的 sort_order - 1
            db.query(models.FileTag).filter(
                models.FileTag.sort_order > tag.sort_order,
                models.FileTag.sort_order <= file_tag_info.new_sort_order
            ).update({models.FileTag.sort_order: models.FileTag.sort_order - 1})
        else:
            # 将 sort_order 在 [new_sort_order, tag.sort_order) 范围内的标签的 sort_order + 1
            db.query(models.FileTag).filter(
                models.FileTag.sort_order >= file_tag_info.new_sort_order,
                models.FileTag.sort_order < tag.sort_order
            ).update({models.FileTag.sort_order: models.FileTag.sort_order + 1})
        
        # 更新当前标签的 sort_order
        tag.sort_order = file_tag_info.new_sort_order

        # 处理所有大于 new_sort_order 的标签
        db.query(models.FileTag).filter(
            models.FileTag.sort_order > max(file_tag_info.new_sort_order, tag.sort_order)
        ).update({models.FileTag.sort_order: models.FileTag.sort_order})

    db.commit()
    db.refresh(tag)
    return tag

