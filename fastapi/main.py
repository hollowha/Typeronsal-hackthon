

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],  # 或 ["*"] 開發時允許全部來源
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# main.py
from fastapi import Depends, HTTPException
from db.mongo import get_db
from ai_router import router as ai_router  # 👈 新增這行
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../typersonal')))

# 添加SLM NPU路由
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../slm_npu')))
from slm_router import router as slm_router

app.include_router(ai_router)  # 👈 掛載路由
app.include_router(slm_router)  # 👈 掛載SLM路由
@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB Atlas ✅"}

@app.get("/users")
async def list_users(db=Depends(get_db)):
    raw_users = await db["users"].find().to_list(100)
    users = []
    for user in raw_users:
        user["_id"] = str(user["_id"])  # ✅ 把 ObjectId 轉成字串
        users.append(user)
    return users

@app.post("/users")
async def create_user(user: dict, db=Depends(get_db)):
    try:
        result = await db["users"].insert_one(user)
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ 插入資料失敗: {str(e)}")
