# Flask Migration and Datatables support 

![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white&style=for-the-badge)
<img style="background-color:#ccc; padding: 4px" src="https://quintagroup.com/cms/python/images/sqlalchemy-logo.png/@@images/image.png" alt="isolated" width="100"/>

### What you can find inside:
- `RouteMaker`, it is helper class, all routes will be stored in separate file _routes.py_. It 
will be helpful when project grew and will have many routes.
- User model. It will work with database it can find user by ID and return, update, save, delete user data. 
Also, I added validation inside this model.
- All Users will have columns created_at, updated_at. Column updated_at updates on save action.
- Validation. It is based on [respect_validation](https://github.com/gurkin33/respect_validation). 
`FormValidator` added to Model class via child, you can find it in db.py.
- Database can be created via Flask-Migrate library (commands below).
- CRUD for simple User. All methods will return an actual data from database. List of examples you can find in the file 
_app3_migration_datatables.json_.
- 

### How to install and run

Download app3_migrate_datatables directory and run next commands inside:

```bash
# Create virtual environment
virtualenv venv

# Activate virtual environment
source ./venv/bin/activate

# Install dependencies
pip install -r ./requirements.txt

# delete init file, it was required for github actions
rm -f __init__.py

# init migrate config
flask db init
# check current app and create migrate scripts
flask db migrate -m "Initial database of this app"
# create database/apply created script
flask db upgrade

# Run flask app
python3 ./app.py
```
After that you can try to connect to http://127.0.0.1:8080/user/1. Successful result:
```json
{
    "error": [
        "User not found"
    ]
}
```

More examples you can find in _app3_migrate_datatables_, please import this file 
to Postman.

### Configuration file

Inside of config.py file you can find settings related to:

- API port (by default, 8080)
- API host, which ip address can get API requests (by default, it is 0.0.0.0 or any ip address) 
- Database link. If you want to connect to real database engine like PostgreSQL, MySQL and so on, 
please change this parameter (by default, it is a link to sqlite).
