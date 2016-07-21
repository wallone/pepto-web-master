
# web/__init__.py

from flask import Flask
from flask_bootstrap import Bootstrap

# Apps
from .labeler import labeler
from .twsurvey import twsurvey


app = Flask(__name__)
Bootstrap(app)

print("\tFlask name {}".format(__name__))
app.register_blueprint(labeler)
app.register_blueprint(twsurvey)

print(app.url_map)
