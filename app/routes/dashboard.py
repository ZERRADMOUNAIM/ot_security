"""
Dashboard routes — main interface, history, analysis detail.
"""

import uuid
from flask import Blueprint, render_template, abort, session

from app import db
from app.models.analysis import Analysis
from app.models.visitor import Visitor
from app.utils.helpers import severity_bg, decision_icon, time_ago, calculate_risk_score

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.context_processor
def inject_counters():
    return {
        'total_analyses': Analysis.query.count(),
        'total_visitors': Visitor.query.count()
    }

@dashboard_bp.route('/')
def index():
    """Main dashboard — analysis input and results display."""
    if 'session_id' not in session:
        new_session_id = uuid.uuid4().hex
        session['session_id'] = new_session_id
        # Record new visitor
        visitor = Visitor(session_id=new_session_id)
        db.session.add(visitor)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    recent_analyses = Analysis.query.filter_by(session_id=session['session_id'])\
        .order_by(Analysis.created_at.desc()).limit(5).all()
        
    return render_template('dashboard.html',
                           recent_analyses=recent_analyses,
                           severity_bg=severity_bg,
                           decision_icon=decision_icon,
                           time_ago=time_ago)


@dashboard_bp.route('/history')
def history():
    """Analysis history page."""
    if 'session_id' not in session:
        new_session_id = uuid.uuid4().hex
        session['session_id'] = new_session_id
        visitor = Visitor(session_id=new_session_id)
        db.session.add(visitor)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        
    page = 1
    try:
        from flask import request
        page = int(request.args.get('page', 1))
    except (ValueError, TypeError):
        page = 1

    analyses = Analysis.query.filter_by(session_id=session['session_id'])\
        .order_by(Analysis.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)

    return render_template('history.html',
                           analyses=analyses,
                           severity_bg=severity_bg,
                           decision_icon=decision_icon,
                           time_ago=time_ago,
                           calculate_risk_score=calculate_risk_score)


@dashboard_bp.route('/analysis/<int:analysis_id>')
def analysis_detail(analysis_id):
    """View a single analysis in detail."""
    analysis = Analysis.query.get_or_404(analysis_id)

    # Ensure the user owns this analysis via session
    if 'session_id' not in session or analysis.session_id != session['session_id']:
        abort(403)

    result = analysis.result
    risk_score = calculate_risk_score(result)

    return render_template('analysis.html',
                           analysis=analysis,
                           result=result,
                           risk_score=risk_score,
                           severity_bg=severity_bg,
                           decision_icon=decision_icon,
                           time_ago=time_ago)
