import json
import mimetypes
import os
import tempfile
import uuid
import requests
import weasyprint
import threading
from datetime import datetime
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from weasyprint import HTML, CSS

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import get_script_prefix

from app_checklist.models import CheckListDone
from app_create_chklst.models import CheckList
from app_input_chklst.models import Manager, Material
from app_utilities.models import Translation


def django_url_fetcher(url, *args, **kwargs):
    """
    Url fetcher from weasyprint
    User to display pictures in pdf : tag files : href="file:/media..."
    taken as-is from Weasyprint
    """
    # load file:// paths directly from disk
    if url.startswith('file:'):
        mime_type, encoding = mimetypes.guess_type(url)
        url_path = urlparse(url).path
        data = {
            'mime_type': mime_type,
            'encoding': encoding,
            'filename': Path(url_path).name,
        }

        default_media_url = settings.MEDIA_URL in ('', get_script_prefix())
        if not default_media_url and url_path.startswith(settings.MEDIA_URL):
            path = url_path.replace(settings.MEDIA_URL, settings.MEDIA_ROOT, 1)
            data['file_obj'] = default_storage.open(path)
            return data

        elif settings.STATIC_URL and url_path.startswith(settings.STATIC_URL):
            path = url_path.replace(settings.STATIC_URL, '', 1)
            data['file_obj'] = open(find(path), 'rb')
            return data

    # fall back to weasyprint default fetcher
    return weasyprint.default_url_fetcher(url, *args, **kwargs)


def send_mail(request, newchecklist, result, mgr):
    """
    Send mail via MAILGUN --> loaded by thread
    The mailgun key must be in the env variable
    Only used ig a manager mail has been set --> only for Pro users
    """
    today = datetime.today()
    year = str(today.year)
    month = str(today.month)
    default_media_url = settings.MEDIA_ROOT
    filename = str(newchecklist.cld_company) + "-" + str(today.day) + "-" + str(uuid.uuid4().hex)[:8] + ".pdf"
    full_filename = os.path.join(default_media_url, "checklists", year, month, filename)
    newchecklist.cld_pdf_file.save(filename, File(BytesIO(result)))
    # send mail
    if mgr['mgr_email1']:
        language = request.session['language']
        subject = Translation.get_translation("Checklist", language=language)
        email_template_name = f"app_checklist/email-{language}.txt"
        society1 = str(newchecklist.cld_company.address.street_number) + " " + \
                   str(newchecklist.cld_company.address.street_type) + " " + \
                   str(newchecklist.cld_company.address.address1)
        zipcity = str(newchecklist.cld_company.address.zipcode) + " " + \
                  str(newchecklist.cld_company.address.city) + " - " + \
                  str(newchecklist.cld_company.address.country)
        c = {
            "material": newchecklist.cld_material.mat_designation,
            'society': newchecklist.cld_company.company_name,
            'society1': society1,
            'society2': newchecklist.cld_company.address.address2,
            'society3': zipcity,
        }
        email = render_to_string(email_template_name, c)
        data = {"from": "Checklist Manager <webmaster@jm-hayons74.fr>",
                "to": mgr['mgr_email1'],
                "subject": subject,
                "text": email,
                }
        if mgr['mgr_email2']:
            data["cc"] = mgr['mgr_email2']
        try:
            # send the mail
            rc = requests.post(
                "https://api.mailgun.net/v3/sandbox1f42285ff9e446fa9e90d34287cd8fee.mailgun.org/messages",
                auth=("api", settings.MAILGUN_KEY),
                files=[("attachment", (filename, open(full_filename, "rb").read()))],
                data=data)
            # print(f"Retour send mail : {rc}")
        except:
           pass
    return


def render_pdf_view(request, *args, **kwargs):
    """
    pdf renderer
    args : {'save': 'What you want !!!!'} or None
            if save in args --> save pdf in media root + Year/month/
                            --> send mail if email is set in manager (even a cc to the email2) via MAILGUN API
            if not --> display preview without saving
    Returns :
            if save --> redirect to main page
            if not --> return pdf render (new page)
    """
    # Get all the datas for the preview
    newchecklist = CheckListDone.objects.get(pk=request.session['newchecklist_id'])
    fotos = newchecklist.pho_chklst.all()

    checklist = CheckList.objects.get(pk=request.session['checklist_id'])
    details = checklist.chklst_detail()


    mgr = request.session['mgr']
    mat = request.session['mat']
    if mgr['id'] != '0':
        manager = Manager.objects.get(pk=mgr['id'])
    else:
        manager = None
    if mat['id'] != '0':
        material = Material.objects.get(pk=mat['id'])
    else:
        material = None
    # get choices and remarks --> in specially formatted string --> put them in dicts
    choices = request.session['chklst']['save']
    choices = choices[:-2]
    choices = '{"' + choices + '}'
    choices = choices.replace(':', '":')
    choices = choices.replace(',', ',"')
    dict_choices = json.loads(choices)

    remarks = request.session['chklst']['remsave']
    remarks = remarks.replace("\r\n", "{CRLF}")
    remarks = remarks.replace('],', ',')
    remarks = remarks.replace('[[', '"')
    remarks = remarks.replace('][', '":"')
    remarks = remarks.replace(']}}', '"')
    remarks = remarks[:-1]
    remarks = "{" + remarks + "}"
    dict_remarks = json.loads(remarks)

    # create context for preview
    base_url = request.build_absolute_uri()
    context = {
        'mgr': mgr,
        'mat': mat,
        'manager': manager,
        'material': material,
        'base_url': base_url,
        'Checklist': newchecklist,
        'fotos': fotos,
        'title': newchecklist.cld_key,
        'dict_choices': dict_choices,
        'details': details,
        'dict_remarks': dict_remarks,
        'user': request.user
    }

    # PDF generator
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'  # just for display not as attachement
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string('app_checklist/chklstpdf.html', context=context)
    html = HTML(string=html_string, url_fetcher=django_url_fetcher)
    css = CSS(string='@page { size: A4; '
                     'margin: 15mm 20mm;'
                     '@top-right{content: "Page " counter(page) " of " counter(pages);}}')
    result = html.write_pdf(stylesheets=[css])
    # save in media root
    if "save" in kwargs:
        task = threading.Thread(target=send_mail, args=(request, newchecklist, result, mgr))
        task.start()
        return redirect('app_home:main')
    # render pdf --> return pdf response in browser
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
