from flask import *

from core.data import responses as resp
from core.data.database import dbconnect

bp = Blueprint("system", __name__, url_prefix="/system")

@bp.route('/', methods=['GET'])
def index():
    return render_template('system/index.html')