
def validate_request_data(data, required_fields):
    for field in required_fields:
        if field not in data:
            return False
    return True

def handle_error(error_message, status_code):
    return {'error': error_message}, status_code