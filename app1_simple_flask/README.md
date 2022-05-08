# Simple flask app ![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white)

### What you can find inside:
- `RouteMaker`, it is helper class, with it all routes will be stored in separate file _routes.py_. It 
will be helpful when project grew and will have many routes.
- CRUD for simple User. All methods will return a dummy data. List of examples you can find in the file 
_app1_simple_flask.postman_collection.json_.

### How to install and run

Download app1_simple_flask directory and run next commands inside:

```bash
# Create virtual environment
virtualenv venv

# Activate virtual environment
source ./venv/bin/activate

# Install dependencies
pip install -r ./requirements.txt

# Run flask app
python3 ./app.py
```

After that you can try to connect to http://127.0.0.1:8080/user/1. Successful result:
```json
{
    "user": {
        "id": 1
    }
}
```

More examples you can find in _app1_simple_flask.postman_collection.json_, please import this file 
to Postman.

### Configuration file

Inside of config.py file you can find settings related to:

- API port (by default, 8080)
- API host, which ip address can get API requests (by default, it is 0.0.0.0 or any ip address) 