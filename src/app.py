import logging
import uvicorn
from tools.deliveryFeeCalculator import calculate_fee
from tools.loadDb import load_db
from schemas.resposne_schemas import SuccessfulFeeCalculationResposneSchema, HTTPError
from fastapi import FastAPI, HTTPException
from schemas.FeeCalcRequestSchema import FeeCalcRequestSchema

app = FastAPI(title="Delivery fee calculator app",
              description="Delivery fee calculator app with fastAPI",
              summary="Delivery fee calculator app with fastAPI",
              version="1.0.0")
db = load_db()


@app.post("/",
          responses={200: {"model": SuccessfulFeeCalculationResposneSchema},
                     500: {"model": HTTPError,
                           "description": "In case something goes wrong"}})
def calculate_delivery_fee(input: FeeCalcRequestSchema):
    try:
        fee = calculate_fee(input=input.model_dump(), config=db)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail="A Terrible Failure happebed in calculating the fee"
        )
    return SuccessfulFeeCalculationResposneSchema(delivery_fee=fee)


if __name__ == "__main__":
    print("this function is happy to be called directly.")
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=False, host='0.0.0.0')
    server = uvicorn.Server(config)
    server.run()
