from fastapi import FastAPI, APIRouter
from config.db import connect_with_connector
from models.group import teamup_group_data
from schema.group import GroupModel


engine = connect_with_connector()
conn = engine.connect()
# with engine.connect() as connection:
#     result = connection.execute(sqlalchemy.text("""
#     select * 
#     from `teamup-group-db`.`teamup_group_data` 
#     limit 3
#     """)).fetchall()

#     print(result)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()



router = APIRouter()

@router.get("/")
async def read_root():
    return {"group_service_status": "ONLINE"}

@router.get("/groups")
async def get_groups():
    return conn.execute(teamup_group_data.select()).fetchall()


# @router.get("/groups/{id}")
# async def get_group_by_id(id: str):
#     return conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchall()


# @router.post("/groups")
# async def create_group(group: GroupModel):
#     conn.execute(teamup_group_data.insert().values(
#         group_id = group.group_id,
#         groupname = group.groupname,
#         organizer = group.organizer,
#         location = group.location,
#         category = group.category,
#         intro = group.intro,
#         policy = group.policy
#     ))
#     return conn.execute(teamup_group_data.select()).fetchall()


# @router.put("/groups/{id}")
# async def update_group_info(id: str, group: GroupModel):
#     conn.execute(teamup_group_data.update(
#         groupname = group.groupname,
#         organizer = group.organizer,
#         location = group.location,
#         category = group.category,
#         intro = group.intro,
#         policy = group.policy
#     ).where(teamup_group_data.c.group_id == id))
#     return conn.execute(teamup_group_data.select()).fetchall()

# @router.delete("/groups/{id}")
# async def get_groups(id: str):
#     conn.execute(teamup_group_data.delete().where(teamup_group_data.c.group_id == id))
#     return conn.execute(teamup_group_data.select()).fetchall()


app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)