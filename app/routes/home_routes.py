from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
import random


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home():
    # If the user is logged in, redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))  # Redirect to dashboard
    # If not logged in, show the home page with login/signup options
    return render_template('home.html')

@home_bp.route('/dashboard')
@login_required
def dashboard():
    # Render the dashboard only if the user is logged in
    return render_template('dashboard.html', user=current_user)


@home_bp.route('/nlp-tools')
def nlp_tools():
    return render_template('nlp_tools.html')

@home_bp.route('/daily-tip')
def daily_tip():
    tips = [
        "Start your day with the hardest task first – it sets the tone for productivity.",
        "Break big goals into smaller, manageable steps.",
        "Use the Pomodoro technique: 25 mins focus, 5 mins break.",
        "Declutter your workspace for better focus.",
        "Prioritize tasks using the Eisenhower Matrix: urgent vs important.",
        "Review your goals weekly to stay on track.",
        "Limit distractions by turning off phone notifications.",
        "Use keyboard shortcuts to save time.",
        "Take short walks to recharge your brain.",
        "Celebrate small wins – they build momentum."
    ]
    return jsonify({"tip": random.choice(tips)})