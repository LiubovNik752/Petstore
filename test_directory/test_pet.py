import json
import requests
import pytest

from pet_directory.classPet import Create_pet

@pytest.mark.create
class Test_create_pet:

    new_pet = Create_pet()
    response = new_pet.get_response()

    def test_check_status_code(self):
        assert self.response.status_code == 200

    def test_check_header(self):
        assert self.response.headers['Content-Type'] == "application/json"

    def test_check_response_positive(self):
        assert self.response.json().get('name') == "Ralf"

    def test_check_response_negative(self):
        assert self.response.json().get('status') != "Sold"

@pytest.mark.update
class Test_update_pet:
    url = "https://petstore.swagger.io/v2/pet"
    new_name = "Rick"
    status = "Sold"
    body = {"name": new_name, "status": status}
    response = requests.put(url, json=body)

    def test_check_status_code(self):
        assert self.response.status_code == 200

    def test_check_header(self):
        assert self.response.headers['Content-Type'] == "application/json"

    def test_check_response_positive(self):
        assert self.response.json().get('name') == "Rick"

    def test_check_response_negative(self):
        assert self.response.json().get('status') != "Available"


class Test_get_pet_byStatus:
    """Получение списка всех питомцев с указанным статусом"""
    status = ['available', 'pending', 'sold']
    url = 'https://petstore.swagger.io/v2/pet/findByStatus?status=' + status[0]
    response = requests.get(url)

    def test_check_status_code(self):
        assert self.response.status_code == 200

    def test_available_in_response(self):
        """Тест, проверяющий, что все статусы в ответе имеют значение available"""
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
        assert self.response.status_code == 200

    def test_check_pet_not_found(self):
        not_existed_id = 0
        get_url = 'https://petstore.swagger.io/v2/pet/' + str(not_existed_id)
        self.get_id_response = requests.get(get_url)
        self.dict_get_response = json.loads(self.get_id_response.content)
        assert self.get_id_response.status_code == 404
        assert self.dict_get_response.get("message") == 'Pet not found'

# @pytest.mark.update
# class Test_update_pet_byId:
#
#     new_pet = Create_pet()  # Создание питомца методом
#     id = new_pet.get_value_id()  # Получение id у созданного питомца
#     url = "https://petstore.swagger.io/v2/pet/" + str(id)
#     response = requests.post(url, data='name=New_name&status=sold')
#
#     def test_check_status_code_200(self):
#         print(self.new_pet.get_response())
#         assert self.response.status_code == 200
#         print(self.response.content)
#
#     def test_check_updated_pet_name(self):
#         url = 'https://petstore.swagger.io/v2/pet/' + str(self.id)
#         petId_response = requests.get(url)
#         dict_response = json.loads(petId_response.content)
#         print(dict_response)
#
#     def test_check_updated_status(self):
#         get_url = 'https://petstore.swagger.io/v2/pet/' + str(self.id)
#         get_pet_response = json.loads(requests.get(get_url).content)
#         assert get_pet_response.get("status") == "sold"


class Test_delete_pet:

    new_pet = Create_pet()  # Создание питомца методом
    value_id = new_pet.get_value_id()  # Получение id у созданного питомца
    url = 'https://petstore.swagger.io/v2/pet/' + str(value_id)
    response = requests.delete(url)

    def test_check_status_code_200(self):
        assert self.response.status_code == 200

    def test_check_pet_not_found(self):
        assert self.new_pet.get_pet_byId().status_code == 404


# class Test_check_validation:
    # pass
