# ========================= IMPORT SECTION ===============================================

from fastapi  import  FastAPI,File ,UploadFile ,Depends,HTTPException ,status ,Header ,Query,Path ,Request
import uvicorn
# import fastapi.requests import  Query
from fastapi.responses import FileResponse
from routers import client,internal_client
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
# ======================== INITILIZE SECTION ===============================================


app =  FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_orgins=["*"],
    allow_methods=["*"]
)
app.include_router(client.router)
app.include_router(internal_client.router)

# ========================= SERVER SECTION =================================================

def auth(head : str = Header()):
    print(head)


def user_valid( id:int,name:str):
    print("Validation id : ",name )
    if(id==1):
        return True
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Sorry does not have access")

@app.get('/',tags=["Root"])
def home():

    return "This is first response"


@app.post('/documents')
def handle_documents(file: UploadFile =File(...) ):
    if  file:
        file_name = f'uploads/{file.filename}'
        with open (file_name,'wb') as content:
            content.write(file.file.read())
            
    return {"message ": file.filename}






@app.get("/user/{name}/{id}" ,dependencies=[Depends(auth)])
def get_user(name:str,
             id:int,
             request: Request,
             check =Depends(user_valid)
             ):
      
      print(request.headers)
  
      return {"message": f"hello {name}" ,"check":check}
  









@app.get('/query')
def get_query(value:str = "dummy"):
    return {"passed value ": value}

@app.get("/items", tags=["Query Params"])
async def get_items(limit: int = 10, sort: Optional[str] = None):
    """
    Get a list of items, with optional sorting and limiting.
    Try:
    - /items
    - /items?limit=50
    - /items?sort=desc
    - /items?limit=25&sort=asc
    """
    if sort:
        return {"message": f"Showing {limit} items, sorted {sort}"}
    
    return {"message": f"Showing {limit} items, unsorted"}


# ========================= Application Run section ========================================



if __name__ =="__mani__":

    pass