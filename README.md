# Flask RESTful auth API

A simple auth RESTful API built with Flask

## Usage

_Note that pipenv package was used to create virtual environment._
_pipenv package can be installed using: `pip install pipenv` ._

1. Clone this repository

2. cd into _flask-rest_

3. Run `pipenv shell`

4. Run `pip install -r requirements.txt`

5. `python run.py`

## Available routes

1. **/register**

-- This route requires JSON payload.
-- The payload contains user registration data
-- Methods allowed: `POST`
-- Sample JSON payload:
`{ "name": "Test", "email": "test@example.com", "password": "secret" }`

2. **/login**

-- This route requires JSON payload.
-- The payload contains user login data
-- Methods allowed: `POST`
-- Sample JSON payload:
`{ "email": "test@example.com", "password": "secret" }`
-- JWT access token that expires in 30 minutes will be returned.

All protected routes can be accessed using the JWT by specifying `x-access-token` in the request header.
