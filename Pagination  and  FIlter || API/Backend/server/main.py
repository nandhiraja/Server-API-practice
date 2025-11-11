from fastapi import FastAPI,Request,Response
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from Router import v1

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"])
app.include_router(v1.router)


# ================================== End points =========================================================

@app.get('/')
def home():
    return{"message" :"Hai welcome"}




# if __name__ =="___main__":
    # uvicorn.run(app="main")