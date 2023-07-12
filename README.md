# can_do
ToDo backend app for Cannabis Magazine IL home assignement
It's a backend app, it provides the API for a TODO frontend. Currently, there's no frontend available. You can use Postman 
The main functionality is covered with tests, however, there still could be bugs. The API connects to an SQLite database, since we're currently not planning any sorts of high loads, however, a switch to PostgreSQL can be done easily if needed. This app provides segregated TODO-lists for each user. The authentication is done via a JWT-token (Bearer in headers). There API has endpoint to register new users, receive a token and to refresh it, every other action requires a valid token.

Installation

git clone https://github.com/holohup/can_do.git && cd can_do/backend

1) 
```
docker build . -t can_do && docker run -d -p 8000:8000 --name can_do can_do && docker exec -it -u root $(docker ps -aqf "name=^can_do$") sh ./init.sh
```

Tests

Usage

If you still haven't done so, register a user using the django admin, or the new user registration endpoint: /api/auth/users/
It requires a simple json with username and password.
After that, get a token at /api/auth/jwt/create/ with the credentials you have just provided. Set up your frontend or program to use it (Bearer) and enjoy the API.

Endpoints

- Get a list of your tasks. GET to /api/tasks/
- Create a new todo item. POST to /api/tasks/
- Modify an existing todo item. PATCH to /api/tasks/{task id}
- Get your info (according to the token) - email, username and id: /api/auth/users/me/
- Refresh your token (current TTL is 30 days): /api/auth/jwt/refresh/

Reordering

There's a special endpoint for reordering items. It accepts a simple JSON with a list of id's in them and reorders your tasks in the corresponding order. /api/tasks/reorder/ . The JSON should look like:
```
{
    "new_order": [1, 5, 7, 3, 2]
}```
Where the numbers are task id's and can be found in the task list, or task details.

Fixtures come with a bunch of tasks and two users:
admin / admin (an admin :)


leo / shmleoleo (an ordinary user)


Ways to impove the app:
- Currently, there's no extra endpoint to mark a task as done (you should use patch on the whole item), probably it's a good idea to make one.
- At this moment you cannot delete a task (the method is explicittly prohibited), however, this feature should be very useful for tasks that stop being needed.