# Library Management System
This is a bare-bone rest api for Library Management System written in Django Rest API which uses role based access policy.
It Supports jwt token based authentication. User can browse books details and request for a Book Loan.

Tested `Python3.9`

## Installation
`- pip install -r requirements.txt`\
`- python manage.py makemigrations && python mange.py migrate`

Create a superuser with the command

`- python manage.py createsuperuser`

Run the server

`- python manage.py runserver`

## Test
`- python manage.py test`