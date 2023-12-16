
## API Endpoints
### Groups
- `/`
  -  {"group_service_status": "ONLINE"}

- `/groups`
  - return all groups,
  - filter by `category`, `location`, `page`, `page_size`

- `/groups/{group_id}`
  - detail info of a group

- `/groups/create` + `body`
  - create a group

- `/groups/update/{group_id}` + `body`
  - update group detail info, except group_id
 
- `/groups/delete/{group_id}`
  - delete a group

### Group Member Relationships
- `/group_member_rel/user/{username}`
  - For the given user, all the groups he/she joined

- `/group_member_rel/group/{group_id}`
  - All the members of that group
 
- `/group_member_rel/join` + `body`
  - user join group

- `/group_member_rel/leave/{group_id}/{username}`
  - user leave group
