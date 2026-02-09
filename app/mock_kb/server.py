from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class SearchReq(BaseModel):
    query: str
    top_k: int = 3


@app.post("/search")
def search(req: SearchReq):
    return [
        {"content": f"【知识1】{req.query} 的定义"},
        {"content": f"【知识2】{req.query} 的应用"},
        {"content": f"【知识3】{req.query} 的注意事项"},
    ]
