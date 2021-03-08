# Standard
import json
from datetime import timedelta
# Third Party
import requests
from fastapi import HTTPException
# Local
from config import EXCHANGE_APP_ID, EXCHANGE_URL
from sql_app.database import get_session
from sql_app.sql_query import fetch_rates_query, insert_query


class Rating:
    def __init__(self, origin, destination, date_from, date_to):
        self.origin = origin
        self.destination = destination
        self.date_from = date_from
        self.date_to = date_to

    def search(self, null_results=False) -> list:
        """
        Searching the average prices for each day on a route between port codes origin and destination.
        :param null_results: For checking frequency of day prices < 3 , will count as null value
        :return: List of dict containing day and avg. price.
        """
        session = get_session()
        result = []
        try:
            db = session.execute(fetch_rates_query.format(self.origin, self.origin,  self.destination, self.destination, self.date_from, self.date_to))
            result = db.fetchall()
        except Exception as e:
            if session is not None:
                session.rollback()

            raise HTTPException(status_code=400, detail="Bad Request Error")
        finally:
            if session is not None:
                session.close()
        return self.results_filter(result, check_day_prices=null_results)

    def upload(self, price) -> str:
        """
        Uploading of price between date_from to date_to
        :param price: price input by user
        :return: done message means job has done.
        """
        session = get_session()
        result = []
        current_date = self.date_from
        day = timedelta(days=1)
        try:
            while current_date <= self.date_to:
                # Query for inserting data
                session.execute(
                    insert_query.format(self.origin, self.destination, current_date, int(price)))
                item = {"origin": self.origin, "destination": self.destination, "day": current_date, "price": int(price)}
                result.append(item)
                current_date += day  # Increment day
            # saving inputs to db
            session.commit()
        except Exception as e:
            # Rollback if any exception
            if session is not None:
                session.rollback()
            print(e)
            raise HTTPException(status_code=404, detail="Not found destination or origin")
        finally:
            # closes session
            if session is not None:
                session.close()
        return result

    @staticmethod
    def results_filter(result, check_day_prices=False, day_prc_limit=3) -> list:
        """
        :param result: Contains avg_price details per day.
        :param day_prc_limit: Threshold value for checking price per day .
        :param check_day_prices: Switch for checking null values.
        :return: Returns filtered results ad formatted into dict of list.
        """
        res_filter = []
        # appending dict to list -----------------------------------------------
        for day_result in result:
            if check_day_prices and day_result[2] < day_prc_limit:
                avg_price = None
            else:
                avg_price = round(day_result[1], 2)
            res_filter.append({'day': day_result[0], 'average_price': avg_price})
        return res_filter


def after_convert(price, source_currency, target_currency='USD'):
    """
    Conversion of currencies
    :param price: Input Price by user
    :param source_currency: Input Currency Code
    :param target_currency: Default set USD
    :return: Price if currency found else None
    """
    # rates_id = os.getenv("ID_EXCHANGE_RATE")
    if source_currency == target_currency:
        # No need to convert currency  ---
        return price
    # Making request to exchange API  ---
    response = requests.get(f"{EXCHANGE_URL}latest.json?app_id={EXCHANGE_APP_ID}")
    if response.status_code == 200:
        rates = json.loads(response.content)['rates']
        if source_currency in rates:
            # converting ---
            return float(price) / float(rates[source_currency])
    return None


def price_convert(request):
    if request.currency_code is None or len(request.currency_code) == 0:
        price = request.price
    else:
        price = after_convert(request.price, request.currency_code)
    return price

