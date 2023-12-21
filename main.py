from fastapi import FastAPI, APIRouter, HTTPException
from controllers.group import graphql_router
from config.db import conn
from fastapi.middleware.cors import CORSMiddleware
from models.group import teamup_group_data, teamup_group_member_rel_data
from schema.group import GroupModel, UpdateGroupModel, GroupMemberModel
import uvicorn
import sqlalchemy
from typing import Optional
from external.city_validate import city_validate


router = APIRouter()

"""Group Service"""
"""GET"""
@router.get("/")
async def read_root():
    return {"group_service_status": "ONLINE"}


@router.get("/groups")
async def get_groups(category: Optional[str] = None, city: Optional[str] = None, page: int = 1, page_size: int = 5):
    offset = (page - 1) * page_size
    query = (
        teamup_group_data.select()
        .offset(offset)
        .limit(page_size)
    )
    if category:
        query = query.where(teamup_group_data.c.category == category)
    if city:
        query = query.where(teamup_group_data.c.city == city)
        
    return conn.execute(query).fetchall()


@router.get("/groups/{id}")
async def get_group_by_id(id: str):
    group_data = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchall()

    if not group_data:
        raise HTTPException(status_code=404, detail=f"Group ID of {id} not found")

    return group_data


"""POST"""
@router.post("/groups/create")
async def create_group(group: GroupModel):
    find = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == group.group_id)).fetchone()
    if find:
        raise HTTPException(status_code=409, detail=f"Group ID of {group.group_id} already taken")
    
    # validate the city and state name using smartystreets
    cities = city_validate(group.city, group.state)
    if not cities:
        raise HTTPException(status_code=422, detail=f"The city {group.city} and state {group.state} you enter is not valid")

    conn.execute(teamup_group_data.insert().values(
        group_id = group.group_id,
        group_name = group.group_name,
        founder = group.founder,
        city = group.city,
        state = group.state,
        category = group.category,
        intro = group.intro,
        policy = group.policy
    ))
    return conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == group.group_id)).fetchone()


"""PUT"""
@router.put("/groups/update/{id}")
async def update_group_info(id: str, update_group: UpdateGroupModel):
    # Fetch the current values from the database
    db_item = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchone()

    if not db_item:
        raise HTTPException(status_code=404, detail=f"Group ID of {id} not found")

    # validate the city and state name using smartystreets
    cities = city_validate(group.city, group.state)
    if not cities:
        raise HTTPException(status_code=422, detail=f"The city {group.city} and state {group.state} you enter is not valid")

    # Create a dictionary with the updated values
    update_values = {key: value for key, value in update_group.dict().items() if value is not None}

    # Update only the specified columns while keeping the old values for others
    update_statement = sqlalchemy.text(
        f"UPDATE teamup_group_data SET {', '.join([f'{key} = :{key}' for key in update_values])} WHERE group_id = :group_id"
    )
    conn.execute(update_statement, {**update_values, "group_id": id})

    return conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchone()


"""DELETE"""
@router.delete("/groups/delete/{id}")
async def delete_group(id: str):
    db_item = conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == id)).fetchone()

    if not db_item:
        raise HTTPException(status_code=404, detail=f"Group ID of {id} not found")

    conn.execute(teamup_group_data.delete().where(teamup_group_data.c.group_id == id))
    return {"message": "Group deleted successfully"}




"""Group Member Relationship Service"""
@router.get("/group_member_rel/user/{username}")
async def get_groups_by_username(username: str):
    user_url = '/users/name/' + username
    group_data = conn.execute(teamup_group_member_rel_data.select().where(teamup_group_member_rel_data.c.username == user_url)).fetchall()

    if not group_data:
        raise HTTPException(status_code=404, detail=f"User name of {username} not found")

    return group_data


@router.get("/group_member_rel/group/{group_id}")
async def get_members_by_group(group_id: str):
    group_url = '/groups/' + group_id
    member_data = conn.execute(teamup_group_member_rel_data.select().where(teamup_group_member_rel_data.c.group_id == group_url)).fetchall()

    if not member_data:
        raise HTTPException(status_code=404, detail=f"Group id of {group_id} not found")

    return member_data


@router.post("/group_member_rel/join")
async def user_join_group(body: GroupMemberModel):
    group_url = '/groups/' + body.group_id
    user_url =  '/users/name/' + body.username
    find = conn.execute(teamup_group_member_rel_data.select().where(
                        (teamup_group_member_rel_data.c.group_id == group_url) & 
                        (teamup_group_member_rel_data.c.username == user_url))).fetchone()
    if find:
        raise HTTPException(status_code=409, detail=f"User {body.username} already in the group {group_id}")
    
    conn.execute(teamup_group_member_rel_data.insert().values(
        group_id = group_url,
        username = user_url
    ))
    return conn.execute(teamup_group_member_rel_data.select().where(
                        (teamup_group_member_rel_data.c.group_id == group_url) & 
                        (teamup_group_member_rel_data.c.username == user_url))).fetchone()


@router.delete("/group_member_rel/leave/{group_id}/{username}")
async def user_leave_group(group_id: str, username: str):
    group_url = '/groups/' + group_id
    user_url =  '/users/name/' + username
    db_item = conn.execute(teamup_group_member_rel_data.select().where(
                          (teamup_group_member_rel_data.c.group_id == group_url) & 
                          (teamup_group_member_rel_data.c.username == user_url))).fetchone()

    if not db_item:
        raise HTTPException(status_code=404, detail=f"User {username} is not in the group {group_id}")

    conn.execute(teamup_group_member_rel_data.delete().where(
                (teamup_group_member_rel_data.c.group_id == group_url) & 
                (teamup_group_member_rel_data.c.username == user_url)))
    return {"message": "User left group successfully"}


app = FastAPI()
app.include_router(router)
app.include_router(graphql_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)