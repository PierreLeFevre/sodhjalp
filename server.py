import sys

from flaskr import create_app

app = create_app()

app.run(port = sys.argv[1])