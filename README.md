IMPORTANT: 
Login/Admin related modules deliberately not implemented, and the blueprint can be modified for Flask-Login or Admin based fixtures.

Run ```docker-compose up --build``` and navigate to ```http://localhost:5000``` in the browser to test it out.

Initialize alembic
```docker-compose exec --user "$(id -u):$(id -g)" website alembic init alembic```

In alembic.ini
change ```script_location``` to {flask_appname}/migrations
comment out sqlalchemy.url

In env.py
import os, sys,  and (create_app and db(from app.py))
set up sqlalchemy url here

Build a model (Posts, Tags, Comments)

Run a migration
```docker-compose exec --user "$(id -u):$(id -g)" website alembic revision -m "create foo table"```
it should be written out to migrations/versions folder with the template used from script.mako

autogenerate a migration
```docker-compose exec --user "$(id -u):$(id -g)" website alembic revision --autogenerate -m "create foo table"```

Get to alembic head after autogenerating a revision
```docker-compose exec website alembic upgrade head```