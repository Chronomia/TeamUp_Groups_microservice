from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

### Groups
# Sample data
groups = [
    {'id': 1, 'name': 'Hiking'},
    {'id': 2, 'name': 'CityWalk'}
]


class Group(BaseModel):
    id: int
    name: str


@app.get("/")
def read_root():
    return {"message": "Hello, World"}


@app.get("/api/groups", response_model=List[Group])
def get_groups():
    return groups


@app.get("/api/groups/{group_id}", response_model=Group)
def get_group(group_id: int):
    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        raise HTTPException(status_code=404, detail='Group not found')
    return group


@app.post("/api/groups", response_model=Group)
def create_group(group: Group):
    groups.append(group.model_dump())
    return group


@app.get("/api/groups/{group_id}/users")
def get_group_users(group_id: int):
    # Sample data, you'd replace this with a query to your data source
    users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    return users


@app.get("/api/groups/{group_id}/events")
def get_group_events(group_id: int):
    # Sample data, you'd replace this with a query to your data source
    events = [{'id': 1, 'name': 'Event A'}, {'id': 2, 'name': 'Event B'}]
    return events


@app.get("/api/groups/{group_id}/records")
def get_group_records(group_id: int):
    # Sample data, you'd replace this with a query to your data source
    records = [{'id': 1, 'detail': 'Record A'}, {'id': 2, 'detail': 'Record B'}]
    return records



### Records
# Sample data
records = [
    {'id': 1, 'detail': 'Record A'},
    {'id': 2, 'detail': 'Record B'}
]


class Record(BaseModel):
    id: int
    detail: str


@app.get("/api/records", response_model=List[Record])
def get_records():
    return records


@app.get("/api/records/{record_id}", response_model=Record)
def get_record(record_id: int):
    record = next((r for r in records if r['id'] == record_id), None)
    if not record:
        raise HTTPException(status_code=404, detail='Record not found')
    return record


@app.get("/api/records/{record_id}/group")
def get_record_group(record_id: int):
    # Sample data, you'd replace this with a query to your data source
    group = [{'id': 1, 'name': 'Hiking'}]
    return group


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)