import re

def handle_db_commit(session):
    try:
        session.commit()
    except Exception as e:
        session.rollback()
    return str(e), 500

def validate_email(email):
    # Improved regex pattern for validating email
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.fullmatch(regex, email) is not None

def validate_request_data(data, required_fields):
    for field in required_fields:
        if field not in data:
            return False
    return True

def handle_error(error_message, status_code):
    return {'error': error_message}, status_code