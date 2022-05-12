import json

import pytest

from app3_migrate_datatables.app import app
from app3_migrate_datatables.db import ValidationModel


def test__output_serialization():
    assert ValidationModel._output_serialization(2.23) == "2.23"


def test_user_get_404():
    with app.test_client() as c:
        response = c.get('/user/1')
        assert response.status_code == 404
        assert response.data == b'{"error": ["User not found"]}\n'


def test_user_get_fail():
    with app.test_client() as c:
        response = c.get('/user')
        assert response.status_code == 400
        assert response.data == b'{"error": ["User ID must be present!"]}\n'


def test_user_post():
    with app.test_client() as c:
        response = c.post(
            '/user',
            content_type='application/json',
            data=json.dumps(dict(username='test1', email='')))
        assert response.status_code == 200
        print(response.data)
        assert '"id": 1, "username": "test1", "email": ""}}' in response.data.decode("utf-8")


def test_user_post2():
    with app.test_client() as c:
        response = c.post(
            '/user',
            content_type='application/json',
            data=json.dumps(dict(username='test1', email='')))
        assert response.status_code == 400
        print(response.data)
        assert response.data == b'{"validation": {"_unknown_": null, "username": {"notExists": ["Username already ' \
                                b'exists"]}, "email": null}}\n'


def test_user_get():
    with app.test_client() as c:
        response = c.get('/user/1')
        assert response.status_code == 200
        assert '"id": 1, "username": "test1", "email": ""}}' in response.data.decode("utf-8")


def test_user_put():
    with app.test_client() as c:
        response = c.put(
            '/user/1',
            content_type='application/json',
            data=json.dumps(dict(username='test2', email='test2@mail.com')))
        assert response.status_code == 200
        print(response.data)
        assert '"id": 1, "username": "test2", "email": "test2@mail.com"}}' in response.data.decode("utf-8")


def test_user_put_404():
    with app.test_client() as c:
        response = c.put(
            '/user/3',
            content_type='application/json',
            data=json.dumps(dict(username='test2', email='test2@mail.com')))
        assert response.status_code == 404
        assert response.data == b'{"error": ["User not found"]}\n'


def test_user_put_401():
    with app.test_client() as c:
        response = c.put(
            '/user/1',
            content_type='application/json',
            data=json.dumps(dict(username='test 2', email='test2@mail.com')))
        assert response.status_code == 400
        print(response.data)
        assert response.data == b'{"validation": {"_unknown_": null, "username": {"alnum": ["Username must contain ' \
                                b'only letters (a-z) and digits (0-9)"], "noWhitespace": ["Username must not contain ' \
                                b'whitespace"]}, "email": null}}\n'


def test_user_put_fail():
    with app.test_client() as c:
        response = c.put('/user')
        assert response.status_code == 400
        assert response.data == b'{"error": ["User ID must be present!"]}\n'


def test_user_delete():
    with app.test_client() as c:
        response = c.delete('/user/1')
        assert response.status_code == 200
        assert response.data == b'{"result": true}\n'


def test_user_delete_404():
    with app.test_client() as c:
        response = c.delete('/user/3')
        assert response.status_code == 404
        assert response.data == b'{"error": ["User not found"]}\n'


def test_user_delete_fail():
    with app.test_client() as c:
        response = c.delete('/user')
        assert response.status_code == 400
        assert response.data == b'{"error": ["User ID must be present!"]}\n'


@pytest.mark.parametrize('user', [
    {"username": 'test1', "email": 'test1@mail.com'},
    {"username": 'test2', "email": 'test2@mail.com'},
    {"username": 'test3', "email": 'test3@mail.com'},
    {"username": 'test4', "email": 'test4@mail.com'},
    {"username": 'user1', "email": 'user1@mail.com'},
    {"username": 'user2', "email": 'user2@mail.com'},
    {"username": 'user3', "email": 'user3@mail.com'},
    {"username": 'user4', "email": 'user4@mail.com'},
])
def test_user_crowd_post(user):
    with app.test_client() as c:
        response = c.post(
            '/user',
            content_type='application/json',
            data=json.dumps(user))
        assert response.status_code == 200


def test_datatables_post_fail():
    datatables = {}

    with app.test_client() as c:
        response = c.post(
            '/user/table',
            content_type='application/json',
            data=json.dumps(datatables))
        assert response.status_code == 400


def test_datatables_post_search():
    datatables = {
        "draw": 0,
        "start": 1,
        "length": 10,
        "search": {
            "regex": False,
            "value": "user"
        },
        "order": [
            {"column": 0, "dir": "asc"}
        ],
        "column": [
            {
                "data": "id",
                "name": "",
                "searchable": True,
                "orderable": True,
                "search": { "regex": False, "value": "" }
            },
            {
                "data": "username",
                "name": "",
                "searchable": True,
                "orderable": True,
                "search": { "regex": False, "value": "" }
            }
        ]
    }

    with app.test_client() as c:
        response = c.post(
            '/user/table',
            content_type='application/json',
            data=json.dumps(datatables))
        assert response.status_code == 200


def test_datatables_post():
    datatables = {
        "draw": 0,
        "start": 0,
        "length": 10,
        "search": {
            "regex": False,
            "value": ""
        },
        "order": [
            {"column": 0, "dir": "asc"}
        ],
        "column": [
            {
                "data": "id",
                "name": "",
                "searchable": True,
                "orderable": True,
                "search": { "regex": False, "value": "" }
            },
            {
                "data": "username",
                "name": "",
                "searchable": True,
                "orderable": True,
                "search": { "regex": False, "value": "" }
            },
            {
                "data": "created_at",
                "name": "",
                "searchable": True,
                "orderable": True,
                "search": { "regex": False, "value": "" }
            },
            {
                "data": "updated_at",
                "name": "",
                "searchable": True,
                "orderable": True,
                "search": { "regex": False, "value": "" }
            }
        ]
    }

    with app.test_client() as c:
        response = c.post(
            '/user/table',
            content_type='application/json',
            data=json.dumps(datatables))
        assert response.status_code == 200
        print(response.json)
        # assert response.json == {}

    data = response.json["data"]
    for user in data:
        with app.test_client() as c:
            response = c.delete('/user/{}'.format(user["id"]))
            assert response.status_code == 200
