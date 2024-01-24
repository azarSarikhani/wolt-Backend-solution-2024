import os
import uvicorn
from tools.deliveryFeeCalculator import calculate_fee
from tools.loadDb import load_db
from schemas.resposne_schemas import resposne_schema

from schemas.InitialConfig import InitialConfig
from fastapi import Depends, FastAPI, HTTPException
from schemas.FeeCalcRequestSchema import FeeCalcRequestSchema

app = FastAPI(title="FastAPI Shirt app",
              description="python project with fastAPI",
    summary="Practice project with python and fastAPI",
    version="0.0.1")
db = load_db()



@app.post("/delivery_fee", response_model=resposne_schema)
def get_delivery_fee(input: FeeCalcRequestSchema):
    fee = calculate_fee(input=input, config=db)
    return {"delivery_fee": fee}





if __name__ == "__main__":
    print("this function is happy to be called directly.")
    #uvicorn.run("app:app", reload=False)
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=False, host='0.0.0.0')
    server = uvicorn.Server(config)
    server.run()