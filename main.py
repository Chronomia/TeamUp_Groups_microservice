from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/api/groups")
def list_groups():
    return {"groups": [{"id": 1, "name": "Group1"}, {"id": 2, "name": "Group2"}]}

@app.get("/api/groups/{group_id}")
def get_group(group_id: int):
    return {"group": {"id": group_id, "name": f"Group{group_id}"}}

@app.get("/api/groups/{group_id}/users")
def get_group_users(group_id: int):
    return {"users": [{"user_id": 1, "username": "User1"}, {"user_id": 2, "username": "User2"}]}

@app.get("/api/groups/{group_id}/events")
def get_group_events(group_id: int):
    return {"events": [{"event_id": 1, "name": "Event1"}, {"event_id": 2, "name": "Event2"}]}

@app.get("/api/groups/{group_id}/records")
def get_group_records(group_id: int):
    return {"records": [{"record_id": 1, "name": "Record1"}, {"record_id": 2, "name": "Record2"}]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
