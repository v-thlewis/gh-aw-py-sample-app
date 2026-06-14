"""
Test file with intentional if-else chain violations.
Contains multiple long if-else chains that should be converted to match/case or dict dispatch.
"""

# Helper functions defined first so dispatch tables can reference them directly
# (avoids lambda wrappers and the extra call frame they introduce)

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


# O(1) dispatch tables — module-level to avoid rebuilding on every call.
# Direct function references avoid the extra lambda call frame.
_REQUEST_TYPE_HANDLERS = {
    'GET': handle_get_request,
    'POST': handle_post_request,
    'PUT': handle_put_request,
    'DELETE': handle_delete_request,
    'PATCH': handle_patch_request,
    'HEAD': handle_head_request,
    'OPTIONS': handle_options_request,
    'TRACE': handle_trace_request,
}

_STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
}

_FILE_EXTENSION_HANDLERS = {
    '.txt': process_text_file,
    '.csv': process_csv_file,
    '.json': process_json_file,
    '.xml': process_xml_file,
    '.pdf': process_pdf_file,
    '.docx': process_docx_file,
    '.xlsx': process_xlsx_file,
    '.zip': process_zip_file,
    '.tar.gz': process_tarball,
}

_DISCOUNTS = {
    'PREMIUM': 0.20,
    'GOLD': 0.15,
    'SILVER': 0.10,
    'BRONZE': 0.05,
    'STUDENT': 0.25,
    'SENIOR': 0.18,
}


def process_request_type(request_type):
    """Violation 1: Long if-else chain for request type handling (8 branches)."""
    return _REQUEST_TYPE_HANDLERS.get(request_type, handle_unknown_request)()

def get_status_message(status_code):
    """Violation 2: Long if-else chain for HTTP status codes (7 branches)."""
    return _STATUS_MESSAGES.get(status_code, "Unknown Status")

def process_file_extension(extension):
    """Violation 3: Long if-else chain for file type processing (9 branches)."""
    return _FILE_EXTENSION_HANDLERS.get(extension, process_unknown_file)()

def calculate_discount(user_type):
    """Violation 4: Long if-else chain for discount calculation (6 branches)."""
    return _DISCOUNTS.get(user_type, 0.0)

class EventProcessor:
    """Class with if-else chain violations."""

    # O(1) dispatch: map event names to handler method names
    _EVENT_HANDLERS = {
        'user_login': 'process_login',
        'user_logout': 'process_logout',
        'password_change': 'process_password_change',
        'profile_update': 'process_profile_update',
        'purchase': 'process_purchase',
        'refund': 'process_refund',
        'subscription': 'process_subscription',
    }

    def handle_event(self, event_type):
        """Violation 5: Long if-else chain in class method (7 branches)."""
        handler_name = self._EVENT_HANDLERS.get(event_type)
        if handler_name:
            return getattr(self, handler_name)()
        return self.process_unknown_event()
    
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
