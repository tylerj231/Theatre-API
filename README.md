## Theatre-API
API service for booking tickets online for various performances in a Theatre.

****

## Installing using GitHub

**Install PostgresSQL and create db**
- git clone https://github.com/tylerj231/Theatre-API.git
- cd Theatre-API
- python -m venv venv
- source venv/bin/activate
- pip install requirements.txt
- SECRET_KEY = your secret key
- DB_PASSWORD = your password
- DB_USER = your db username
- DB_NAME = your db name
- DB_HOST= your db hostname
- python manage.py migrate
- python manage.py runserver

****

## Running API with docker
**Docker should be installed, and db properly configured. (see above)**

- docker-compose build
- docker-compose up
- Create admin user. First: "docker exec -it [container identifier hash] bash" then: "python manage.py createsuperuser"
- To run tests: python manage.py test. (You should be inside the container)

****

## Getting access
****Make sure ModHeader or any other browser extension for authentication is installed****

- create user via api/user/register
- get access token via api/user/token

## Features

- JWT authentication
- Admin panel /admin/
- API documentation is at /api/doc/swagger/
- Create/Update/Delete for all endpoints (Admin only)
- Create/Delete reservation for particular performance (Users)
- Other endpoints only available for view (Users)
- Filtering performances by particular play and/or date.

## Demo
****

## Models diagram

![Models Diagram](/images/db_structure.png)

****

## Screenshots

![Genres](/images/Genre list.png)
![Actors](/images/Actor list.png)
![Tickets](/Images/Tickets List.png)
![Theatre Halls](/images/Theatre Hall List.png)
![Reservations](/images/Reservation List.png)
![Performances](/images/Performance List.png)