from decimal import Decimal
import datetime
import unittest
from fastapi.testclient import TestClient
from helpers import Rating
from main import app

client = TestClient(app)

# Basic Test Cases:


class TestRates(unittest.TestCase):

    def test_fetch_valid_shipping_rates_between_port_and_slug(self):
        rating_obj = Rating('CNSGH','north_europe_main', datetime.date(2016, 1, 1),datetime.date(2016, 1, 2))
        output = rating_obj.search(null_results=False)
        expected_output = [
        {
            "day": datetime.date(2016, 1, 1),
            "average_price": Decimal('1076.61')
        },
        {
            "day": datetime.date(2016, 1, 2),
            "average_price": Decimal('1076.61')
        }]
        self.assertEqual(expected_output, output)

    def test_fetch_valid_shipping_rates_between_two_ports(self):
        rating_obj = Rating('CNSGH', 'EETLL', datetime.date(2016, 1, 1), datetime.date(2016, 1, 2))
        output = rating_obj.search(null_results=False)
        print(output)
        expected_output = [
        {
            "day": datetime.date(2016, 1, 1),
            "average_price": Decimal('1059.33')
        },
        {
            "day": datetime.date(2016, 1, 2),
            "average_price": Decimal('1059.33')
        }]
        self.assertEqual(expected_output, output)

    def test_valid_upload_of_prices_between_date_range(self):
        expected_output = [
            {"origin": "CNSGH",
             "destination": "CNSGH",
             "day": datetime.date(2021, 3, 29),
             "price": 2
             },
            {
                "origin": "CNSGH",
                "destination": "CNSGH",
                "day": datetime.date(2021, 3, 30),
                "price": 2
            }]
        rating_obj = Rating('CNSGH', 'CNSGH', datetime.date(2021, 3, 29), datetime.date(2021, 3, 30))
        output = rating_obj.upload(2)
        self.assertEqual(expected_output, output)

    def test_fetch_valid_shipping_rates_with_null_between_two_ports_returns_null_if_count_less_than_3(self):
        rating_obj = Rating('CNSGH', 'CNSGH', datetime.date(2021, 3, 29), datetime.date(2021, 3, 31))
        output = rating_obj.search(null_results=True)
        expected_output = [
            {
                "day": datetime.date(2021, 3, 29),
                "average_price": None
            },
            {
                "day": datetime.date(2021, 3, 30),
                "average_price": None
            }]
        self.assertEqual(expected_output, output)

    def test_api_post_with_date_from_greter_than_date_to(self):
        """Check a post request with no date_from."""
        result = client.post('/upload_price/',
                                    json={"origin":"CNSGH", "destination":"CNSGH", "date_from":"2018-02-13", "date_to":"2018-02-12",
                                              "price":"1000"})
        self.assertEqual(result.status_code, 400)
        self.assertIn('{"status":"error","message":"date_from is greater than date_to"}', result.text)

    def test_api_post_with_correct_currency_code(self):
        """Check a post request with no date_from."""
        result = client.post('/upload_price/',
                                    json={"origin":"CNSGH", "destination":"CNSGH", "date_from":"2018-02-11", "date_to":"2018-02-12",
                                              "price":"78", "currency_code": "INR"})
        self.assertEqual(result.status_code, 200)
        self.assertIn('{"result":[{"origin":"CNSGH","destination":"CNSGH","day":"2018-02-11","price":1},'
                      '{"origin":"CNSGH","destination":"CNSGH","day":"2018-02-12","price":1}]}', result.text)

    def test_api_post_with_invalid_currency_code(self):
        """Check a post request with no date_from."""
        result = client.post('/upload_price/',
                                    json={"origin":"CNSGH", "destination":"CNSGH", "date_from":"2018-02-11", "date_to":"2018-02-12",
                                              "price":"78", "currency_code": "IND"})
        print(result.text)
        self.assertEqual(result.status_code, 400)
        self.assertIn('{"status":"error","message":"Invalid Currency Code"}', result.text)


# Tests conveniently executable
if __name__ == "__main__":
    unittest.main()