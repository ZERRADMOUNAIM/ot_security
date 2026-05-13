"""
Helper utilities for OTMindset.
"""

from datetime import datetime, timezone


def severity_color(severity):
    """Return CSS color class for a severity level."""
    colors = {
        'Critical': 'text-red-700 dark:text-red-400',
        'High': 'text-orange-700 dark:text-orange-400',
        'Medium': 'text-yellow-700 dark:text-yellow-400',
        'Low': 'text-green-700 dark:text-green-400',
    }
    return colors.get(severity, 'text-gray-700 dark:text-gray-400')


def severity_bg(severity):
    """Return CSS background class for a severity badge."""
    colors = {
        'Critical': 'bg-red-50 text-red-700 border-red-200 dark:bg-red-500/20 dark:text-red-400 dark:border-red-500/30',
        'High': 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-500/20 dark:text-orange-400 dark:border-orange-500/30',
        'Medium': 'bg-yellow-50 text-yellow-700 border-yellow-200 dark:bg-yellow-500/20 dark:text-yellow-400 dark:border-yellow-500/30',
        'Low': 'bg-green-50 text-green-700 border-green-200 dark:bg-green-500/20 dark:text-green-400 dark:border-green-500/30',
    }
    return colors.get(severity, 'bg-sand-100 text-gray-700 border-sand-200 dark:bg-gray-500/20 dark:text-gray-400 dark:border-gray-500/30')


def decision_icon(decision):
    """Return icon for decision type."""
    icons = {
        'Proceed': '✅',
        'Proceed with Controls': '🛡️',
        'Requires Further Review': '🔍',
        'Escalate to OT Security': '⚠️',
        'Reject Until Clarified': '❌',
    }
    return icons.get(decision, '❓')


def calculate_risk_score(result):
    """
    Calculate a numeric risk score (0-100) based on analysis results.
    """
    score = 25  # Base score

    # Number of risks identified (max 40 points)
    risks = result.get('expected_risks', [])
    score += min(len(risks) * 7, 40)

    # Number of missing information items/questions (max 20 points)
    questions = result.get('what_you_should_ask', [])
    score += min(len(questions) * 4, 20)

    # Keyword analysis in risks to dynamically boost score
    risk_text = " ".join(risks).lower()
    if any(keyword in risk_text for keyword in ['critical', 'safety', 'ransomware', 'stuxnet', 'production stop']):
        score += 15
    elif any(keyword in risk_text for keyword in ['high', 'downtime', 'unauthorized', 'malware']):
        score += 10
    elif any(keyword in risk_text for keyword in ['medium', 'exposure', 'sniffing']):
        score += 5

    # Ensure the score stays within 0-100 boundaries
    return min(max(int(score), 10), 100)


def format_timestamp(dt):
    """Format a datetime object for display."""
    if dt is None:
        return 'N/A'
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime('%Y-%m-%d %H:%M UTC')


def time_ago(dt):
    """Return a human-readable 'time ago' string."""
    if dt is None:
        return 'unknown'
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        mins = int(seconds / 60)
        return f'{mins}m ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours}h ago'
    else:
        days = int(seconds / 86400)
        return f'{days}d ago'
