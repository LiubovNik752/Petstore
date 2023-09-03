import requests
import pytest


class Test_post_request:
    url = "https://petstore.swagger.io/v2/pet/"
    name = "Ralf"
    status = "Available"
    body = {"name": name, "status": status}
    response = requests.post(url, json=body)

    @pytest.mark.create
    def test_check_status_code(self):
        assert self.response.status_code == 200

    @pytest.mark.create
    def test_check_header(self):
        assert self.response.headers['Content-Type'] == "application/json"


    def test_check_response_positive(self):
        assert self.response.json().get('name') == "Ralf"


    def test_check_reponse_negative(self):
        assert self.response.json().get('status') != "Sold"


class Test_put_request:
    url = "https://petstore.swagger.io/v2/pet"
    new_name = "Rick"
    status = "Sold"
    body = {"name": new_name}
    response = requests.put(url, json=body)

    @pytest.mark.update
    def test_check_status_code(self):
        assert self.response.status_code == 200

    def test_check_header(self):
        assert self.response.headers['Content-Type'] == "application/json"

    def test_check_response_positive(self):
        assert self.response.json().get('name') == "Rick"

    def test_check_response_negative(self):
        assert self.response.json().get('name') != "Ralf"
