
  
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

  

After that, there're two options

  

#### 2) Run in a Docker container

  

```

  

docker build . -t can_do && docker run -d -p 8000:8000 --name can_do can_do && docker exec -it -u root $(docker ps -aqf "name=^can_do$") sh ./init.sh

  

```

These commands build a Docker image, run it, apply migrations, collect static files and preload fixtures for the project to become more substantial right away.

  

#### 3) Set up a Python virtual environment and launch the test server.

  

```

python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata fixtures/initial.json && python manage.py runserver

```

> *If you don't want the fixtures to be preloaded, skip the **loaddata** command. Then you would need to create an admin*:

```

python manage.py createsuperuser

```

**That's it!** After either step, the **Can Do API** will become available by the address http://127.0.0.1:8000/api/. From here and on, the API links will be provided to this address.


### Usage

The preloaded fixtures provide two already registered users:

**admin** / **admin** (an admin :)
**leo** / **shmleoleo** (an ordinary user)

If you have skipped the fixture preloading, create and admin and a user of your choice using the django admin, or the new user registration endpoint: http://127.0.0.1:8000/api/auth/users/. It requires a simple JSON:
```json
{
    "username": "alexey",
    "password": "shmalexei"
}
```
If everythin went ok and the password was not too short and didn't look at all like the username, you'll get the user registration confirmation:
```json
{
    "email": "",
    "username": "alexey",
    "id": 3
}
```
  

It requires a simple json with username and password.

  

After that, get a token at /api/auth/jwt/create/ with the credentials you have just provided. Set up your frontend or program to use it (Bearer) and enjoy the API.

  

  

Endpoints

  

  

- Get a list of your tasks. GET to /api/tasks/

  

- Create a new todo item. POST to /api/tasks/

  

- Modify an existing todo item. PATCH to /api/tasks/{task id}

  

- Get your info (according to the token) - email, username and id: /api/auth/users/me/

  

- Refresh your token (current TTL is 30 days): /api/auth/jwt/refresh/

  

  

#### Reordering

  

There's a special endpoint for reordering items. It accepts a simple JSON with a list of id's in them and reorders your tasks in the corresponding order. /api/tasks/reorder/ . The JSON should look like:

  

```json

  

{

"new_order": [1, 5, 7, 3, 2]

}

```

  

Where the numbers are task id's and can be found in the task list, or task details.

  

Fixtures come with a bunch of tasks and two users:

  




  

  

Final words

  

  

Tests

  

  

Launch the command

  

```

  

pytest

  

```

  

from the backend directory.

  
  

Ways to impove the app:

  

- Currently, there's no extra endpoint to mark a task as done (you should use patch on the whole item), probably it's a good idea to make one.

  

- At this moment you cannot delete a task (the method is explicittly prohibited), however, this feature should be very useful for tasks that stop being needed.

  

- Switch to a more sequire way to acquire tokens, this would need an approval from a frontend guys!