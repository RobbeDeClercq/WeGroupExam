from __future__ import absolute_import

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response
import requests

from app.models.zipcode import ZipCodeRiskFactor


class IndexResponse(BaseModel):
    index: float


async def get_index(request: Request, year: int = 2004):
    import datetime

    # EXERCISE 1
    # TODO INDEX_1
    # Make sure only 1996, 2004 and 2013 are valid
    # https://fastapi.tiangolo.com/tutorial/handling-errors/
    # tip: from fastapi import HTTPException
    if year not in {1996, 2004, 2013}:
        raise HTTPException(status_code=404, detail="WRONG_YEAR")

    # TODO INDEX_2
    # Retrieve the latest index from external source for given base year
    # https://statbel.fgov.be/en/themes/consumer-prices/health-index
    index = 100.00

    d = datetime.datetime.now()
    m = int(d.strftime("%m")) - 1

    url = "https://indexpub.economie.fgov.be/indexpub/api/ng-indsearch/get-consumer-health-index/{}/2020/IS".format(m)

    data = requests.get(url).json()

    # TODO INDEX_3
    # Format and return the response
    for item in data:
        if item["base"]["code"] == str(year):
            index = item["value"]

    return {"index": index}

async def get_zipcode_risk_factor(request: Request, zipcode: int):
    import csv
    # EXERCISE 2
    # TODO ZIPCODE_1
    # Validate if the zipcode entered has the correct format
    # (integer between 1000 and 9999)
    if zipcode < 1000 or zipcode > 9999:
        raise HTTPException(status_code=404, detail="ZIPCODE_NOT_VALID")
    # TODO ZIPCODE_2
    # Read the file app.data.zipcodes.csv and format data
    with open('app\data\zipcodes.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    # TODO ZIPCODE_3
    # Validate if the zipcode entered is in the dataset
    risk_factor = ""
    for item in data:
        if "-" in item[0]:
            item[0] = item[0].split(" - ")
            if zipcode >= int(item[0][0]) and zipcode <= int(item[0][1]):
                risk_factor = item[1]
                continue
        elif zipcode == int(item[0]):
            risk_factor = item[1]
            continue
    
    if risk_factor == "":
        raise HTTPException(status_code=400, detail="ZIPCODE_NOT_VALID")

    # TODO ZIPCODE_4
    # Formulate appropriate response
    return {"risk_factor": "{}".format(risk_factor)}


async def get_zipcode_risk_factor_from_database(request: Request, zipcode: int):
    # EXERCISE 3
    return await request.app.repositories.zipcodes.get(zipcode)


router = APIRouter()


router.add_api_route(
    "/index",
    get_index,
    include_in_schema=True,
    deprecated=False,
    methods=["GET"],
    status_code=200,
    description="Retrieve the latest Belgian health index from external source for given base year. (default 2004)",
    summary="Retrieve Belgian Health Index",
    tags=["EX1"],
    response_model=IndexResponse,
)


router.add_api_route(
    "/zipcode/{zipcode}",
    get_zipcode_risk_factor,
    include_in_schema=True,
    deprecated=False,
    methods=["GET"],
    status_code=200,
    description="Retrieve the risk factor associated with given zipcode",
    summary="Retrieve Zipcode Risk Factor",
    tags=["EX2"],
    response_model=ZipCodeRiskFactor,
)

router.add_api_route(
    "/databases/zipcode/{zipcode}",
    get_zipcode_risk_factor_from_database,
    include_in_schema=True,
    deprecated=False,
    methods=["GET"],
    status_code=200,
    description="Retrieve the risk factor associated with given zipcode from databases",
    summary="Retrieve Zipcode Risk Factor from database",
    tags=["EX3"],
    response_model=ZipCodeRiskFactor,
)
