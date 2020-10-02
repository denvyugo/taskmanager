# Task manager

Task manager is an API application for manage of personal tasks.
Each task has a set of attributes (fields):
- name - name of task;
- description - description of task;
- created - date and time when task was created;
- status - status of task that may be a one of set: New (value is `NEW`), Planing (`PLN`), Working (`WRK`), Complete (`CMP`);
- plan - date when the task planed to complete.

## API description

There is a user registration required with a pair of parameters: username, password.
The request to api for user registration looks like:

`curl -X POST http://127.0.0.1:8000/auth/users/ --data 'username=user001&password=top!secret'`

`{"email": "", "username": "user001", "id":1}`

For work with API, you should get an authorization token with request:

`curl -X POST http://127.0.0.1:8000/auth/token/login/ --data 'username=user001&password=top!secret'`

`{"auth_token": "i702j9fc7001634641236ac2950269d352zy6572"}`

To get a list of user's tasks you should use a request with token in a header:

`curl -LX GET http://127.0.0.1:8000/api/v1/tasks -H 'Authorization: Token i702j9fc7001634641236ac2950269d352zy6572'`

Log out:

`curl -X POST http://127.0.0.1:8000/auth/token/logout/ -H 'Authorization: Token i702j9fc7001634641236ac2950269d352zy6572'`

You can use filter for fields `status` and `plan`.
For example, for filtering all tasks with status planing the parameter specifying it will be transmitted via GET:

`curl -X GET http://127.0.0.1:8000/api/v1/tasks/?status=PLN -H 'Authorization: Token i702j9fc7001634641236ac2950269d352zy6572'`
