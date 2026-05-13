from datetime import datetime, timezone
from app import db

class Visitor(db.Model):
    """Tracks unique visitors to the site."""
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    first_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Visitor {self.session_id}>'
