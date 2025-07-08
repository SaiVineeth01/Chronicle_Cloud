from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.models import Blog
from app import db
import random
from datetime import datetime
from flask_login import login_required, current_user
from app.controllers.blog_controller import save_blog
from app.utils.text_image_generator import generate_blog_image_helper
from app.utils.activity_logger import log_activity
from app.models.activity import Activity  


blog_bp = Blueprint('blogs', __name__)

# View all blogs
@blog_bp.route('/view_blogs')
def view_blogs():
    blogs = Blog.query.all()
    return render_template('view_blogs.html', blogs=blogs)

# Alternative route to blogs page
@blog_bp.route('/blogs')
def blogs_page():
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)

# Render blog creation form
@blog_bp.route('/blogs/create', methods=['GET'])
@login_required
def create_blog():
    
    return render_template('create_blog.html')

# Create new blog
@blog_bp.route('/blogs/create', methods=['POST'])
@login_required
def create_new_blog():
    title = request.form['title']
    category = request.form.get('category')
    content = request.form['content']
    ai_image = request.form.get('ai_image')
    due_date_str = request.form.get('due_date')  # 🟡 Raw string from form

    if not title or not content:
        flash("Title and content are required!", "danger")
        return redirect(url_for('blogs.create_blog'))

    # 🟢 Convert due_date string to a proper datetime.date object (if provided)
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid due date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for('blogs.create_blog'))

    # 🟢 Generate image or use AI-generated one
    image_path = ai_image if ai_image else generate_blog_image_helper(title, content)

    try:
        new_blog = Blog(
            title=title,
            category=category,
            content=content,
            image_url=image_path,
            due_date=due_date,  # 🟢 Now a valid Python date
            created_at=db.func.now(),
            user_id=current_user.id
        )
        db.session.add(new_blog)
        db.session.commit()
        
        log_activity(current_user.id, "Created Blog", f"Blog titled '{title}' was published.")
        flash("Blog created successfully!", "success")
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        flash("There was an error creating the blog. Please try again.", "danger")

    return redirect(url_for('blogs.view_blogs'))

# Delete a blog
@blog_bp.route('/blogs/delete/<int:blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if blog.user_id != current_user.id and current_user.role != 'admin':
        flash("You are not authorized to delete this blog.", "danger")
        return redirect(url_for('blogs.view_blogs'))

    # Save details before deletion (for activity logging)
    blog_title = blog.title
    blog_author = blog.user.username

    try:
        # Delete blog
        db.session.delete(blog)
        db.session.commit()

        # ✅ Log activity
        activity = Activity(
            user_id=current_user.id,
            username=current_user.username,
            action_type='blog',
            description=f"Blog titled '{blog_title}' by {blog_author} was deleted."
        )
        db.session.add(activity)
        db.session.commit()

        flash("Blog deleted successfully!", "success")

    except Exception as e:
        db.session.rollback()
        print("Delete Error:", e)
        flash("Error deleting blog.", "danger")

    return redirect(url_for('blogs.view_blogs'))

from flask import jsonify
from datetime import datetime
import random
from app.utils.text_image_generator import generate_blog_image_helper

@blog_bp.route('/generate_blog_ai', methods=['GET'])
def generate_blog_ai():
    blog_data = {
        "Tech": {
            "titles": [
                "AI Revolutionizing Healthcare",
                "The Age of Quantum Computing",
                "Top Cloud Platforms in 2025",
                "5G vs Wi-Fi 6: What's Better?",
                "Blockchain Beyond Crypto",
                "The Power of Edge Computing",
                "How IoT Is Changing Cities",
                "Cybersecurity Trends to Watch",
                "AI and Ethics: The Debate",
                "Big Data in Everyday Life"
            ],
            "intro": "Technology continues to reshape industries at an astonishing pace.",
            "body": "In this blog, we examine how emerging technologies are being integrated into business, healthcare, education, and beyond. From quantum processors to decentralized apps, the pace of innovation challenges both our imagination and infrastructure. We’ll explore the benefits, risks, and what the next wave of adoption means for global societies.",
            "closing": "Tech is no longer optional—it’s the backbone of progress. Stay ahead by staying informed."
        },
        "Education": {
            "titles": [
                "EdTech Innovations Reshaping Classrooms",
                "The Rise of Hybrid Learning",
                "Gamification in Education",
                "Using AI for Personalized Learning",
                "Digital Literacy for the Next Generation",
                "The Globalization of Online Degrees",
                "Challenges in Remote Teaching",
                "Lifelong Learning in the Digital Age",
                "The Future of Examinations",
                "VR & AR in Education: A New Frontier"
            ],
            "intro": "Education is entering a golden age powered by technology and accessibility.",
            "body": "We explore how educators and institutions are adopting digital tools for better learning outcomes. From adaptive assessments to virtual reality classrooms, the evolution of learning environments aims to empower students in new and interactive ways. We also look at how educational equity can be supported by digital access and inclusion.",
            "closing": "The future of education is inclusive, engaging, and driven by innovation."
        },
        "Lifestyle": {
            "titles": [
                "Mindfulness for Busy Minds",
                "Digital Detox: Why and How",
                "Balancing Work and Wellness",
                "Sustainable Fashion Trends",
                "The Power of Morning Routines",
                "Home Workouts That Actually Work",
                "Nutrition Myths Busted",
                "Declutter Your Life: Minimalism Tips",
                "Sleep Science: Better Rest Today",
                "Tech Tools for a Healthier Life"
            ],
            "intro": "A fulfilling lifestyle begins with mindful habits and conscious choices.",
            "body": "This post uncovers practical tips and psychological insights into building healthier routines. From staying active at home to cultivating inner peace in a noisy world, we look at scientifically backed strategies that help build long-term wellbeing. Embracing simplicity and purpose can lead to real happiness.",
            "closing": "Your lifestyle is your foundation—invest in it wisely and intentionally."
        },
        "Other": {
            "titles": [
                "The Psychology of Procrastination",
                "Space Tourism: Are We Ready?",
                "The Economics of Happiness",
                "Creativity in the AI Age",
                "Understanding Climate Anxiety",
                "Time Management for Students",
                "The History of Internet Memes",
                "AI-Generated Art: Threat or Tool?",
                "The Rise of Indie Game Developers",
                "Exploring Human Behavior Through Design"
            ],
            "intro": "In this piece, we explore topics that stretch across disciplines and perspectives.",
            "body": "Whether it's unraveling emotional patterns, assessing economic paradoxes, or spotlighting cultural shifts, these subjects provide a broader lens into the human condition. By examining niche ideas, we encourage curiosity, diversity of thought, and meaningful introspection.",
            "closing": "Every topic is a door to deeper understanding—let curiosity lead you forward."
        }
    }

    # Select random category
    category = random.choice(list(blog_data.keys()))
    title = random.choice(blog_data[category]["titles"])
    content = f"{blog_data[category]['intro']}\n\n{blog_data[category]['body']}\n\n{blog_data[category]['closing']}"
    due_date = datetime.today().strftime('%Y-%m-%d')
    image_path = generate_blog_image_helper(title, content)

    return jsonify({
        "title": title,
        "content": content,
        "category": category,
        "due_date": due_date,
        "image": image_path
    })
@blog_bp.route('/generate_live_image', methods=['POST'])
def generate_live_image():
    data = request.get_json()
    title = data.get('title', '')
    content = data.get('content', '')
    if not title or not content:
        return jsonify({'error': 'Missing title or content'}), 400

    image_path = generate_blog_image_helper(title, content)
    return jsonify({ 'image': image_path })

