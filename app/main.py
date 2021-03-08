# Standard
from datetime import date
# Third Party
import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse
# Local
from app.data_models import SearchResponse, SubmitRates, UploadResponse
from app.helpers import Rating, price_convert

app = FastAPI(title='RatesTask API')


@app.get("/rates/", name="Rates", response_model=SearchResponse)
async def rates(
    origin: str, destination: str, date_from: date, date_to: date

):

    """
        The Average Prices for each day on a route between port codes origin and destination.
    """
    # ----------------------------------Checking date range ----------------------------------
    if date_from > date_to:
        return JSONResponse(status_code=400,
                            content={"status": "error", "message": "date_from is greater than date_to"})
    # ----------------- Fetching Details ----------------------------------------------------
    rating_obj = Rating(origin, destination, date_from, date_to)
    return SearchResponse(result=rating_obj.search(null_results=False))


@app.get("/rates_null/", name="Rates Null", response_model=SearchResponse)
async def rates_null(
    origin: str, destination: str, date_from: date, date_to: date
):
    """
        Finding, an empty value (JSON null) for days on which there are less than 3 prices in total.
    """
    # ----------------------------------Checking date range ----------------------------------
    if date_from > date_to:
        return JSONResponse(status_code=400, content={"status": "error", "message": "date_from is greater than date_to"})
    # ----------------- Fetching Details ----------------------------------------------------
    rating_obj = Rating(origin, destination, date_from, date_to)
    return SearchResponse(result=rating_obj.search(null_results=True))


@app.post("/upload_price/", name="Upload Price", response_model=UploadResponse)
async def upload_price(
    request: SubmitRates
):
    """
        Uploading price with or without using currency, Currency field is optional.
    """
    # ----------------------------------Checking date range ----------------------------------
    if request.date_from > request.date_to:
        return JSONResponse(status_code=400, content={"status": "error", "message": "date_from is greater than date_to"})
    # ------------------ Price Checking Before Convert----------------------------------------
    price = price_convert(request)
    if price is None:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid Currency Code"})
    # --------------------Saving Price--------------------------------------------------------
    rating_obj = Rating(request.origin, request.destination, request.date_from, request.date_to)
    # --------------------- Response ----------------------------------------------------------
    return UploadResponse(result=rating_obj.upload(price))

# To run using using command line
#  uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, port=8000)

