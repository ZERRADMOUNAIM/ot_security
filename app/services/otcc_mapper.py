"""
OTCC (OT Cybersecurity Controls) Mapper.
Provides domain mappings and control references for OT compliance.
"""


# OTCC Control Domains with descriptions and common controls
OTCC_DOMAINS = {
    "OT-1": {
        "name": "OT Cybersecurity Governance",
        "description": "Policies, procedures, and governance structure for OT cybersecurity.",
        "controls": [
            "OT-1.1: OT Cybersecurity Policy",
            "OT-1.2: OT Cybersecurity Roles and Responsibilities",
            "OT-1.3: OT Cybersecurity Risk Management",
            "OT-1.4: OT Cybersecurity Awareness and Training",
            "OT-1.5: OT Cybersecurity Compliance",
        ]
    },
    "OT-2": {
        "name": "OT Asset Management",
        "description": "Identification, classification, and management of OT assets.",
        "controls": [
            "OT-2.1: OT Asset Inventory",
            "OT-2.2: OT Asset Classification",
            "OT-2.3: OT Asset Ownership",
            "OT-2.4: OT Media Management",
        ]
    },
    "OT-3": {
        "name": "OT Network Security & Architecture",
        "description": "Network segmentation, architecture design, and communication security.",
        "controls": [
            "OT-3.1: OT Network Architecture",
            "OT-3.2: OT Network Segmentation",
            "OT-3.3: OT DMZ Implementation",
            "OT-3.4: OT Wireless Security",
            "OT-3.5: OT Communication Security",
        ]
    },
    "OT-4": {
        "name": "OT Vulnerability Management",
        "description": "Vulnerability identification, assessment, and remediation for OT systems.",
        "controls": [
            "OT-4.1: OT Vulnerability Assessment",
            "OT-4.2: OT Patch Management",
            "OT-4.3: OT Penetration Testing",
        ]
    },
    "OT-5": {
        "name": "OT Access Control",
        "description": "Identity management, authentication, and authorization for OT systems.",
        "controls": [
            "OT-5.1: OT Access Control Policy",
            "OT-5.2: OT User Authentication",
            "OT-5.3: OT Privileged Access Management",
            "OT-5.4: OT Account Management",
            "OT-5.5: OT Multi-Factor Authentication",
        ]
    },
    "OT-6": {
        "name": "OT Remote Access",
        "description": "Secure remote access to OT environments.",
        "controls": [
            "OT-6.1: OT Remote Access Policy",
            "OT-6.2: OT Remote Access Architecture",
            "OT-6.3: OT Remote Session Monitoring",
            "OT-6.4: OT Remote Access Time Limits",
        ]
    },
    "OT-7": {
        "name": "OT Third-Party Management",
        "description": "Management and oversight of third-party access and services.",
        "controls": [
            "OT-7.1: OT Third-Party Risk Assessment",
            "OT-7.2: OT Third-Party Access Control",
            "OT-7.3: OT Third-Party Monitoring",
            "OT-7.4: OT Supply Chain Security",
        ]
    },
    "OT-8": {
        "name": "OT Physical Security",
        "description": "Physical security controls for OT environments and assets.",
        "controls": [
            "OT-8.1: OT Physical Access Control",
            "OT-8.2: OT Equipment Protection",
            "OT-8.3: OT Environmental Controls",
        ]
    },
    "OT-9": {
        "name": "OT Incident Management",
        "description": "Detection, response, and recovery from OT cybersecurity incidents.",
        "controls": [
            "OT-9.1: OT Incident Response Plan",
            "OT-9.2: OT Incident Detection",
            "OT-9.3: OT Incident Response",
            "OT-9.4: OT Incident Recovery",
            "OT-9.5: OT Forensics",
        ]
    },
    "OT-10": {
        "name": "OT Business Continuity",
        "description": "Continuity planning and disaster recovery for OT systems.",
        "controls": [
            "OT-10.1: OT Business Continuity Plan",
            "OT-10.2: OT Backup and Recovery",
            "OT-10.3: OT Redundancy",
        ]
    },
    "OT-11": {
        "name": "OT Monitoring & Logging",
        "description": "Continuous monitoring, logging, and alerting for OT environments.",
        "controls": [
            "OT-11.1: OT Security Monitoring",
            "OT-11.2: OT Log Management",
            "OT-11.3: OT Anomaly Detection",
            "OT-11.4: OT Security Information and Event Management",
        ]
    },
    "OT-12": {
        "name": "OT Configuration & Change Management",
        "description": "Configuration baseline management and change control for OT systems.",
        "controls": [
            "OT-12.1: OT Configuration Management",
            "OT-12.2: OT Change Management",
            "OT-12.3: OT Baseline Configuration",
        ]
    },
    "OT-13": {
        "name": "OT Data Protection",
        "description": "Data classification, encryption, and protection in OT environments.",
        "controls": [
            "OT-13.1: OT Data Classification",
            "OT-13.2: OT Data Encryption",
            "OT-13.3: OT Data Backup",
        ]
    },
}


def get_domain(domain_id):
    """Get OTCC domain details by ID."""
    return OTCC_DOMAINS.get(domain_id, None)


def get_all_domains():
    """Return all OTCC domains."""
    return OTCC_DOMAINS


def get_domain_names():
    """Return a list of (id, name) tuples for all domains."""
    return [(k, v["name"]) for k, v in OTCC_DOMAINS.items()]


def search_controls(keyword):
    """Search controls across all domains by keyword."""
    results = []
    keyword_lower = keyword.lower()
    for domain_id, domain in OTCC_DOMAINS.items():
        for control in domain["controls"]:
            if keyword_lower in control.lower() or keyword_lower in domain["name"].lower():
                results.append({
                    "domain_id": domain_id,
                    "domain_name": domain["name"],
                    "control": control
                })
    return results
