
## API Endpoints
### Groups
- `/`
  -  {"group_service_status": "ONLINE"}

- `/groups`
  - return all groups,
  - filter by `category`, `city`, `page`, `page_size`

- `/groups/{group_id}`
  - detail info of a group

- `/groups/create` + `body`
  - create a group
  - support smartystreets api check: whether city & state is valid

- `/groups/update/{group_id}` + `body`
  - update any group detail info, except group_id
  - support smartystreets api check: whether city & state is valid
 
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

### GraphQL query
- `/graphql`
  ```
  query Ex{
    groups {
      groupId
      groupName
    }
  }
  ```
  ```
  query Ex{
    group(groupId: "some id"){
      groupId
      groupName
    }
  }
  ```
