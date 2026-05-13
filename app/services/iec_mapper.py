"""
IEC 62443 Reference Mapper.
Provides standard references, security requirements, and zone/conduit data.
"""


# IEC 62443 Standard Parts
IEC_STANDARDS = {
    "IEC 62443-1-1": {
        "title": "Concepts and Models",
        "description": "Terminology, concepts, and models for industrial automation and control system security."
    },
    "IEC 62443-2-1": {
        "title": "Security Program Requirements for IACS Asset Owners",
        "description": "Requirements for establishing and maintaining an IACS security program."
    },
    "IEC 62443-2-4": {
        "title": "Security Program Requirements for IACS Service Providers",
        "description": "Security requirements for IACS service providers including integration and maintenance."
    },
    "IEC 62443-3-2": {
        "title": "Security Risk Assessment and System Design",
        "description": "Methodology for security risk assessment and zone/conduit model design."
    },
    "IEC 62443-3-3": {
        "title": "System Security Requirements and Security Levels",
        "description": "System-level security requirements mapped to four security levels (SL)."
    },
    "IEC 62443-4-1": {
        "title": "Secure Product Development Lifecycle",
        "description": "Requirements for secure development of IACS products."
    },
    "IEC 62443-4-2": {
        "title": "Technical Security Requirements for IACS Components",
        "description": "Component-level security requirements for embedded devices, host devices, network devices, and applications."
    },
}

# Foundational Requirements
FOUNDATIONAL_REQUIREMENTS = {
    "FR 1": {
        "name": "Identification and Authentication Control",
        "description": "Identify and authenticate all users before allowing access.",
        "security_requirements": ["SR 1.1", "SR 1.2", "SR 1.3", "SR 1.5", "SR 1.6", "SR 1.7", "SR 1.9", "SR 1.13"]
    },
    "FR 2": {
        "name": "Use Control",
        "description": "Enforce the assigned privileges of authenticated users.",
        "security_requirements": ["SR 2.1", "SR 2.4", "SR 2.5", "SR 2.6", "SR 2.8", "SR 2.9", "SR 2.12"]
    },
    "FR 3": {
        "name": "System Integrity",
        "description": "Ensure the integrity of the IACS to prevent unauthorized manipulation.",
        "security_requirements": ["SR 3.1", "SR 3.3", "SR 3.4"]
    },
    "FR 4": {
        "name": "Data Confidentiality",
        "description": "Ensure the confidentiality of information on IACS communication channels.",
        "security_requirements": ["SR 4.1", "SR 4.3"]
    },
    "FR 5": {
        "name": "Restricted Data Flow",
        "description": "Segment the IACS into zones and control data flows through conduits.",
        "security_requirements": ["SR 5.1", "SR 5.2", "SR 5.3", "SR 5.4"]
    },
    "FR 6": {
        "name": "Timely Response to Events",
        "description": "Respond to security violations by notifying proper authorities and taking corrective action.",
        "security_requirements": ["SR 6.1", "SR 6.2"]
    },
    "FR 7": {
        "name": "Resource Availability",
        "description": "Ensure the availability of the IACS against denial-of-service attacks.",
        "security_requirements": ["SR 7.1", "SR 7.2", "SR 7.3", "SR 7.4", "SR 7.6", "SR 7.7", "SR 7.8"]
    },
}

# Security Levels
SECURITY_LEVELS = {
    "SL 1": "Protection against casual or coincidental violation.",
    "SL 2": "Protection against intentional violation using simple means.",
    "SL 3": "Protection against sophisticated attack using moderate resources.",
    "SL 4": "Protection against state-sponsored attack using extensive resources.",
}

# Zone/Conduit Model Reference
ZONE_CONDUIT_MODEL = {
    "Enterprise Zone": {
        "purdue_level": "Level 5",
        "description": "Corporate IT network, internet connectivity, email, ERP.",
        "typical_assets": ["Corporate servers", "Email", "ERP systems", "Internet"]
    },
    "DMZ": {
        "purdue_level": "Level 3.5",
        "description": "Demilitarized zone between IT and OT networks.",
        "typical_assets": ["Historian mirror", "Patch server", "AV server", "Remote access gateway"]
    },
    "Manufacturing Zone": {
        "purdue_level": "Level 3",
        "description": "Site operations and control, production management.",
        "typical_assets": ["Historian", "Engineering workstations", "Application servers"]
    },
    "Control Zone": {
        "purdue_level": "Level 2",
        "description": "Supervisory control and data acquisition.",
        "typical_assets": ["HMI", "SCADA servers", "Engineering workstations"]
    },
    "Field Zone": {
        "purdue_level": "Level 1",
        "description": "Basic control — controllers and safety systems.",
        "typical_assets": ["PLC", "RTU", "DCS controllers", "SIS"]
    },
    "Process Zone": {
        "purdue_level": "Level 0",
        "description": "Physical process — sensors and actuators.",
        "typical_assets": ["Sensors", "Actuators", "Field instruments"]
    },
}


def get_standard(standard_id):
    """Get IEC 62443 standard details by ID."""
    return IEC_STANDARDS.get(standard_id, None)


def get_all_standards():
    """Return all IEC 62443 standards."""
    return IEC_STANDARDS


def get_foundational_requirements():
    """Return all foundational requirements."""
    return FOUNDATIONAL_REQUIREMENTS


def get_security_levels():
    """Return security level definitions."""
    return SECURITY_LEVELS


def get_zone_conduit_model():
    """Return the zone/conduit model reference."""
    return ZONE_CONDUIT_MODEL
