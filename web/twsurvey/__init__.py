
from flask import Blueprint


twsurvey = Blueprint('twsurvey', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/twsurvey')


from . import views
