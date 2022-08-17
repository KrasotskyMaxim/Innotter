from fastapi import FastAPI
from fastapi import FastAPI

from models import Page
import utils


app = FastAPI() 


@app.post("/create_page")
async def new_page(page: Page):
    data = utils.create_new_page(page=page)
    
    return data  


@app.put("/update_page")
async def update_page(page_name: str, user_id: str, page_id: str):
    data = utils.update_page(page_name=page_name, page_id=page_id, user_id=user_id)

    return data 
    

@app.delete("/delete_page")
async def delete_page(user_id: str, page_id: str):
    data = utils.delete_page(user_id=user_id, page_id=page_id)
    
    return data 


@app.get("/pages", response_model=list[Page])
async def get_pages(user_id: str):
    data = utils.get_pages(user_id=user_id)
    
    return data 
    

@app.put("/pages/{page_id}/new_like/", response_model=Page)
async def new_like(page_id: str):
    data = utils.new_like(page_id=page_id)
    
    return data 


@app.put("/pages/{page_id}/new_follower/", response_model=Page)
async def new_follower(page_id: str):
    data = utils.new_follower(page_id=page_id)
    
    return data     


@app.put("/pages/{page_id}/new_follow_request/", response_model=Page)
async def new_follow_request(page_id: str):
    data = utils.new_follow_request(page_id=page_id)
    
    return data 


@app.put("/pages/{page_id}/undo_like/", response_model=Page)
async def undo_like(page_id: str):
    data = utils.undo_like(page_id=page_id)
    
    return data


@app.put("/pages/{page_id}/undo_follower/", response_model=Page)
async def undo_follower(page_id: str):
    data = utils.undo_follower(page_id=page_id)

    return data 


@app.put("/pages/{page_id}/undo_follow_request/", response_model=Page)
async def undo_follow_request(page_id: str):
    data = utils.undo_follow_request(page_id=page_id)
    
    return data 
