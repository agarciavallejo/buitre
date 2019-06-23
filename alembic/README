Generic single-database configuration.

# CREATE AN ALEMBIC MIGRAION

see: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script

to create an alembic migration:

`$ [pipenv run] alembic revision -m "<descriptive message>"`

a file will be created with an identifier hash and the message. Use the `upgrade()` and `downgrade()`
methods to do and undo the changes. Then run this command to apply the migration:

`$ [pipenv run] alembic upgrade head`