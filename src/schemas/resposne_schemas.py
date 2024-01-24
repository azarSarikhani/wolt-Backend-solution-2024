from pydantic import BaseModel, Field

class resposne_schema(BaseModel):
    delivery_fee: int  = Field(description="Calculated delivery fee in cents.")