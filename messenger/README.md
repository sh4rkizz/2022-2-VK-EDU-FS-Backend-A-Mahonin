# URLs

## Chat /chats

#### GET

* **localhost:8000/chats/**            - Get index.html (chat-page)
* **localhost:8000/chats/list/**       - Get chat list
* **localhost:8000/chats/\<int:id>/**  - Get chat by its ID

#### POST

* **localhost:8000/chats/add/**        - Create new chat

### Test chat (curl)

##### POST

* **curl -d "message=Fine" -X POST http://127.0.0.1:8000/chats/1**
* **curl -d "name=Lesha&message=hey" -X POST http://127.0.0.1:8000/chats/new**

##### GET

* **curl http://127.0.0.1:8000/chats**
* **curl http://127.0.0.1:8000/chats/1**

## Users /users

#### GET

* **localhost:8000/users/username/\<int:user_id>**   - Get user full name information
* **localhost:8000/users/meta/\<int:user_id>**       - Get meta information about user

### Test Users

##### GET

* **curl http://127.0.0.1:8000/users/username/1**
* **curl http://127.0.0.1:8000/users/meta/1**
