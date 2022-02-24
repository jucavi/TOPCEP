from flask import Blueprint, render_template
from auth import login_required, g

dash_bp = Blueprint('dashboard', __name__)


@dash_bp.route('/')
def index():
    return render_template('index.html', user=g.user)


@dash_bp.route('/workspace')
@login_required
def workspace():
    return render_template('workspace.html', title='workspace', user=g.user)