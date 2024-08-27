import base64
import os
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
