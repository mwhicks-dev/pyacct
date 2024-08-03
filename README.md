# pyacct

Please install the required dependencies:

```bash
pip install -r requirements.txt
```

You will also need to install the dependencies required by SQLAlchemy for your [dialect](https://docs.sqlalchemy.org/en/13/dialects/) of choice, among those supported.

Necessary environment variables:
* `PYACCT_DATABASE_URL`: Set this to the URL of the database you'd like to connect to. This allows for details of the specific database to be removed from pyacct and left to you.

Main docs references:
* [FastAPI relationship basics](https://fastapi.tiangolo.com/tutorial/sql-databases/)
* [Seperable APIs](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
