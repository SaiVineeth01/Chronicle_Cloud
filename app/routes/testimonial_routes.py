from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.testimonial import Testimonial
from app import db

testimonial_bp = Blueprint('testimonial', __name__)

# Optional: Page to view all testimonials
@testimonial_bp.route('/testimonials')
def testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('testimonials.html', testimonials=testimonials)

# Form to submit testimonial
@testimonial_bp.route('/testimonial/submit', methods=['POST'])
@login_required
def submit_testimonial():
    message = request.form.get('message')
    if not message:
        flash('Testimonial message cannot be empty.', 'danger')
        return redirect(url_for('main.dashboard'))

    new_testimonial = Testimonial(username=current_user.username, message=message)
    db.session.add(new_testimonial)
    db.session.commit()
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('main.dashboard'))

# DELETE Testimonial (admin only)
@testimonial_bp.route('/testimonials/delete/<int:testimonial_id>', methods=['POST'])
@login_required
def delete_testimonial(testimonial_id):
    if current_user.role != 'admin':
        flash("You are not authorized to delete testimonials.", "danger")
        return redirect(url_for('main.dashboard'))

    testimonial = Testimonial.query.get_or_404(testimonial_id)
    try:
        db.session.delete(testimonial)
        db.session.commit()
        flash("Testimonial deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        print("Error deleting testimonial:", e)
        flash("An error occurred while deleting the testimonial.", "danger")
    
    return redirect(url_for('main.dashboard'))
