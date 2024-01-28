import logging
import uvicorn
from tools.deliveryFeeCalculator import calculate_fee
from tools.loadDb import load_db
from schemas.resposne_schemas import resposne_schema

from fastapi import Depends, FastAPI, HTTPException
from schemas.FeeCalcRequestSchema import FeeCalcRequestSchema

app = FastAPI(title="FastAPI Shirt app",
              description="python project with fastAPI",
    summary="Practice project with python and fastAPI",
    version="0.0.1")
db = load_db()



@app.post("/", response_model=resposne_schema)
def get_delivery_fee(input: FeeCalcRequestSchema):
    try:
        fee = calculate_fee(input=input.model_dump(), config=db)
    except Exception as e:
        logging.error(e)
        return {"message": "Problem in calculating fee."}
    return {"delivery_fee": fee}





if __name__ == "__main__":
    print("this function is happy to be called directly.")
    #uvicorn.run("app:app", reload=False)
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=False, host='0.0.0.0')
    server = uvicorn.Server(config)
    server.run()
