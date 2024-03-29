# Project structure

```bash
.
├── Dockerfile
├── Dockerfile_test
├── compose.yaml
├── readme.md
├── requirements.txt
├── noxfile.py
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
    └── test_response.py
```


### ./Docerfile
This file is used by docker compose to build the API image

### ./Dockerfile_test
this file is used by docker compose to build the image for testing the API, the API image will not be built if the tests fail.

### ./noxfile.py
nox will create a seperate environment, in which it installs pytest and runs the test, and also runs the linter. for now there is only one non default rule for the linter that being the max line lenght declared in the .flake8 file. In the future code standards could be decided and added to the project. 

### ./requirements.txt
This file includes needed packages to build and test the API, for simplicity there is only one requirements.txt for both the test and the API itself.

### ./compose.yml
This file incudes 2 services. One ´api´ and one ´api-tests´. ´api´ depends on ´api-tests´. Docker builds the image based on this file.

### src/app.py
Contains the main fastAPI application that defines root and methods in the API. Requests to the API land into get_delivery_fee of this file first. In the get_delivery_fee function input is converted to FeeCalcRequestSchema and is fed into calculate_fee.

### src/db/db.json
This file has all of the constant values declared in the question. The reason we are not using Docker env_file instead is that when loading db the schema validator can be checked to validate the initial values, in case these values need to be checked in the future when db gets bigger, and more complicated. This file is mapped to a valumo in the API container, and so if the initial values need to be changed the hole image does not need to be rebuilt, restarting the container is enough.

### src/schemas/FeeCalcRequestSchema.py
This file has input validators in place that is done thanks to type hints enforced by pydantic library. At the moment the API responds to apst and future delivery time requests and only cares about the dates being valid dates, depending on the business policies past and future times could be made invalid.

### src/schemas/InitialConfig.py
InitialConfig is used to validate db. This validation is also done thanks to type hints enforced by pydantic library.

### src/schemas/resposne_schemas.py
This file declare and validates response schema

### src/tools/deliveryFeeCalculator.py
This file is the heart of the calculator API. The FeeCalculator class in this file has all the functions needed to calculate delivery surcharges. These methods are called by calculate_fee function in turn.

### src/tools/loadDb
Load_db function reads, validates and returns the data in the database.

### src/tests/test_deliveryFeeCalculator.py
Given that the tests directory is the defult directory that pytest scans for test files, test_deliveryFeeCalculator.py is placed here. This file has test cases for all of the methods listed in the FeeCalculator class.  

### src/tests/test_response.py
This file has tests for valid and invalid requests. The valid requests should get 200 response code alongside a response body in the specified format. And invalid requests 422 response code.

# How to use
First build and run:
```bash
docker compose build
docker compose up
```
Then test the app by sending a curl request:
```bash
curl --location '127.0.0.1:8000/' \
--header 'Content-Type: application/json' \
--data '{"cart_value":1, "delivery_distance":3, "number_of_items":1, "time": "2024-05-22T12:23:04Z"}'
```
Alternatively open a browser and go to ``` http://localhost:8000/docs ```,  you should see the app up and running. Post requests could be sent from here as well. This is a security isuue that has to be addressed in the future by implementing authentication.
