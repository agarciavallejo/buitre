## Dependencies

Flask app uses the following python libs:

* `flask_cors`
* `sqlalchemy`
* `marshmallow`
* `psycopg2`
* `graphene`
* `graphene-sqlalchemy`

## POSTGRESQL

1. Install:
`sudo apt install postgresql postgresql-contrib`

2. Instanciate postgres user
`sudo -u postgres -i`

3. Create app user & buitre database
`CREATE USER app WITH PASSWORD '1234';`
`CREATE DATABASE buitre OWNER app;`

4. Run Alembic Migrations
`alembic upgrade 47ef3050097f #initial migration`
@TODO: find a way to "upgrade to the whole migrations collection"

## RUN FLASK APP

`export FLASK_APP=buitre.py`
`flask run`
browse `127.0.0.1:5000`

## DOCKER	

Run single flask app container (no DB)

1. Build the image
`docker build -t buitre_img .`

2. Check image is created
`docker images`

3. Run the container
`docker run -d -p 80:80 --name buitre_ctn buitre_image`

4. Check container is running
`docker ps -a`

