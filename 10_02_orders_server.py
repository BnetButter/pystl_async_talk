from fastapi import FastAPI
from fastapi import Request
import uvicorn


orders_list = []

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return "OK"

@app.api_route("/api/orders", methods=["POST", "GET"])
async def orders(request: Request):
    if request.method == "GET":
        return orders_list
    elif request.method == "POST":
        orders_list.append(await request.json())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

