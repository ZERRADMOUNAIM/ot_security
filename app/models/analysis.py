"""
Analysis model for storing OT cybersecurity assessments.
"""

import json
from datetime import datetime, timezone
from app import db


class Analysis(db.Model):
    """Stores OT cybersecurity analysis results."""
    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    scenario = db.Column(db.Text, nullable=False)
    result_json = db.Column(db.Text, nullable=False)  # JSON string
    risk_score = db.Column(db.Float, default=0.0)
    severity = db.Column(db.String(20), default='Medium')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    session_id = db.Column(db.String(100), nullable=True, index=True)

    @property
    def result(self):
        """Parse result_json into a Python dict."""
        try:
            return json.loads(self.result_json)
        except (json.JSONDecodeError, TypeError):
            return {}

    @result.setter
    def result(self, value):
        """Serialize a Python dict to JSON string."""
        self.result_json = json.dumps(value, ensure_ascii=False)

    @property
    def scenario_preview(self):
        """Return a truncated preview of the scenario."""
        if len(self.scenario) > 100:
            return self.scenario[:100] + '...'
        return self.scenario

    def __repr__(self):
        return f'<Analysis {self.id}: {self.scenario_preview}>'
