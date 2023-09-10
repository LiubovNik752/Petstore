import json
from pydantic import BaseModel
import requests

# class Pet(BaseModel):
#     id: int
#     name: str
#     status: str


class Create_pet():
    """Добавление нового питомца"""
    url = "https://petstore.swagger.io/v2/pet/"
    name = "Ralf"
    status = "Available"
    body = {"name": name, "status": status}
    response = requests.post(url, json=body)

    def get_response(self):
        response = requests.post(self.url, json=self.body)
        return response

    def get_dict_response(self):
        dict_response = json.loads(self.response.content)
        return dict_response

    def get_value_id(self):
        self.value_id = self.get_dict_response().get('id')
        return self.value_id

    def get_pet_byId(self):
        get_url = 'https://petstore.swagger.io/v2/pet/' + str(self.value_id)
        get_pet_response = requests.get(get_url)
        return get_pet_response




    # @validator("name")
    # @classmethod
    # def validate_name(cls, value):
    #     if value > 16:
    #         raise ValueError("Pet name must be less than 16 symbols")
    #     return value