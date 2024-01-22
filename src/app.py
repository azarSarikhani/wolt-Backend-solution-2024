import os
import uvicorn
from tools.deliveryFeeCalculator import calculate_fee
from tools.loadDb import load_db

from schemas.InitialConfig import InitialConfig
from fastapi import Depends, FastAPI, HTTPException
from schemas.FeeCalcRequestSchema import FeeCalcRequestSchema

app = FastAPI(title="FastAPI Shirt app",
              description="python project with fastAPI",
    summary="Practice project with python and fastAPI",
    version="0.0.1")
db = load_db()



@app.post("/delivery_fee", )
def get_delivery_fee(input: FeeCalcRequestSchema):
    fee = calculate_fee(input=input, config=db)
    return fee


@app.get("/", )
def get_root():
    return {"message": "Hel  lo World"}


if __name__ == "__main__":
    print("this function is happy to be called directly.")
    uvicorn.run("app:app", reload=True)
    #config = uvicorn.Config("app:app", port=5000, log_level="info", reload=True)
    #server = uvicorn.Server(config)
    #server.run()