import logging

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile,  status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import FileResponse, StreamingResponse

from . import crud, crud_file, models, schemas
from .crud_file import read_pdf_as_base64
from .database import engine, get_db
from .auth.security import get_current_user
from app.auth import auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
    user (schemas.UserCreate): The new user.

    Returns:
    schemas.User: The created user.

    Raises:
    HTTPException: 400 Bad Request if the username already exists.
    """
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户已存在")
    return crud.create_user(db=db, user=user, is_admin=user.is_admin)

@app.get("/users/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    """
    Get all users.

    Returns:
    List[schemas.User]: A list of all users.
    """
    return db.query(models.User).all()

@app.delete("/delete_user/")
def del_user(
    user_info: schemas.UserDelete,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
    ):
    return crud.delete_user(db=db, user_id=user_info.id, is_admin=current_user.is_admin)
    

@app.post("/upload/", response_model=schemas.File)
def upload_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(get_current_user)  # 获取当前用户
):
    """
    Upload a PDF file.

    Args:
    file (UploadFile): The file to be uploaded.

    Returns:
    schemas.File: The uploaded file.

    Raises:
    HTTPException: 400 Bad Request if the file is not a PDF.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只能上传pdf文件")
    return crud_file.upload_file(db=db, file=file, uploader_id=current_user.id, is_admin=current_user.is_admin)

@app.delete("/delete_file/")
def delele_file(file_info: schemas.FileDelete, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    return crud_file.delete_file(db=db, file_id=file_info.id, is_admin=current_user.is_admin)

@app.get("/files/", response_model=List[schemas.File])
def list_files(db: Session = Depends(get_db)):
    return crud_file.get_files(db=db)


@app.post("/token", response_model=schemas.Token, )
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in a user.

    Args:
    form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
    db (Session): The database session.

    Returns:
    dict: A dictionary containing the access token and token type.

    Raises:
    HTTPException: 401 Unauthorized if the username or password is invalid.
    """
    # logging.info(form_data)
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户名或密码",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/create-admin/", response_model=schemas.User)
def create_admin(request: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户已存在")
    return crud.create_user(db, request, is_admin=1)


@app.get("/files/{filename}")
def get_file(filename: str):
    file_path = f"./files/{filename}"
    headers = {"Content-Disposition": "inline"}
    return FileResponse(file_path, media_type='application/pdf', headers=headers)


@app.get("/get_pdf_base64/")
def get_pdf_base64(file_name: str):
    try:
        # 假设 PDF 文件存放在 "uploaded_files" 目录下
        file_path = f"./files/{file_name}"
        base64_pdf = read_pdf_as_base64(file_path)
        return {"base64_pdf": base64_pdf}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


