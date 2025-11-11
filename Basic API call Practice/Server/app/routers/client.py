from fastapi import APIRouter ,Request,Response


router =  APIRouter(
            prefix="/client",
            tags=["Clients"]
            )   


@router.get('/')
def post_data():
    return {"response ": "Hello, from post team"}


@router.post("/user-data")
def set_user_data(response: Request):
    # print(response.query_params )
    # response.headers["This is my header"] ="vanakkam"
    return{"status": 200,"message":"Thank you from server" ,"IP ":response.client.host}
