from flask import *

from core.data import responses as resp
from core.data.database import dbconnect
from core import bleutils as ble

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')