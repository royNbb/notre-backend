from rest_framework.response import Response


def success_response_format(data: any, status_code: int) -> Response:
    return Response(
        {
            'data': data,
        },
        status=status_code,
    )


def error_response_format(message: str, status_code: int) -> Response:
    return Response(
        {
            'error': {
                'status': status_code,
                'message': message,
            },
        },
        status=status_code,
    )
