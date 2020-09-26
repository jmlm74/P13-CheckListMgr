import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_utilities.models import Translation


@csrf_exempt
def get_message(request):
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        msg = request_data['msg']
        try:
            language = request.session['language']
        except KeyError:
            language = "UK"
        text_to_display = Translation.get_translation(msg, language)
        data = {'msg': text_to_display, 'data': 'OK'}
    return JsonResponse(data)
