"""
Additional test file with more if-else chain violations.
"""

# O(1) dispatch table — module-level to avoid rebuilding on every call
_REGION_ROUTES = {
    'us-east-1': lambda: route_to_virginia(),
    'us-west-2': lambda: route_to_oregon(),
    'eu-west-1': lambda: route_to_ireland(),
    'eu-central-1': lambda: route_to_frankfurt(),
    'ap-southeast-1': lambda: route_to_singapore(),
    'ap-northeast-1': lambda: route_to_tokyo(),
    'ca-central-1': lambda: route_to_canada(),
    'sa-east-1': lambda: route_to_brazil(),
}


def route_traffic(region):
    """Violation 6: Long if-else chain for traffic routing (8 branches)."""
    return _REGION_ROUTES.get(region, route_to_default)()

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
