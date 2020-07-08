IMPORTANT: 
Login/Admin related modules deliberately not implemented, and the blueprint can be modified for Flask-Login or Admin based fixtures.
## Instructions
* Run ```docker-compose up --build``` and navigate to ```http://localhost:8000``` in the browser to test it out.

* To Initialize alembic run ```docker-compose exec --user "$(id -u):$(id -g)" website alembic init blogexample/migrations```

* In alembic.ini change ```script_location``` to {flask_appname}/migrations comment out sqlalchemy.url(default is 'blogexample')

* In env.py import os, sys,  and (create_app and db(from app.py))
set up sqlalchemy url here

## *Optional*

 * Build a model (Posts, Tags, Comments)
 * After adding the model, autogenerate a migration ```sudo docker-compose exec --user "$(id -u):$(id -g)" website alembic revision --autogenerate -m "create foo table"```

Finally, Get to alembic head after autogenerating a revision or to create db ```sudo docker-compose exec website alembic upgrade head```


NOTE:
Anyone trying it in windows OS
After initalize alembic we need to edit  env.py  in migration folder 
It fails saying 
"sqlalchmey.exc.NoSuchModuleNameError:can't load Plugins:sqlalchemy.dialects:driver"

