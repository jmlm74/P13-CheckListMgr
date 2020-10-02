import json
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_utilities.models import Translation
from app_user.models import Address
from django.core import serializers


@csrf_exempt
def get_message(request):
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        msg = request_data['msg']
        try:
            language = request.session['language']
        except KeyError:
            language = "UK"
        text_to_display = Translation.get_translation(msg, language=language)
        data = {'msg': text_to_display, 'data': 'OK'}
    return JsonResponse(data)


@csrf_exempt
def get_address(request):
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        id_address = request_data['id']
        try:
            address = Address.objects.filter(pk=int(id_address))
        except ObjectDoesNotExist:
            data = {'data': 'Error'}
        else:
            print(address)
            print(type(address))
            address = serializers.serialize("json", address)
            data = {'address': address, 'data': 'OK'}

    return JsonResponse(data)
