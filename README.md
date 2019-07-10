

Run ```docker-compose up --build``` and navigate to ```localhost:5000``` in the browser to test it out.

Initialize alembic
```docker-compose exec --user "$(id -u):$(id -g)" website alembic init alembic```

In alembic.ini
change ```script_location``` to {flask_appname}/migrations
comment out sqlalchemy.url

In env.py
import os, sys,  and (create_app and db(from app.py))
set up sqlalchem url here

Build a model

Run a migration
```docker-compose exec --user "$(id -u):$(id -g)" website alembic revision -m "create foo table"```
it should be written out to migrations/versions folder with the template used from script.mako

autogenerate a migration
```docker-compose exec --user "$(id -u):$(id -g)" website alembic revision --autogenerate -m "create foo table"```

Get to alembic head after autogenerating a revision
```docker-compose exec website alembic upgrade head```