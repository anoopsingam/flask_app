from flask import Blueprint, render_template

from Utility.Config import login_required

ap = Blueprint('ap', __name__)


@ap.route('/')
def home():
    return render_template('home.html')


@ap.route('/app/privacy-policy')
@login_required
def privacy_policy():
    return render_template('admin/privacy-policy.html')
