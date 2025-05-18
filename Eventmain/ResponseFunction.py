from rest_framework.response import Response


def success_response(data=None, status_code=200):
    return Response(data, status=status_code)
    

def error_response(message, error_code=400, error_details=None):
    response = {
        "message": message,
    }
    if error_details:
        response["error_details"] = error_details
    return Response(response, status=error_code)