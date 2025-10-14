from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Project  # Import db and Project from models
import os
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
# ensure secret key is set on app (flask uses config, but this makes it explicit)
app.secret_key = app.config.get('SECRET_KEY')

# Initialize db with the app
db.init_app(app)

# Create database tables on startup (inside app context)
with app.app_context():
    db.create_all()

# Custom decorator for admin protection
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' not in session:
            flash('Access denied. Please log in.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrap

@app.route('/')
def index():
    # Order by created_at desc so newest appear first
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('index.html', projects=projects)

@app.route('/admin')
def admin_login():
    return render_template('admin.html')

@app.route('/admin/login', methods=['POST'])
def login():
    pin = request.form.get('pin', '').strip()
    if len(pin) == 4 and pin == app.config['ADMIN_PIN']:
        session['admin'] = True
        flash('Logged in successfully.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid PIN. Please try again.', 'error')
        return redirect(url_for('admin_login'))

@app.route('/dashboard')
@admin_required
def dashboard():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('dashboard.html', projects=projects)

@app.route('/add_project', methods=['POST'])
@admin_required
def add_project():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    image_url = request.form.get('image_url', '').strip()
    project_link = request.form.get('project_link', '').strip() or None

    if title and description and image_url:
        try:
            project = Project(
                title=title,
                description=description,
                image_url=image_url,
                project_link=project_link
            )
            db.session.add(project)
            db.session.commit()
            flash('Project added successfully.', 'success')
        except Exception as e:
            # print stacktrace to server logs to help debugging
            import traceback
            traceback.print_exc()
            db.session.rollback()
            flash('An error occurred while saving the project. Check server logs.', 'error')
    else:
        flash('All fields (title, description, image URL) are required.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/delete_project/<int:project_id>')
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully.', 'success')
    except Exception:
        import traceback
        traceback.print_exc()
        db.session.rollback()
        flash('Error deleting project. Check server logs.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
