## Dependencies

Flask app uses the following python libs:

* `flask_cors`
* `sqlalchemy`
* `marshmallow`
* `psycopg2`
* `graphene`
* `graphene-sqlalchemy`

## DOCKER	

Run single flask app container (no DB)

1. Build the image
`docker build -t buitre_img .`

2. Check image is created
`docker images`

3. Run the container
`docker run -d -p 80:80 --name buitre_ctn buitre_image`

4. Check container is running
`docker ps`

