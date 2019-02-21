web: set FLASK_APP=flaskr
web: flask init-db
web: flask create-admin
web: gunicorn setup:app -b "0.0.0.0:$PORT" -w 3