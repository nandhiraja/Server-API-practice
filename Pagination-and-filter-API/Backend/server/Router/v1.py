from fastapi  import  APIRouter
from service import page_data
import json
router = APIRouter(
             prefix='/api',
             tags=["v1"]
             )

@router.get("/")
def home():
    return {"message":"Welcome to  Recipe page"}

@router.get("/recipes")
def get_recipes(page:int ,limit:int):
    return { "total_count": 1000,"data ":page_data.get_recipes(page=page,limit=limit)}


@router.get("/search")
def get_recipes(calories:str = None ,title:str= None ,cuisine:str= None  ,total_time:str = None ,rating:str= None ):
    params = {"title":title,"cuisine":cuisine,"total_time":total_time,"rating":rating}
    new_params ={}
   
    for key in params.keys():
        print(key)
        if params[key] ==None:
            continue
        new_params[key] =params[key]            

   
    if "total_time" in new_params:
       new_params["total_time"] = total_time.split("=")
    if "rating" in new_params:
        new_params["rating"] = rating.split("=")

    print(new_params)
    db_data = page_data.search_data(new_params)

    if(calories == None):
        return {"response" : db_data}
    
    final_data={}
    calories_parse = calories.split("=")
    symbol =calories_parse[0]
    check_value = int(calories_parse[1])
    
    index =0
    for value in db_data:
        
        if("calories" in db_data[value]["nutrients"]):
            calories_value = int(db_data[value]["nutrients"]["calories"].split()[0])
            if(symbol == '' and calories_value == check_value):
                final_data[index] =db_data[value]
            if(symbol == '>' and calories_value > check_value):
                final_data[index] =db_data[value]
            if(symbol == '<' and calories_value < check_value):
                final_data[index] =db_data[value]
            print(value)
            index+=1




    return {"total_count": 1000,"data ":final_data}
