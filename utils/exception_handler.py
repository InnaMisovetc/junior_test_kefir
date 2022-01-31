from rest_framework import exceptions, status
from rest_framework.views import exception_handler

from utils.serializers import BadRequestSerializer, ValidationErrorSerializer


def custom_exception_handler(exc, context):
    handlers = {
        'ValidationError': _handle_validation_error,
        'ParseError': _handle_bad_request_error,
        'Http404': _handle_not_found_error,
        'PermissionDenied': _handle_permission_denied_error,
    }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        response.data = 'Authentication credentials were not provided.'

    if 'UsersListView' in str(context['view']) or 'PrivateUsersListCreateView' in str(context['view']) and exc.status_code == 404:
        response.status_code = 400
        response.data = BadRequestSerializer(data={'code': response.status_code, 'message': exc.detail}).to_json()

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_bad_request_error(exc, context, response):
    response.data = BadRequestSerializer(data={'code': response.status_code, 'message': exc.detail}).to_json()
    return response


def _handle_validation_error(exc, context, response):
    response.status_code = 422
    data = {'detail': []}
    for loc, detail in exc.get_full_details().items():
        data['detail'].append({
            "loc": [loc],
            "msg": detail[0]['message'],
            "type": detail[0]['code']
        })
    response.data = ValidationErrorSerializer(data=data).to_json()
    return response


def _handle_not_found_error(exc, context, response):
    if 'UserUpdateView' in str(context['view']) or 'PrivateUserRetrieveUpdateDestroyView' in str(context['view']):
        response.data = str(exc)
    return response


def _handle_permission_denied_error(exc, context, response):
    if 'PrivateUsersListCreateView' in str(context['view']):
        response.data = exc.detail
    if 'PrivateUserRetrieveUpdateDestroyView' in str(context['view']):
        response.data = exc.detail
    return response
