import uvicorn
from tools import loadDb, calculate_fee
from schemas.InitialConfig import InitialConfig
from fastapi import Depends, FastAPI, HTTPException
from schemas.FeeCalcRequestSchema import FeeCalcRequestSchema

app = FastAPI()

# Dependency
def get_db():
    db = loadDb.load_db()
    return db



@app.post("/delivery_fee/", )
def get_delivery_fee(input: FeeCalcRequestSchema, db: InitialConfig = Depends(get_db)):
    fee = calculate_fee(input=input, config=db)
    return fee



if __name__ == "__main__":
    print("this function is happy to be called directly.")
    uvicorn.run("app:app", reload=True)