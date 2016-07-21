
from flask import Blueprint


labeler = Blueprint('labeler', __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/labeler')

from . import views
