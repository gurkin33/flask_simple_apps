import json
from app3_migrate_datatables.app import app


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
