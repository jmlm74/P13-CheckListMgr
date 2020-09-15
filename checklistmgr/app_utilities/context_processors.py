from django.urls import resolve, Resolver404


def get_appname(request):
    """
    context processor to get appname in templates.
    Essentially used to get the corrects css and js files
    """
    try:
        return {'appname': resolve(request.path).app_name}
    except Resolver404:
        return {'appname': None}
