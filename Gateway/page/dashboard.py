from flask import *

from core.data import responses as resp
from core.data.database import dbconnect
from core import bleutils as ble

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route('/', methods=['GET'])
def index():
    return render_template('dashboard/index.html')