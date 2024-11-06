# Notes BE

Personal Be for notes-app

[Notes Webapp](https://albertobarrago.github.io/)

```tree
my_fastapi_service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       ├── item.py
│   │   │       └── user.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   └── utils/
│       ├── __init__.py
│       ├── dependency.py
│       └── helper.py
├── tests/
│   ├── __init__.py
│   ├── test_item.py
│   └── test_user.py
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── 1234567890_add_user_table.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```