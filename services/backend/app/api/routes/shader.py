from fastapi import APIRouter, Depends, status, HTTPException

router = APIRouter(prefix="/shader", tags=["shader"])
