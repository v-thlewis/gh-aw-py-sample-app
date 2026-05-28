"""
Additional test file with more if-else chain violations.
"""

def route_traffic(region):
    """Violation 6: Long if-else chain for traffic routing (8 branches)."""
    if region == 'us-east-1':
        return route_to_virginia()
    elif region == 'us-west-2':
        return route_to_oregon()
    elif region == 'eu-west-1':
        return route_to_ireland()
    elif region == 'eu-central-1':
        return route_to_frankfurt()
    elif region == 'ap-southeast-1':
        return route_to_singapore()
    elif region == 'ap-northeast-1':
        return route_to_tokyo()
    elif region == 'ca-central-1':
        return route_to_canada()
    elif region == 'sa-east-1':
        return route_to_brazil()
    else:
        return route_to_default()

def parse_log_level(level):
    """Short chain that should NOT be flagged (only 4 branches)."""
    if level == 'DEBUG':
        return 10
    elif level == 'INFO':
        return 20
    elif level == 'WARNING':
        return 30
    elif level == 'ERROR':
        return 40
    else:
        return 50

# Helper functions
def route_to_virginia():
    return "Routing to us-east-1"

def route_to_oregon():
    return "Routing to us-west-2"

def route_to_ireland():
    return "Routing to eu-west-1"

def route_to_frankfurt():
    return "Routing to eu-central-1"

def route_to_singapore():
    return "Routing to ap-southeast-1"

def route_to_tokyo():
    return "Routing to ap-northeast-1"

def route_to_canada():
    return "Routing to ca-central-1"

def route_to_brazil():
    return "Routing to sa-east-1"

def route_to_default():
    return "Routing to default region"
