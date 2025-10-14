from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Define db here, independent of the app
db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(1000), nullable=False)
    project_link = db.Column(db.String(1000), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'
