# pyacct

This software is designed to run on Python 3.6. Please install the required dependencies:

```bash
pip install -r requirements.txt
```

You will also need to install the dependencies required by SQLAlchemy for your [dialect](https://docs.sqlalchemy.org/en/13/dialects/) of choice, among those supported.

Necessary environment variables:
* `PYACCT_DATABASE_URL`: Set this to the URL of the database you'd like to connect to. This allows for details of the specific database to be removed from pyacct and left to you.
* `PYACCT_PORT` (Optional): Set this to the port on which you'd like to run the API. If unset, this will default to 8000.

Main FastAPI docs referenced:
* [SQL (Relational) Database](https://fastapi.tiangolo.com/tutorial/sql-databases/)
* [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
* [Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/)
