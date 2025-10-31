"""
Main routes for dashboard UI
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Render the main dashboard

    Returns:
        Rendered dashboard template
    """
    return render_template('dashboard.html')
