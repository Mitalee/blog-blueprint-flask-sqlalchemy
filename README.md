IMPORTANT: 
Login/Admin related modules deliberately not implemented, and the blueprint can be modified for Flask-Login or Admin based fixtures.
## Instructions
* Clone the repository and cd into blog-blueprint-flask-sqlalchemy

* Run ```docker-compose up -d --build```

* Run the required migrations ```docker-compose exec website alembic upgrade head```

* Now navigate to ```http://localhost:8000``` in the browser to test it out.

## *Optional*
* Build a model (Posts, Tags, Comments)

* After adding the model, autogenerate a migration ```sudo docker-compose exec --user "$(id -u):$(id -g)" website alembic revision --autogenerate -m "create foo table"```

* Finally, Get to alembic head after autogenerating a revision or to create db ```sudo docker-compose exec website alembic upgrade head```

* Check database migrations by running ```docker-compose exec website alembic current```
