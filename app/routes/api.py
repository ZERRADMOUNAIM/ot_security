"""
API routes — analysis endpoint and export.
"""

import json
import logging
import uuid
from flask import Blueprint, request, jsonify, session

from app import db, limiter, csrf
from app.models.analysis import Analysis
from app.services.groq_service import GroqService
from app.utils.validators import validate_scenario
from app.utils.helpers import calculate_risk_score

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Initialize the Groq service
groq_service = GroqService()


@api_bp.route('/analyze', methods=['POST'])
@limiter.limit("10/minute")
@csrf.exempt  # API uses JSON, CSRF handled via session
def analyze():
    """
    Analyze an OT cybersecurity request.
    
    Request JSON:
        { "scenario": "Vendor requires remote access to SCADA historian" }
    
    Returns:
        Structured cybersecurity assessment JSON.
    """
    data = request.get_json()

    if not data or 'scenario' not in data:
        return jsonify({'error': 'Missing "scenario" field in request body.'}), 400

    scenario = data['scenario']

    # Validate the input
    is_valid, error_msg = validate_scenario(scenario)
    if not is_valid:
        return jsonify({'error': error_msg}), 400

    try:
        # Call the AI engine
        result = groq_service.analyze_ot_request(scenario)

        # Calculate risk score
        risk_score = calculate_risk_score(result)

        # Extract severity based on risk score
        if risk_score >= 80:
            severity = 'Critical'
        elif risk_score >= 60:
            severity = 'High'
        elif risk_score >= 40:
            severity = 'Medium'
        else:
            severity = 'Low'

        # Ensure session_id exists
        if 'session_id' not in session:
            new_session_id = uuid.uuid4().hex
            session['session_id'] = new_session_id
            from app.models.visitor import Visitor
            visitor = Visitor(session_id=new_session_id)
            db.session.add(visitor)
            db.session.commit()

        # Save to database
        analysis = Analysis(
            scenario=scenario.strip(),
            result_json=json.dumps(result, ensure_ascii=False),
            risk_score=risk_score,
            severity=severity,
            session_id=session['session_id']
        )
        db.session.add(analysis)
        db.session.commit()

        logger.info(f"Analysis {analysis.id} created by session {session['session_id']}")

        return jsonify({
            'id': analysis.id,
            'scenario': analysis.scenario,
            'result': result,
            'risk_score': risk_score,
            'severity': severity,
            'created_at': analysis.created_at.isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Analysis failed. Please try again.'}), 500


@api_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Retrieve a specific analysis by ID."""
    analysis = Analysis.query.get_or_404(analysis_id)

    if analysis.session_id != session.get('session_id'):
        return jsonify({'error': 'Access denied.'}), 403

    return jsonify({
        'id': analysis.id,
        'scenario': analysis.scenario,
        'result': analysis.result,
        'risk_score': analysis.risk_score,
        'severity': analysis.severity,
        'created_at': analysis.created_at.isoformat()
    })


@api_bp.route('/history', methods=['GET'])
def get_history():
    """Retrieve analysis history for the current session."""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify([])

    analyses = Analysis.query.filter_by(session_id=session_id)\
        .order_by(Analysis.created_at.desc()).limit(50).all()

    return jsonify([{
        'id': a.id,
        'scenario': a.scenario_preview,
        'severity': a.severity,
        'risk_score': a.risk_score,
        'created_at': a.created_at.isoformat()
    } for a in analyses])
