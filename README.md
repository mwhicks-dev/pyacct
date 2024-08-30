# PyAcct

PyAcct is a lightweight software layer that provides an account and session management system with a service-oriented architecture. Data exchange is performed via REST API for the sake of integration with other high-level programming languages.

## Table of Contents

* [Introduction](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#introduction)
* [Installation](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#installation)
* [Quick start](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#quick-start)
* [Usage](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#usage)
* [Known issues and limitations](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#known-issues-and-limitations)
* [Getting help](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#getting-help)
* [Contributing](https://github.com/mwhicks-dev/pyacct/tree/dev?tab=readme-ov-file#contributing)
* [License](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#license)
* [Acknowledgements](https://github.com/mwhicks-dev/pyacct/?tab=readme-ov-file#acknowledgements)

## Introduction

Very often, an account system is needed for modern software projects and web solutions. PyAcct is an effort to, like other similar software, modularize this protocol so that it is repeatable and available. 

I implemented this small back-end utility to provide a flexible, RESTful method of account management and authentication, with the goal of allowing for users to extend upon it freely; given the correct authentication, PyAcct allows for an account's unique integer ID and username to be retrieved so that they can be used in (more or less) join tables, although not so strongly connected. 

The important part is that if you want to associate more data to an account, like an email or profile picture, you can use the same account ID.

## Installation

PyAcct was developed in Python 3.12, but is designed to run on Python 3.6 or above. Following, there are two steps for installation. First, install the basic requirements:

```bash
pip install -r requirements.txt
```

and then, install the driver required by SQLAlchemy for your [dialect](https://docs.sqlalchemy.org/en/13/dialects/) of choice. **This part is important -- SQLAlchemy cannot connect to your database without these being implemented.**

Docker deployment options available in Usage.

### Build to Package

If you only want to build PyAcct to a package for use in other sofware, just install `setuptools` and run `python -m build`.

## Quick start

PyAcct does not come packaged with a database of its own. Instead, you must configure your database using an environment variable. Before running, please assign `PYACCT_DATABASE_URL` in the form:

```
dialect+driver://username:password@host:port/database
```

That is:

```bash
export PYACCT_DATABASE_URL="dialect+driver://username:password@host:port/database"
```

Once completed, you can run the PyAcct layer using the following command:

```bash
python src/pyacct/main.py
```

See the [REST API docs](https://github.com/mwhicks-dev/pyacct/wiki/PyAcct-API-v1) for access information.

## Usage

The usage is broken into five sections: Prerequisites, Environment Variables, Strategy, Deployment and Extension. Following this is the condensed Docker Usage subsection.

### Prerequisites

PyAcct does not come with a packaged database; instead, it requires a running relational database for you to connect to. Check [here](https://docs.sqlalchemy.org/en/13/dialects/#included-dialects) for a list of databases that are well-defined for SQLAlchemy, and others that have external adapters.

### Environment Variables

PyAcct is designed to be configured once and then run as many times as you need it to be, taking advantage of environment variables to do so. Only the `PYACCT_DATABASE_URL` environment variable is required. The other ones can be set if desired, but have defaults in place.

#### `PYACCT_DATABASE_URL`

This environment variable is required to run PyAcct. As the layer does not come with a packaged databse, you must instead configure it to connect to an external (relational) database.

The variable should be assigned the a value specified by SQLAlchemy's [Database URLs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) format -- that is, 

```
dialect+driver://username:password@host:port/database
```

You can find your `dialect` by selecting your database from the options [here](https://docs.sqlalchemy.org/en/13/dialects/). Once you select your database of choice, the URL will read `https://docs.sqlalchemy.org/en/13/dialects/{dialect}.html`.

The `driver` will be whatever database driver you have downloaded among those listed in the DBAPI Support section of `https://docs.sqlalchemy.org/en/13/dialects/{dialect}.html`. One of them is required.

#### `PYACCT_PORT`

This environment variable allows you to specify on what port of the running machine you would like to host the PyAcct REST API. If unset, this will default to `8000`. [Here](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) is a resource you can use to check what ports are available or not.

Necessary environment variables:
* `PYACCT_DATABASE_URL`: Set this to the URL of the database you'd like to connect to. This allows for details of the specific database to be removed from pyacct and left to you.
* `PYACCT_PORT` (Optional): Set this to the port on which you'd like to run the API. If unset, this will default to 8000.

### Strategy

[This file](https://github.com/mwhicks-dev/pyacct/blob/main/util/token_validation.py) contains an interface for token validation, which by default, is implemented by [this file](https://github.com/mwhicks-dev/pyacct/blob/main/pyacct_token_validator.py). If you want to change how token validation works, you should write your own implementation in the top-level directory and have the [main script](https://github.com/mwhicks-dev/pyacct/blob/main/main.py) set `persistence.session.token_validation` to an instance of it instead of to my default one.

The default validator will deem tokens invalid after they have been unused for an hour, or after they have existed for a day.

### Deployment

Once all of the prerequisites and configuration are satisfied, you can simply run PyAcct with the following command:

```bash
python src/pyacct/main.py
```

### Extension

PyAcct has an API endpoint where you can retrieve the account ID from your auth token -- this is the main method of extension. These ID doesn't change unless the account is deleted, so you can use this as a unique ID/weakly-defined foreign key for tables in your own separate applications. See [service-oriented architecture](https://aws.amazon.com/what-is/service-oriented-architecture/).

A detailed outline of the API endpoints this software serves can be found [here](https://github.com/mwhicks-dev/pyacct/wiki/PyAcct-API-v1).

### Docker Usage

If you are not yet familiar with anything covered, please read the above subsections before this one.

You can use the Dockerfile to build and run this service. Before building, you will need to verify or modify the following arguments:
* `TARGET`: This will be the branch (or tag) you would like to build to your Docker image (for instance, v1.1.1 or dev). If not modified, this argument defaults to `main`.
* `DRIVER`: This will be the installed SQLAlchemy driver for your database type. If not modified, this argument defaults to `psycopg2`.

Afterwards, in order to build, execute:

```bash
docker build --no-cache -t pyacct --build-arg TARGET={your-target} --build-arg DRIVER={your-driver} .
```

or

```bash
docker build --no-cache -t pyacct .
```

Use of the `--no-cache` flag is recommended for non-release branches, as Docker will not consider that its fetch of `pyacct` may change over time.

Once successfully built, you can run your Docker image by:

```bash
docker run --rm -v /$(pwd)/src/pyacct/config/:/pyacct/src/pyacct/config/ -p {host-pyacct-port}:8000 pyacct
```

You can detach this process using `-d` if you would like, but testing first without is recommended. If successful, you should be able to access PyAcct via `localhost:{host-pyacct-port}` or remotely through your public IP address `hostaddr` and the port. Try `localhost:{host-pyacct-port}/docs` (or `hostaddr`) to test.

## Known issues and limitations

The biggest problem from a practical standpoint is a lack of unit tests. I really despise FastAPI testing in particular, so I have neglected to do it.

PyAcct is designed for HTTPS, as implementing end-to-end encryption from scratch was not the goal of this software. If you are not planning to access the API from HTTPS, *use caution*.

To reduce bottleneck, sessions are pruned only when one is used to make an authenticated request. This could theoretically cause some clogging, but should be fine.

Async programming isn't used yet even though it is supported by FastAPI. This will change if ever necessary.

## Getting help

Fill out an [issue](https://github.com/mwhicks-dev/pyacct/issues) if you're having trouble. If necessary, I will pin both an FAQ and a bug reporting standard there, but if neither of them are there, go ahead and just submit your problem the best you know how. I'll get back to you with a fix or if I need more info from you.

## Contributing

Feel free to fork PyAcct if you want to add or fix something.

## License

No license. Use, fork, and abuse as much as you want. If you just want to add a new table or column or something, knock yourself out, but I would encourage you to read this [article on service-oriented architecture](https://aws.amazon.com/what-is/service-oriented-architecture/), which is the overarching pattern with which PyAcct has been designed. You should just make your own services, and have your tables share the ID of the underlying account where necessary.

I'm not a cybersecurity expert, so **you are warned that there may be security flaws in PyAcct that could harm the data of yourself and others; I am not responsible nor liable for any harm or loss that come as a result.**

## Acknowledgements

Sources include (but are not limited to) the following:
* [SQL (Relational) Database](https://fastapi.tiangolo.com/tutorial/sql-databases/)
* [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
* [Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/)

Anything else that I referenced something specific besides Python STL has a ref in the source code.
