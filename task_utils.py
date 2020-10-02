"""
work with taskmanager API
version 1
"""

from datetime import datetime as dt
from datetools import convert_datetime, local_datetime_string
import requests
from requests.exceptions import HTTPError


BASE_URL = 'http://127.0.0.1:8000/api/'

URLS = {'tasks' : 'v1/tasks/'}


class Task:
    """class for user's task"""
    def __init__(self, user, name=''):
        self._id = 0
        self._user = user
        self.name = name
        self.description = ''
        self._created = None
        self.status = ''
        self.plan = None

    def __str__(self):
        return f'Task: {self._id}, {self._user}'

    def __repr__(self):
        return f'<Task object: Task.id = {self._id}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_number):
        if isinstance(id_number, int):
            if id_number > 0:
                self._id = id_number
        else:
            raise TypeError(
                "the agrument 'id_number' should be positive integer")

    @property
    def created(self):
        return self._created
    
    def load_data(self, data):
        self._user._load_task_data(self, data)


class User:
    """user class for working with task manager"""
    def __init__(self):
        self._id = 0
        self._username = ''
        self._tasks = {}
        self._token = None

    def loging(self, username, password):
        """get token"""
        url = BASE_URL + 'auth/token/login/'
        self._username = username
        data = {
            'username': self._username,
            'password': password,
            }
        reply = self._get_data_post(url, data)
        if reply:
            self._token = reply['auth_token']
            return self._token

    def logout(self):
        """user logout"""
        url = BASE_URL + 'auth/token/logout/'
        self._get_data_post(url)
        self._token = None
        return self._token

    def register(self, username, password):
        """register new user."""
        url = BASE_URL + 'auth/users/'
        self._username = username
        data = {
            'username': self._username,
            'password': password
            }
        reply = self._get_data_post(url, data)
        if reply:
            self._id = int(reply['id'])
            return self._id
    
    @property
    def id(self):
        return self._id
    
    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token_value):
        self._token = token_value

    def number_tasks(self):
        return len(self._tasks)

    def _load_task_data(self, task, data):
        """load data into task object"""
        task.id = data['id']
        task.name = data['name']
        task._created = data['created']
        task.description = data['description']
        task.status = data['status']
        task.plan = data['plan']

    def _task_data(self, task):
        data = {'name': task.name}
        if task.description:
            data['description'] = task.description
        if task.status:
            data['status'] = task.status
        if task.plan:
            data['plan'] = dt.strftime(task.plan, '%Y-%m-%d')
        return data
    
    def _add_task(self, url, task):
        """add task to API"""
        data = self._task_data(task)
        reply = self._get_data_post(url, data)
        if reply:
            task.load_data(reply)
            return task

    def _get_task(self, url):
        """get a one task by url."""
        response = self._get_data_get(url)
        if response:
            reply = response.json()
            task_object = Task(self)
            task_object.load_data(reply)
            self._tasks[task_object.id] = task_object
            return task_object

    def get_tasks(self):
        """get a tasks list"""
        url = BASE_URL + URLS['tasks']
        response = self._get_data_get(url)
        reply = response.json()
        if reply:
            for data in reply:
                task = Task(self)
                task.load_data(data)
                self._tasks[task.id] = task

    def task_by_id(self, task_id):
        """get task by id from self package tasks"""
        if not task_id in self._tasks:
            url = f"{BASE_URL}{URLS['tasks']}{task_id}/"
            self._get_task(url)
        return self._tasks[task_id]

    def add_task(self, task):
        """add new task"""
        url = BASE_URL + URLS['tasks']
        if isinstance(task, Task):
            pass
        elif isinstance(task, str):
            task = Task(self, task)
        else:
            return None
        task = self._add_task(url, task)
        if task:
            self._tasks[task.id] = task
            return task

    def save_task(self, task):
        """save task to API"""
        url = f"{BASE_URL}{URLS['tasks']}{task.id}/"
        data = self._task_data(task)
        #data = {'status': task.status}
        reply = self._get_data_put(url, data)
        if reply:
            return task
    
    def get_tasks_status(self, status='NEW'):
        """get lists of tasks with provided status"""
        url = f"{BASE_URL}{URLS['tasks']}"
        params = {'status': status}
        response = self._get_data_get(url, params)
        reply = response.json()
        if reply:
            tasks = []
            for data in reply:
                task = Task(self)
                task.load_data(data)
                tasks.append(task)
            return tasks
    
    # working with API
    def _get_data_post(self, url, data=None):
        try:
            if self._token:
                auth_header = {'Authorization': f'Token {self._token}'}
                if data:
                    response = requests.post(url, data=data, headers=auth_header)
                else:
                    response = requests.post(url, headers=auth_header)
            else:
                response = requests.post(url, data=data)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred {http_err}')
        except Exception as err:
            print(f'Unexpected error occurred {err}')
        else:
            if response.status_code != 204:
                return response.json()

    def _get_data_patch(self, url, data):
        try:
            if self._token:
                auth_header = {'Authorization': f'Token {self._token}'}
                response = requests.patch(url, data=data, headers=auth_header)
            else:
                response = requests.patch(url, data=data)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred {http_err}')
        except Exception as err:
            print(f'Unexpected error occurred {err}')
        else:
            return response.json()

    def _get_data_put(self, url, data):
        try:
            if self._token:
                auth_header = {'Authorization': f'Token {self._token}'}
                response = requests.put(url, data=data, headers=auth_header)
            else:
                response = requests.put(url, data=data)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred {http_err}')
        except Exception as err:
            print(f'Unexpected error occurred {err}')
        else:
            return response.json()

    def _get_data_get(self, url, param=None):
        if self._token:
            auth_header = {'Authorization': f'Token {self._token}'}
            try:
                if param:
                    response = requests.get(
                        url, headers=auth_header, params=param
                        )
                else:
                    response = requests.get(
                        url, headers=auth_header
                        )
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred {http_err}')
            except Exception as err:
                print(f'Unexpected error occurred {err}')
            else:
                return response
