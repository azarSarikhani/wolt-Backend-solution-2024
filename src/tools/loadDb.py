import json
from src.schemas.InitialConfig import InitialConfig
from pydantic import ValidationError
	

def load_db() -> InitialConfig:
	"""Load initial values from the JSON file"""
	with open("./src/db/db.json") as f:
		data = json.load(f)
	try:
		InitialConfig.model_validate(data)
	except ValidationError:
		raise
	return data