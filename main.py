from fastapi import FastAPI, APIRouter, HTTPException
from config.db import connect_with_connector
from models.group import teamup_group_data
from schema.group import GroupModel, UpdateGroupModel
import uvicorn
import sqlalchemy
from typing import Optional

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
async def get_groups(category: Optional[str] = None, location: Optional[str] = None, page: int = 1, page_size: int = 5):
    offset = (page - 1) * page_size
    query = (
        teamup_group_data.select()
        .offset(offset)
        .limit(page_size)
    )
    if category:
        query = query.where(teamup_group_data.c.category == category)
    if location:
        query = query.where(teamup_group_data.c.location == location)
        
    return conn.execute(query).fetchall()


@router.get("/groups/{id}")
async def get_group_by_id(id: str):
    group_data = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchall()

    if not group_data:
        raise HTTPException(status_code=404, detail=f"Group ID of {id} not found")

    return group_data


@router.post("/groups/create")
async def create_group(group: GroupModel):
    find = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == group.group_id)).fetchone()
    if find:
        raise HTTPException(status_code=409, detail=f"Group ID of {group.group_id} already taken")
    
    conn.execute(teamup_group_data.insert().values(
        group_id = group.group_id,
        groupname = group.groupname,
        organizer = group.organizer,
        location = group.location,
        category = group.category,
        intro = group.intro,
        policy = group.policy
    ))
    return conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == group.group_id)).fetchone()


@router.put("/groups/update/{id}")
async def update_group_info(id: str, update_group: UpdateGroupModel):
    # Fetch the current values from the database
    db_item = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchone()

    if db_item is None:
        raise HTTPException(status_code=404, detail=f"Group ID of {id} not found")

    # Create a dictionary with the updated values
    update_values = {key: value for key, value in update_group.dict().items() if value is not None}

    # Update only the specified columns while keeping the old values for others
    update_statement = sqlalchemy.text(
        f"UPDATE teamup_group_data SET {', '.join([f'{key} = :{key}' for key in update_values])} WHERE group_id = :group_id"
    )
    conn.execute(update_statement, {**update_values, "group_id": id})

    return conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchone()


@router.delete("/groups/delete/{id}")
async def get_groups(id: str):
    db_item = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchone()

    if db_item is None:
        raise HTTPException(status_code=404, detail=f"Group ID of {id} not found")
        
    conn.execute(teamup_group_data.delete().where(teamup_group_data.c.group_id == id))
    return {"message": "User deleted successfully"}


app = FastAPI()
app.include_router(router)



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)