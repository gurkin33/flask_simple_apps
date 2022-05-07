from app1_simple_flask.app import app


def test_user_get():
    with app.test_client() as c:
        response = c.get('/user/1')
        assert response.status_code == 200
        assert response.data == b'{"user": {"id": 1}}\n'


def test_user_get_fail():
    with app.test_client() as c:
        response = c.get('/user')
        assert response.status_code == 400
        assert response.data == b'{"error": ["User ID must be present!"]}\n'


def test_user_post():
    with app.test_client() as c:
        response = c.post('/user')
        assert response.status_code == 200
        assert '{"user": {"id": ' in response.data.decode('utf-8')


def test_user_put():
    with app.test_client() as c:
        response = c.put('/user/2')
        assert response.status_code == 200
        assert response.data == b'{"user": {"id": 2}}\n'


def test_user_put_fail():
    with app.test_client() as c:
        response = c.put('/user')
        assert response.status_code == 400
        assert response.data == b'{"error": ["User ID must be present!"]}\n'


def test_user_delete():
    with app.test_client() as c:
        response = c.delete('/user/3')
        assert response.status_code == 200
        assert response.data == b'{"result": true}\n'


def test_user_delete_fail():
    with app.test_client() as c:
        response = c.delete('/user')
        assert response.status_code == 400
        assert response.data == b'{"error": ["User ID must be present!"]}\n'
