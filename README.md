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

PyAcct does not come packaged with a database of its own. Instead, you must configure your database using an environment variable.

After setting up your database dependency, please follow the steps in **Usage** > **Configuration**.

Once completed, you can run the PyAcct layer by navigating to `src/pyacct` and using the following command:

```bash
python uvicorn main:app
```

See the [REST API docs](https://github.com/mwhicks-dev/pyacct/wiki/PyAcct-API-v2) for access information.

## Usage

In this section, we cover the Docker build and deployment of PyAcct.

The usage is broken into five sections: Prerequisites, Configuration, Strategy, Deployment and Extension. Following this is the condensed Docker Usage subsection.

### Prerequisites

PyAcct does not come with a packaged database; instead, it requires a running relational database for you to connect to. Check [here](https://docs.sqlalchemy.org/en/13/dialects/#included-dialects) for a list of databases that are well-defined for SQLAlchemy, and others that have external adapters.

### Configuration
Before running this application, you must first make your own copy of the configuration. Navigate to the `src/pyacct/config/` directory, and make a copy of `config.json.template` titled `config.json`. 

In your text editor of choice, you can now populate the following thre configuration sections:

* `sqlalchemy_url`: Depending on what database and driver you are planning to use, refactor this string in accoradnace with the [Supported Databases](https://docs.sqlalchemy.org/en/20/core/engines.html#supported-databases) and [Database URLs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) sections.
* `origins`: This list should contain all of the address-port combinations you would like to be able to make cross-origin requests to PyAcct. If you are using a web page to access PyAcct's REST API, then you will need to put the address of your web service.
* `attributes`: This list should contain, in the format provided, all of the attributes (except username and password, which are supported natively) that you want PyAcct to track. You can change this between launches of PyAcct, so don't worry. Here is a description of each of these dictionaries' keys for reference:
  * `key`: This is the unique identifier of the attribute -- its name.
  * `required`: Set this to `true` if you want to *require* that new accounts have this attribute, and to `false` if you do not. If you change a previously not required attribute to required between PyAcct launches, old accounts will not be penalized. This should instead be handled by the caller.
  * `sensitive`: Set this to `true` if you don't want for this data to be read by anyone, unless the person owning the attribute is the same person making the request. Set this to `false` if you want for anyone to be able to read this attribute by account ID and key. Sensitive details should not also be unique.
  * `unique`: Set this to `true` if you want for this attribute to be unique - that is, only one person at a time can have a specific key-value combination. Set this to false otherwise. Unique details should not also be sensitive.
* `super`: This list should contain all of the account IDs you would like to be super users (that is, able to query sensitive data through PyAcct). It is a good idea to only allow other services' accounts, a billing service for instance, to be able to retrieve this data; most of the time, sufficiently important users will have database access to sensitive details anyways. The smaller this list is, the better. 

Afterwards, in order to build, execute:

```bash
docker build --no-cache -t pyacct --build-arg TARGET={your-target} --build-arg DRIVER={your-driver} .
```

If not included, the `TARGET` and `DRIVER` build arguments will default to `main` and `psycopg2` respectively.

Building with `--no-cache` is recommended in order to ensure that the appropriate versions are pulled from `git`.

Once successfully built, you can run your Docker image by:

```bash
uvicorn main:app --host 0.0.0.0 --port {host-pyacct-port}
```

If you only want to use PyAcct locally, then instead use `--host 127.0.0.1`.

### Extension

PyAcct has an API endpoint where you can retrieve the account ID from your auth token -- this is the main method of extension. These ID doesn't change unless the account is deleted, so you can use this as a unique ID/weakly-defined foreign key for tables in your own separate applications. See [service-oriented architecture](https://aws.amazon.com/what-is/service-oriented-architecture/).

A detailed outline of the API endpoints this software serves can be found [here](https://github.com/mwhicks-dev/pyacct/wiki/PyAcct-API-v2).

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
