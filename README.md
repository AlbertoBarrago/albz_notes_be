# Notes BE

Personal Be for notes-app

[Notes Webapp](https://albertobarrago.github.io/)

## TODO
 - [ ] Add Logger
 - [ ] Improve Error Handling


## Note for alembic 
 - `alembic init alembic`
 - Import Base and all Models 
 - `alembic revision --autogenerate -m "Create tables from scratch"
 - `alembic upgrade head
`
`


```tree
Base Structure

albz_notes_be/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   ├── core/
│   │   ├── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   └── utils/
│       ├── __init__.py
├── tests/
│   ├── __init__.py
├── .env
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```



work in progress... 
