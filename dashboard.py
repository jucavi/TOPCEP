from flask import Blueprint, render_template
from auth import login_required

dash_bp = Blueprint('dashboard', __name__)


@dash_bp.route('/')
def index():
    return render_template('index.html')


@dash_bp.route('/workspace')
@login_required
def workspace():
    return render_template('workspace.html', title='workspace')