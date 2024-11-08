# Notes BE

Personal Be for notes-app

[Notes Webapp](https://albertobarrago.github.io/)

## TODO
 - [x] Add Logger
 - [x] Improve Error Handling
 - [x] Audit action notes and auth 
 - [x] Check import
 - [ ] Add home API for Welcome localhost:/ 


## Note for alembic 
 - `alembic init alembic`
 - Import Base and all Models inside `env.py`
 - `alembic revision --autogenerate -m "Create tables from scratch"`
 - `alembic upgrade head`

## Tree

```tree
app/
├── __init__.py
├── api
│   ├── __init__.py
│   └── v1
│       ├── __init__.py
│       └── endpoints
│           ├── __init__.py
│           ├── auth.py
│           └── note.py
├── core
│   ├── __init__.py
│   ├── access_token.py
│   └── config.py
├── db
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── audit_logs.py
│   │   ├── base.py
│   │   ├── notes.py
│   │   └── users.py
│   └── session.py
├── main.py
├── schemas
│   ├── __init__.py
│   ├── auth.py
│   ├── note.py
│   └── user.py
└── utils
    ├── __init__.py
    ├── audit_utils.py
    └── dependency.py

```



work in progress... 
