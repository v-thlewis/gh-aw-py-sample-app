"""
Test file with intentional if-else chain violations.
Contains multiple long if-else chains that should be converted to match/case or dict dispatch.
"""

def process_request_type(request_type):
    """Violation 1: Long if-else chain for request type handling (8 branches)."""
    if request_type == 'GET':
        return handle_get_request()
    elif request_type == 'POST':
        return handle_post_request()
    elif request_type == 'PUT':
        return handle_put_request()
    elif request_type == 'DELETE':
        return handle_delete_request()
    elif request_type == 'PATCH':
        return handle_patch_request()
    elif request_type == 'HEAD':
        return handle_head_request()
    elif request_type == 'OPTIONS':
        return handle_options_request()
    elif request_type == 'TRACE':
        return handle_trace_request()
    else:
        return handle_unknown_request()

def get_status_message(status_code):
    """Violation 2: Long if-else chain for HTTP status codes (7 branches)."""
    if status_code == 200:
        return "OK"
    elif status_code == 201:
        return "Created"
    elif status_code == 400:
        return "Bad Request"
    elif status_code == 401:
        return "Unauthorized"
    elif status_code == 403:
        return "Forbidden"
    elif status_code == 404:
        return "Not Found"
    elif status_code == 500:
        return "Internal Server Error"
    else:
        return "Unknown Status"

def process_file_extension(extension):
    """Violation 3: Long if-else chain for file type processing (9 branches)."""
    if extension == '.txt':
        return process_text_file()
    elif extension == '.csv':
        return process_csv_file()
    elif extension == '.json':
        return process_json_file()
    elif extension == '.xml':
        return process_xml_file()
    elif extension == '.pdf':
        return process_pdf_file()
    elif extension == '.docx':
        return process_docx_file()
    elif extension == '.xlsx':
        return process_xlsx_file()
    elif extension == '.zip':
        return process_zip_file()
    elif extension == '.tar.gz':
        return process_tarball()
    else:
        return process_unknown_file()

def calculate_discount(user_type):
    """Violation 4: Long if-else chain for discount calculation (6 branches)."""
    if user_type == 'PREMIUM':
        return 0.20
    elif user_type == 'GOLD':
        return 0.15
    elif user_type == 'SILVER':
        return 0.10
    elif user_type == 'BRONZE':
        return 0.05
    elif user_type == 'STUDENT':
        return 0.25
    elif user_type == 'SENIOR':
        return 0.18
    else:
        return 0.0

class EventProcessor:
    """Class with if-else chain violations."""
    
    def handle_event(self, event_type):
        """Violation 5: Long if-else chain in class method (7 branches)."""
        if event_type == 'user_login':
            return self.process_login()
        elif event_type == 'user_logout':
            return self.process_logout()
        elif event_type == 'password_change':
            return self.process_password_change()
        elif event_type == 'profile_update':
            return self.process_profile_update()
        elif event_type == 'purchase':
            return self.process_purchase()
        elif event_type == 'refund':
            return self.process_refund()
        elif event_type == 'subscription':
            return self.process_subscription()
        else:
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
