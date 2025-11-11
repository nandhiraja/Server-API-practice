from fastapi import APIRouter


router =  APIRouter(
            prefix="/internal",
            tags=["Internal_clients"]
            )   


@router.get('/')
def home():
    return {"response ": "Hello, from internal team"}