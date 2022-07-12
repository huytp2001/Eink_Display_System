from flask import *

from core.data import responses as resp
from core.data.database import dbconnect
from core import bleutils as ble

bp = Blueprint("slave", __name__, url_prefix="/slave")

@bp.route('/', methods=['GET'])
def index():
    return render_template('slave/index.html')

@bp.route('/scan', methods=['GET'])
def scan():
    return render_template('slave/scan.html')

@bp.route('<mac>/test', methods=['GET'])
def test(mac):
    return render_template('slave/test.html', mac= mac)

@bp.route('<mac>', methods=['GET'])
def details(mac):
    return render_template('slave/details.html', mac= mac)