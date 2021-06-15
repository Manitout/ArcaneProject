from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):

    id = fields.IntField(pk=True)
    firstname = fields.CharField(max_length=250)
    name = fields.CharField(max_length=250)
    birthdate = fields.CharField(max_length=250)


class Good(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=250)
    description  = fields.CharField(max_length=500)
    city = fields.CharField(max_length=250)
    type_of_good = fields.CharField(max_length=250)
    number_of_room = fields.IntField(default=0)
    room_characteristics = fields.CharField(max_length=500)
    
    owner = fields.ForeignKeyField('models.User', related_name='good_owner')



User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

Good_Pydantic = pydantic_model_creator(Good, name="Good")
GoodIn_Pydantic = pydantic_model_creator(Good, name="GoodIn", exclude_readonly=True)