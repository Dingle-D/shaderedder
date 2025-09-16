from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse

from app.db.services.shaders import add_shader, get_shader_by_id, get_shader_file_by_shader_id, delete_shader

from app.core.config import settings
from app.api.utils import CurrentUser

from app.models import ShaderDescription, ShaderFileDescription, Message

from typing import List
from pathlib import Path 
import shutil
import uuid
import os

UPLOAD_DIR = settings.STORAGE

def _get_absolute_path(filename: str) -> str:
    pth = Path.cwd() / UPLOAD_DIR
    file_path = pth / filename
    if not pth.exists():
        raise RuntimeError("Uploads path does not exists")
    return str(file_path)

def _generate_random_name(user_id, extension):
    import uuid, base64 
    u = uuid.uuid4()
    short_name = base64.urlsafe_b64encode(u.bytes).rstrip(b"=").decode('utf-8')
    return f"{user_id}_{short_name}.{extension}"

router = APIRouter(prefix="/shader", tags=["shader"])

@router.post("/upload")
async def upload_shader(
    current_user: CurrentUser,
    file: UploadFile = File(...),
    title: str = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    uniforms: str = Form(...)
):
    sdesc, sfdesc = None, None 

    try:
        print(f"Title: {title}, desc: {description}, author id: {current_user.id}")
        sdesc = ShaderDescription(
            title=title,
            description=description,
            author_id=current_user.id
        )
        sfdesc = ShaderFileDescription(
            type=type,
            source=_generate_random_name(current_user.id, type),
            uniforms=uniforms
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect data format")

    filename = sfdesc.source

    file_path = _get_absolute_path(filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await add_shader(sdesc, sfdesc)
    return Message(success=True)

@router.post("/update")
async def udate_shader(
    current_user: CurrentUser,
    file: UploadFile = File(...),
    shader_id: int = Form(...),
    uniforms: str = Form
):
    shader = await get_shader_by_id(shader_id)
    if not shader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shader not found")
    if current_user.id != shader.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Has no access to that shader")
    shader_file = await get_shader_file_by_shader_id(shader_id)
    if not shader_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shader not found")

    file_path = shader_file.file
    # TODO: should change uniforms on save
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return Message(success=True)

@router.post("/delete")
async def delete_shader(
    current_user: CurrentUser,
    shader_id: int = Form(...),
):
    shader = await get_shader_by_id(shader_id)
    if not shader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shader not found")
    if current_user.id != shader.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Has no access to that shader")
    await delete_shader(shader)
    return Message(success=True)

@router.get("/download/{id}")
async def download_shader(id: int):
    shader = await get_shader_by_id(id)
    if not shader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shader not found")
    shader_file = await get_shader_file_by_shader_id(id)
    if not shader_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shader not found")
    response = FileResponse(
        path=shader_file.file,
        media_type="application/octet-stream",
        headers={
            "X-Uniforms": shader_file.uniforms
        }
    )
    return response

@router.get("/meta/{id}")
async def download_shader(id: int):
    shader = await get_shader_by_id(id)
    if not shader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shader not found")
    shader_file = await get_shader_file_by_shader_id(id)
    if not shader_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shader not found")

    response = JSONResponse(content={"Uniforms": shader_file.uniforms}, headers={"X-Uniforms": shader_file.uniforms})
    return response
