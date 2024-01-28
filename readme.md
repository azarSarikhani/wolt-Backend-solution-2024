# Project structure

```bash
.
├── Dockerfile
├── Dockerfile_test
├── compose.yaml
├── readme.md
├── requirements.txt
├── src
│   ├── app.py
│   ├── db
│   │   └── db.json
│   ├── schemas
│   │   ├── FeeCalcRequestSchema.py
│   │   ├── InitialConfig.py
│   │   └── resposne_schemas.py
│   └── tools
│       ├── deliveryFeeCalculator.py
│       └── loadDb.py
└── tests
    ├── __init__.py
    └── test_deliveryFeeCalculator.py
```


## Docerfile
This file is used by docker compose to build the API image

## Dockerfile_test
this file is used by docker compose to build the image for testing the API, the API image will not be built if the tests fail.

## requirements.txt
This file includes needed packages to build and test the API, for simplicity thereis only one requirements.txt for both the test and the API itself.

## compose.yml
This file incudes 2 services. One ´api´ and one ´api-tests´. ´api´ depends on ´api-tests´ is used by Docker to build 

# How to use
docker compose build
docker compose up 
