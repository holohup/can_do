## Can Do
### ToDo backend app for Cannabis Magazine IL, a home assignement

It's a backend app, it provides the API for a TODO frontend. Currently, there's no frontend available. You can use **Postman** or any other program of your choice. It's developed using the TDD methodology, therefore the main functionality is covered with tests, however, there still could be bugs. The API connects to an SQLite database, since we're currently not planning any sorts of high loads, however, a switch to PostgreSQL can be done easily if needed. This app provides segregated TODO-lists for each user. The authentication is done via a JWT-token (Bearer in headers). There API has endpoint to register new users, receive a token and to refresh it, every other action requires a valid token.

### Installation

There're *three ways* to get to know this project better.

#### 1) Take a look

It's latest version is already running on an AWS server by the URL http://ondeletecascade.ru:8000/api/ and every action can be performed there. The instance will keep running for some time, but no guarantees on how long it will last.

You can also copy the project and run it on your PC or server:

```
git clone https://github.com/holohup/can_do.git && cd can_do/backend
```
After that, there're two options:

#### 2) Run in a Docker container

```
docker build . -t can_do && docker run -d -p 8000:8000 --name can_do can_do && docker exec -it -u root $(docker ps -aqf "name=^can_do$") sh ./init.sh
```

These commands build a Docker image, run it, apply migrations, collect static files and preload fixtures for the project to become more substantial right away.

#### 3) Set up a Python virtual environment and launch the test server.

```
python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata fixtures/initial.json && cp .env.sample .env && python manage.py runserver
```

> *If you don't want the fixtures to be preloaded, skip the **loaddata** command. Then you would need to create an admin*:

```
python manage.py createsuperuser
```

**That's it!** After either step, the **Can Do API** will become available by the address http://127.0.0.1:8000/api/. From here and on, the API links will be provided to this address, however, feel free to use the *ondeletecascade*.ru version.

### Usage

The Django admin panel is located at http://127.0.0.1:8000/admin/. The preloaded fixtures provide two already registered users:

**admin** / **admin** (an admin :)
**leo** / **shmleoleo** (an ordinary user)

If you have skipped the fixture preloading, create and admin and a user of your choice using the django admin, or the new user registration endpoint: http://127.0.0.1:8000/api/auth/users/. It requires a simple JSON:
```json
{
    "username": "alexey",
    "password": "shmalexei"
}
```
If everything went **OK** and the password was not too short and didn't look at all like the username, you'll get the user registration confirmation:
```json
{
    "email": "",
    "username": "alexey",
    "id": 3
}
```
You would also need a JWT Token. Send the same username/password JSON combo POST request to http://127.0.0.1:8000/api/auth/jwt/create/ and you'll receive a response that looks similar to:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTMxNzczNCwiaWF0IjoxNjg5MjMxMzM0LCJqdGkiOiI4ZDVmYTAxZTc3OGI0Yjc1YmYxYjY3MjMwYzZlMTEzZiIsInVzZXJfaWQiOjN9.eFH82eZvzNtbBUpKaXAoXltdFb3w_jOcVdU7U3rXbhc",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxODIzMzM0LCJpYXQiOjE2ODkyMzEzMzQsImp0aSI6IjczMzkwOTJhZDdlNDRmYWY5ZDczYzRjZWJmZGMwN2EzIiwidXNlcl9pZCI6M30.koJbtDboe8fQsqQNgY_LyHZsi4fqJ2cWdwRHBvAu2Us"
}
```
Now copy the "access" key to your favorite program (I use **Postman** and highly recommend it) to use it (**Bearer** in the headers) and enjoy the API.


### Endpoints

#### Create a new todo item

POST to http://127.0.0.1:8000/api/tasks/
```json
{
    "title": "Feed the dog",
    "description": "He likes chicken sausages",
    "done": false
}
```
Only the title field is required, but you can provide extra details in the other fields if you want. The response will contain the new task id.

#### Modify an existing todo item.

Use the id from the previous step to modify any of the fields, send a PATCH request with modified JSON from the previous step to http://127.0.0.1:8000/api/tasks/{task_id}

#### Get a list of your tasks.

Since you're authorized using the JWT token, you can get a list of your tasks. Send a GET request to http://127.0.0.1:8000/api/tasks/

You can also get all of your task id's from that list.

#### Get your user info.

Simple information about the authorized user (according to the token) - email, username and id.
Send a GET request to http://127.0.0.1:8000/api/auth/users/me/

#### Refresh your token

The current token TTL is set to 30 days. If you ever feel the need to refresh it, you need to send a POST request with JSON that looks like this:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTMxNzczNCwiaWF0IjoxNjg5MjMxMzM0LCJqdGkiOiI4ZDVmYTAxZTc3OGI0Yjc1YmYxYjY3MjMwYzZlMTEzZiIsInVzZXJfaWQiOjN9.eFH82eZvzNtbBUpKaXAoXltdFb3w_jOcVdU7U3rXbhc"
}
```
Where "refresh" is the key you received when aquired the token. The endpoint is: http://127.0.0.1:8000/api/auth/jwt/refresh/

Then you would need to use the new token provided by the system.


#### Reordering

Here comes the tricky part. There's a special endpoint for reordering items. It accepts a simple JSON with a list of id's in the new order, and reorders the todo tasks accordingly. Let's say you've got task id's **1, 2 and 3** (you can get those from the task list endpoint). If you reorder them, once you get a new task list, they'll come in the new order. To reorder, send PATCH request to http://127.0.0.1:8000/api/tasks/reorder/ containing a simple JSON:


```json
{
"new_order": [3, 1, 2]
}
```
The response either provides the new order, or reports of an error (e.g. you tried to include other user's post, or didn't include some of your posts in the new order)

```json
{
    "new_order": [
        3,
        1,
        2,
    ]
}
```

### Final words

#### Tests

Launch the command

```
pytest
```
from the backend directory.

#### Ways to impove the app:

- Currently, there's no extra endpoint to mark a task as done (you should use patch on the whole item), probably it's a good idea to make one.
- At this moment you cannot delete a task (the method is explicittly prohibited), however, this feature should be very useful for tasks that stop being needed.
- Switch to a more sequire way to acquire tokens, this would need an approval from a frontend guys!
- Pagination / filtering to the tasks lists once their number grows.
