import json
import requests
import pytest

from pet_directory.classPet import Create_pet

@pytest.mark.create
class Test_create_pet:

    new_pet = Create_pet()
    response = new_pet.get_response()

    def test_check_status_code(self):
        """Test status code is 200"""
        assert self.response.status_code == 200

    def test_check_header(self):
        """Test content-type header is json"""
        assert self.response.headers['Content-Type'] == "application/json"

    def test_check_response_positive(self):
        """Test name is Ralf"""
        assert self.response.json().get('name') == "Ralf"

    def test_check_response_negative(self):
        """Test status is Sold"""
        assert self.response.json().get('status') != "Sold"

@pytest.mark.update
class Test_update_pet:
    url = "https://petstore.swagger.io/v2/pet"
    new_name = "Rick"
    status = "Sold"
    body = {"name": new_name, "status": status}
    response = requests.put(url, json=body)

    def test_check_status_code(self):
        """Test status code is 200"""
        assert self.response.status_code == 200

    def test_check_header(self):
        """Test content-type header is json"""
        assert self.response.headers['Content-Type'] == "application/json"

    def test_check_response_positive(self):
        """Test name is Rick"""
        assert self.response.json().get('name') == "Rick"

    def test_check_response_negative(self):
        """Test status is not Available"""
        assert self.response.json().get('status') != "Available"


class Test_get_pet_byStatus:
    """Получение списка всех питомцев с указанным статусом"""
    status = ['available', 'pending', 'sold']
    url = 'https://petstore.swagger.io/v2/pet/findByStatus?status=' + status[0]
    response = requests.get(url)

    def test_check_status_code(self):
        """Test status code is 200"""
        assert self.response.status_code == 200

    def test_available_in_response(self):
        """Test all statuses in response have value 'available'"""
        self.list_status = [i.get('status') == 'available' for i in self.response.json()]
        assert all(self.list_status)


class Test_get_pet_byId:

    new_pet = Create_pet()  # Создание питомца
    value_id = new_pet.get_value_id()    # Получение id у созданного питомца
    response = new_pet.get_pet_byId()
    dict_get_id_response = json.loads(response.content)

    def test_get_response(self):
        """Проверка наличия в базе питомца по Id ранее созданного"""
        dict_get_id_response = json.loads(self.response.content)
        id = dict_get_id_response.get('id')
        assert id == self.value_id

    def test_check_status_code_200(self):
        """Test status code is 200"""
        assert self.response.status_code == 200

    def test_check_pet_not_found(self):
        """Negative test - pet not found"""
        not_existed_id = 0
        get_url = 'https://petstore.swagger.io/v2/pet/' + str(not_existed_id)
        self.get_id_response = requests.get(get_url)
        self.dict_get_response = json.loads(self.get_id_response.content)
        assert self.get_id_response.status_code == 404
        assert self.dict_get_response.get("message") == 'Pet not found'

@pytest.mark.update
class Test_update_pet_byId:

    new_pet1 = Create_pet()
    value_id = new_pet1.get_value_id()
    data = {"name": 'New_name', "status": 'sold'}
    url = "https://petstore.swagger.io/v2/pet/" + str(value_id)
    response = requests.post(url, data=data)

    def test_check_status_code_200(self):
        """Test status code is 200"""
        print(self.new_pet1.get_response())
        assert self.response.status_code == 200

    def test_check_updated_pet_name(self):
        """Test update name"""
        url = 'https://petstore.swagger.io/v2/pet/' + str(self.value_id)
        petId_response = requests.get(url)
        assert petId_response.json().get('name') == "New_name"

    def test_check_updated_status(self):
        """Test update status is sold"""
        get_url = 'https://petstore.swagger.io/v2/pet/' + str(self.value_id)
        get_pet_response = json.loads(requests.get(get_url).content)
        assert get_pet_response.get("status") == "sold"


class Test_delete_pet:

    new_pet = Create_pet()
    value_id = new_pet.get_value_id()
    url = 'https://petstore.swagger.io/v2/pet/' + str(value_id)
    response = requests.delete(url)

    def test_check_status_code_200(self):
        """Test status code is 200"""
        assert self.response.status_code == 200

    def test_check_pet_not_found(self):
        """Test pet not found"""
        assert self.new_pet.get_pet_byId().status_code == 404
