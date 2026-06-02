"""
Test file with intentional if-else chain violations.
Contains multiple long if-else chains that should be converted to match/case or dict dispatch.
"""

# Dict dispatch: O(1) hash lookup instead of O(n) linear branch scan.
_REQUEST_TYPE_HANDLERS = {
    'GET': lambda: handle_get_request(),
    'POST': lambda: handle_post_request(),
    'PUT': lambda: handle_put_request(),
    'DELETE': lambda: handle_delete_request(),
    'PATCH': lambda: handle_patch_request(),
    'HEAD': lambda: handle_head_request(),
    'OPTIONS': lambda: handle_options_request(),
    'TRACE': lambda: handle_trace_request(),
}

def process_request_type(request_type):
    """Dispatch HTTP method to handler via dict lookup (O(1) vs O(n) if-else)."""
    return _REQUEST_TYPE_HANDLERS.get(request_type, handle_unknown_request)()

# Status codes map directly to values — no callable needed.
_STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
}

def get_status_message(status_code):
    """Return HTTP status message via dict lookup (O(1) vs O(n) if-else)."""
    return _STATUS_MESSAGES.get(status_code, "Unknown Status")

_FILE_EXTENSION_HANDLERS = {
    '.txt':    lambda: process_text_file(),
    '.csv':    lambda: process_csv_file(),
    '.json':   lambda: process_json_file(),
    '.xml':    lambda: process_xml_file(),
    '.pdf':    lambda: process_pdf_file(),
    '.docx':   lambda: process_docx_file(),
    '.xlsx':   lambda: process_xlsx_file(),
    '.zip':    lambda: process_zip_file(),
    '.tar.gz': lambda: process_tarball(),
}

def process_file_extension(extension):
    """Dispatch file extension to processor via dict lookup (O(1) vs O(n) if-else)."""
    return _FILE_EXTENSION_HANDLERS.get(extension, process_unknown_file)()

_DISCOUNTS = {
    'PREMIUM': 0.20,
    'GOLD':    0.15,
    'SILVER':  0.10,
    'BRONZE':  0.05,
    'STUDENT': 0.25,
    'SENIOR':  0.18,
}

def calculate_discount(user_type):
    """Return discount rate via dict lookup (O(1) vs O(n) if-else)."""
    return _DISCOUNTS.get(user_type, 0.0)

class EventProcessor:
    """Class with if-else chain violations."""

    # Mapping built once at class definition time — avoids per-call dict allocation.
    _EVENT_HANDLER_NAMES = {
        'user_login':      'process_login',
        'user_logout':     'process_logout',
        'password_change': 'process_password_change',
        'profile_update':  'process_profile_update',
        'purchase':        'process_purchase',
        'refund':          'process_refund',
        'subscription':    'process_subscription',
    }

    def handle_event(self, event_type):
        """Dispatch event type to handler via class-level dict + getattr (O(1) vs O(n) if-else)."""
        method_name = self._EVENT_HANDLER_NAMES.get(event_type, 'process_unknown_event')
        return getattr(self, method_name)()
    
    def process_login(self):
        return "Processing login event"
    
    def process_logout(self):
        return "Processing logout event"
    
    def process_password_change(self):
        return "Processing password change event"
    
    def process_profile_update(self):
        return "Processing profile update event"
    
    def process_purchase(self):
        return "Processing purchase event"
    
    def process_refund(self):
        return "Processing refund event"
    
    def process_subscription(self):
        return "Processing subscription event"
    
    def process_unknown_event(self):
        return "Processing unknown event"

# Helper functions for the violations above
def handle_get_request():
    return "Handling GET request"

def handle_post_request():
    return "Handling POST request"

def handle_put_request():
    return "Handling PUT request"

def handle_delete_request():
    return "Handling DELETE request"

def handle_patch_request():
    return "Handling PATCH request"

def handle_head_request():
    return "Handling HEAD request"

def handle_options_request():
    return "Handling OPTIONS request"

def handle_trace_request():
    return "Handling TRACE request"

def handle_unknown_request():
    return "Handling unknown request"

def process_text_file():
    return "Processing text file"

def process_csv_file():
    return "Processing CSV file"

def process_json_file():
    return "Processing JSON file"

def process_xml_file():
    return "Processing XML file"

def process_pdf_file():
    return "Processing PDF file"

def process_docx_file():
    return "Processing DOCX file"

def process_xlsx_file():
    return "Processing XLSX file"

def process_zip_file():
    return "Processing ZIP file"

def process_tarball():
    return "Processing tarball"

def process_unknown_file():
    return "Processing unknown file type"
