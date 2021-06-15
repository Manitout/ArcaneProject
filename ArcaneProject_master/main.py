from fastapi import FastAPI, HTTPException
from models import User, User_Pydantic, UserIn_Pydantic, Good, Good_Pydantic, GoodIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel


app = FastAPI()

@app.post("/user/", response_model=User_Pydantic)
async def create(user: UserIn_Pydantic):
    obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(obj)

@app.put("/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_user(user_id: int, user: UserIn_Pydantic):
    await User.filter(id= user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id= user_id))

@app.post('/good/{user_id}')
async def get_one_good(user_id: int, goods_details: GoodIn_Pydantic):
    user = await User.get(id=user_id)
    obj = await Good.create(**goods_details.dict(exclude_unset=True), owner = user)
    response = await Good_Pydantic.from_tortoise_orm(obj)
    return {"status": "ok", "data": response}


@app.put("/good/{good_id}&{user_id}", response_model=Good_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_good(good_id: int,user_id:int, good: GoodIn_Pydantic):
    if await test_owner_good(good_id,user_id):
        await Good.filter(id= good_id).update(**good.dict(exclude_unset=True))
        return await Good_Pydantic.from_queryset_single(Good.get(id= good_id))
    else:
        raise HTTPException(status_code=404, detail="Not allowed to change content")

@app.delete("/good/{good_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_user(good_id: int,user_id:int,):
    if await test_owner_good(good_id,user_id):
        delete_obj = await Good.filter(id= good_id).delete()
        if not delete_obj:
            raise HTTPException(status_code=404, detail="this good is not found")
        return {"status": "Successfully deleted", "data": "not here anymore"}
    else:
        raise HTTPException(status_code=404, detail="Not allowed to delete content")

async def test_owner_good(good_id:int, user_id:int):
    user = await User.get(id=user_id) 
    goodY = await Good.filter(owner=user)
    goodT = await Good.get(id=good_id)
    value = 0
    for t in goodY:
        if t==goodT:
            value=1
    return value

register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
