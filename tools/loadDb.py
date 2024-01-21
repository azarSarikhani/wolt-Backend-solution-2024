import json
from schemas.InitialConfig import InitialConfig
	


def load_db() -> InitialConfig:
	"""Load initial values from the JSON file"""
	with open("db.json") as f:
		data = json.load(f)
	return data