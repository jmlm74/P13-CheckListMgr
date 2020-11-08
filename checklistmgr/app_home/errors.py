from django.shortcuts import render
"""
Errors handlers.
The most generic as possible --> Dict for the errors - simple functions for the different errors
"""


VIEW_ERRORS = {
    404: {'title': "404 - Page not found",
          'content': "Error 404", },
    500: {'title': "Internal server error",
          'content': "Error 500", },
    403: {'title': "Permission denied",
          'content': "Error 403", },
    400: {'title': "Bad request",
          'content': "Error 400", }, }


def handler404(request, exception=None):
    return error_view_handler(request, exception, 404)


def handler500(request, exception=None):
    return error_view_handler(request, exception, 500)


def handler403(request, exception=None):
    return error_view_handler(request, exception, 403)


def handler400(request, exception=None):
    return error_view_handler(request, exception, 400)


def error_view_handler(request, exception, status):
    """
        Error Handler
        Args :  request : the request !
                exception : the error exception (dict)
                status : status code
        return : errors.html
                 context : error detail to be displayed
    """
    print(f"Erreur {status} - {exception}")
    return render(request, template_name='errors/errors.html', status=status,
                  context={'error': str(exception), 'status': status,
                           'title': VIEW_ERRORS[status]['title'],
                           'content': VIEW_ERRORS[status]['content']})
