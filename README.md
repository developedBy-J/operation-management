# coops
Consulting Operations System

## Prerequisites

1. Python 3.8+
2. Python pipenv
   - [installation instructions](https://github.com/pypa/pipenv)
   - tl;dr: `pip3 install pipenv`
   
## Building

To build the project, do the following

```sh
pipenv install
```

## Running

#### Using pipenv

To open and activate the virtual environment

```sh
pipenv shell
```
To create database migration files
```sh
python manage.py makemigrations
```
To create tables in database
```sh
python manage.py migrate
```
To create document types like Personal, Formal, Official, etc
```sh
python manage.py create_doctype
```
To create user groups
```sh
python manage.py create_groups
```
   
   
   
