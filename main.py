from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 導入 CORS 中間件
from pydantic import BaseModel
from typing import List, Optional
from api.endpoints import videos, products, brands, categories, influencers  # 導入視頻和商品路由

app = FastAPI(
    title="視頻分析系統",
    description="用於分析視頻和商品數據的REST API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Videos",
            "description": "視頻相關的操作",
        },
        {
            "name": "Products",
            "description": "商品相關的操作",
        },
        {
            "name": "Brands",
            "description": "品牌相關的操作",
        },
        {
            "name": "Categories",
            "description": "分類相關的操作",
        }
    ]
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，生產環境建議設置具體的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 headers
)

# 註冊路由
app.include_router(videos.router)
app.include_router(products.router)
app.include_router(brands.router)
app.include_router(categories.router)
app.include_router(influencers.router)

# class Category(Enum):
#     TOOLS = "tools"
#     CONSUMABLES = "consumables"

# class Item(BaseModel):
#     name: str
#     price: float
#     count: int
#     id: int
#     category: Category

# items = {
#     0: Item(name="Hammer", price=6.9, count = 20 ,id = 0, category=Category.TOOLS),
#     1: Item(name="Plier", price=22.9, count = 20 , id = 1, category=Category.TOOLS),
#     2: Item(name="Nails", price=1.99, count = 100 , id = 2, category=Category.CONSUMABLES)
# }

# @app.get("/", tags=["General"])
# def index() -> dict[str, dict[int, Item]]:
#     return {"items":items}

# @app.get(
#     "/items/{item_id}",
#     tags=["Items"],
#     summary="獲取特定商品",
#     description="通過商品ID獲取特定商品的詳細信息"
# )
# def query_item_by_id(item_id : int) -> Item:
#     if item_id not in items:
#         raise HTTPException(
#           status_code=404, detail = f"Can't find item_id = {item_id} in items!"
#         ) 
#     else:
#         return items[item_id]

# # 定义返回的模型
# class QueryResponse(BaseModel):
#     query: dict[str, Optional[str | float | int | Category]]
#     selection: List[Item]

# # 定义 Selection 类型
# Selection = dict[str, str | int | float | Category | None]

# @app.get("/items/", response_model=QueryResponse, tags=["Items"])
# def query_item_by_parameters(
#     name : str | None = None, 
#     price : float | None = None,
#     count : int | None = None,
#     category : Category | None = None,
# ) -> dict[str, Selection | list[Item]]:
#     def check_item(item : Item) -> bool:
#         return all(
#             (
#                 name is None or item.name == name,
#                 price is None or item.price == price,
#                 count is None or item.count == count,
#                 category is None or item.category is category,
#             )
#         )
#     selection = [item for item in items.values() if check_item(item)]        
#     return {
#         "query" : {"name" : name, "price" : price, "count" : count, "category" : category}, 
#         "selection" : selection,
#     }

# @app.post('/', tags=["Items"])
# def add_item(item:Item) -> dict[str, Item]:

#     if item.id in items:
#         raise HTTPException(status_code=400, detail=f"Item with id = {item.id} already exists.")
#     print (item.id)        
#     print (item)
#     items[item.id] = item
#     return {"added": item}

# @app.put("/items/{item_id}", tags=["Items"])
# def update(
#     item_id : int, 
#     name : str | None = None, 
#     price : float | None = None,
#     count : int | None = None
# ) -> dict[str, Item]:
    
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item with id = {item.id} not exists.")
#     if all(info is None for info in (name, price, count)):
#         raise HTTPException(
#             status_code=400, detail="No parameters provided for update."
#         )
#     item = items[item_id]
#     if name is not None:
#         item.name = name
#     if price is not None:
#         item.price = price
#     if count is not None:
#         item.count = count

#     return {"update" : item}

# @app.delete('/items/{item_id}', tags=["Items"])
# def delete_item(item_id: int) -> dict[str, Item]:
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail=f"Item with id = {item.id} not exists.")

#     item = items.pop(item_id)
#     return {"deleted": item}

