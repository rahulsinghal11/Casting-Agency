# Casting Agency

## Motivation
The motivation for this project is to create my capstone project for Udacity's Fullstack Nanodegree program. It models a company that is responsible for creating movies and managing and assigning actors to those movies. The assumption is that I am an Executive Producer within the company and wants to create a system to simplify and streamline my process process.
This project covers all the learnt concepts that were covered by the nanodegree which includes data modeling for web using postgres, API development and testing with Flask, Authorization with RBAC, JWT authentication and finally API deployment using Heroku.

## API URL 
- **Localhost:** [base URL] localhost:5000
- **Heroku:** [base URL](https://capstone-casting-agency53.herokuapp.com/)

## Features
- Create and manage ators as well as movies

## Authentication and Authorisation
RBAC using Auth0

#### Roles
- Casting Assistant
- Casting Director
- Executive Producer

## Technologies and Services used
- Python
- Flask
- Flask-Migrate
- Flask-CORS
- Unittest
- SQLAlchemy
- Auth0
- PostgreSQL
- Autopep8

### Dependencies
#### Python 3.7

Follow instructions [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended to work within a virtual environment [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the ptoject directory and running:

```bash
pip install -r requirements.txt
```

#### Environmental Variables
Follow the **.env-sample** to create a .env file for your local setup

### Database Setup
- Create a database
- Generate database tables from the migration files included by executing: 
  `python manage.py db upgrade`
- Add dummy data by executing:
  `python manage.py seed`
  
## Running the Server
From within the project directory first ensure you are working using your created virtual environment.

- To run the **development** server, execute:
`bash setup.sh` then 
`flask run`
- To run the **test**, add fresh token for each of the roles specified above under roles. Then execute:
`bash testing.sh` 


***Note** You can also use `casting-agency-heroku.postman_collection.json` to run tests
***Note** Remember to stop the development server before running the test

## Endpoints
```
# Movies

GET '/movies'
POST '/movies'
PATCH '/movies/<id>'
DELETE '/movies/<id>'

GET '/movies'
- Fetches all movies on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and casting Director
- Required permission (get:movies)
- Response
{
  "movies": [
    {
      "id": 3,
      "release_date": "Thu, 23 Jun 2005 00:00:00 GMT",
      "title": "A fall from Grace"
    },
    {
      "id": 1,
      "release_date": "Thu, 28 Jun 2000 00:00:00 GMT",
      "title": "Jumanji"
    }
  ],
  "success": True
}

POST '/movies'
- Creates a new movie with the provided parameters
- Request Arguments: None
- Allowed users: Casting Director, Executive Producer
- Required permission (add:movies)
- Request Body: {
	"title": "Golden Eye"
	"release_date": "2/25/1984"
}

- Response
{
  "movie": {
    "id": 2,
    "release_date": "Sat, 25 Feb 1984 00:00:00 GMT",
    "title": "Golden Eye"
  },
  "success": true
}


PATCH '/movies/<id>'
- Updates a specific movie with the provided parameters
- Request Arguments: movie_id 
- Allowed users: Executive Producer, Casting Director
- Required permission (edit:movies)
- Request Body: {
	"title": "Ready Player One"
}

- Response
{
  "movie": {
    "id": 4,
    "release_date": "Sun, 11 March 2018 00:00:00 GMT",
    "title": "Ready Player One"
  },
  "success": true
}

DELETE '/movies/<id>'
- Deletes a specific movie
- Request Arguments: movie_id
- Allowed users: Executive Producer
- Required permission (delete:movie)
- Response
{
  "delete": id,
  "success": true
}


# Actors

GET '/actors'
POST '/actors'
PATCH '/actors/<id>'
DELETE '/actors/<id>'

GET '/actors'
- Fetches all actors on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and Casting Director
- Required permission (get:actors)
- Response
{
  "actors": [
    {
      "age": 35,
      "gender": "male",
      "id": 2,
      "name": "Ryan Reynolds"
    },
    {
      "age": 30,
      "gender": "female",
      "id": 4,
      "name": "Jennifer Lawrence"
    }
  ],
  "success": true
}

POST '/actors'
- Creates a new actor with the provided parameters
- Request Arguments: None
- Allowed users: Casting Director and Executive Producer 
- Required permission (add:actors)
- Request Body: {
	"name": "Chriss Pratt",
	"age": 35,
	"gender": "male"
}

- Response
{
  "actor": {
    "age": 35,
    "gender": "male",
    "id": 4,
    "name": "Chriss Pratt"
  },
  "success": true
}


PATCH '/actors/<id>'
- Updates a specific actor with the provided parameters
- Request Arguments: actor_id
- Allowed users: Casting Director and Executive Producer 
- Required permission (edit:actor)
- Request Body: {
	"name": "Chriss Pratt",
}

- Response
{
  "actor": {
    "age": 35,
    "gender": "male",
    "id": 4,
    "name": "Chriss Pratt"
  },
  "success": true
}

DELETE '/actors/<id>'
- Deletes a specific actor
- Request Arguments: actor_id
- Required permission (delete:actors)
- Response
{
  "delete": id,
  "success": true
}

Errors 
The server returns a json object with a description of the type of error.

400 (Bad Request)
  {
    "success": False, 
    "error": 400,
    "message": "bad request, please check your input"
  }

401 (Unauthorised)
  {
    "success": False, 
    "error": 401,
    "message": "authorisation error"
  }

403 (Forbiddden request)
  {
    "success": False, 
    "error": 403,
    "message": "You are not allowed to access this resource"
  }

404 (Resource Not Found)
  {
    "success": False, 
    "error": 404,
    "message": "resource not found"
  }

405 (Method not allowed)
  {
    "success": False, 
    "error": 405,
    "message": "Method not allowed"
  }

422 (Unprocessable entity)
  {
    "success": False, 
    "error": 422,
    "message": "unprocessable"
  }

500 (Internal server error)
  {
    "success": False, 
    "error": 500,
    "message": "Server error
  }
```