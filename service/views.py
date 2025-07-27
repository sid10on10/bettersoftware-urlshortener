from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# 3rd party libraries
import pymongo

# python Standard
from datetime import datetime, time

# utils

from .utils import generate_random_alphanumeric_code

def index(request):

    return JsonResponse(data={
        'code': 200,
        'message': 'Success'
    })

@csrf_exempt
def create_url(request):
    import json

    if request.method == 'POST':
        data = json.loads(request.body)

        if not data.get('url'):
            return JsonResponse(data={
                'code': 400,
                'message': 'url is not present'
            })
        
        if not data.get('redirect_url'):
            return JsonResponse(data={
                'code': 400,
                'message': 'redirect_url is not present'
            })
        
        code = generate_random_alphanumeric_code(10)

        temp = {
            "_id": data['url'],
            "url": data['url'],
            "redirect_url": data["redirect_url"],
            "code": code,
            "visits": 0,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        my_client = pymongo.MongoClient(settings.CONNECTION_STRING)
        shortener = my_client['urlshortener']

        urls = shortener["urls"]

        urls.insert_one(temp)

        return JsonResponse(data={
            'code': 200,
            'message': 'Data successfully inserted',
            'data': f'http://localhost:8000/service/url/{code}'
        })
    else:
        return JsonResponse(data={
            'code': 405,
            'message': 'Method not allowed'
        })

@csrf_exempt
def edit_url(request):
    import json
    # check method
    if request.method == 'PUT':
        data = json.loads(request.body)

        if not data.get('url'):
            return JsonResponse(data={
                'code': 400,
                'message': 'url is not present'
            })
        
        if not data.get('redirect_url'):
            return JsonResponse(data={
                'code': 400,
                'message': 'redirect_url is not present'
            })

        my_client = pymongo.MongoClient(settings.CONNECTION_STRING)
        shortener = my_client['urlshortener']

        urls = shortener["urls"]

        urls.update_one({ '_id': data['url'] }, { '$set': { 'redirect_url': data['redirect_url'] } })

        return JsonResponse(data={
            'code': 200,
            'message': 'Data successfully updated'
        })
    else:
        return JsonResponse(data={
            'code': 405,
            'message': 'Method not allowed'
        })
    


def visit_url(request, url_name):
    # check method
    if request.method == 'GET':

        if not url_name:
            return JsonResponse(data={
                'code': 400,
                'message': 'url is not present'
            })

        # connect with db
        my_client = pymongo.MongoClient(settings.CONNECTION_STRING)
        shortener = my_client['urlshortener']

        urls = shortener["urls"]

        find_query = urls.find_one({ 'code': url_name })

        # if code not present
        if not find_query:
            return JsonResponse(data={
                'code': 404,
                'message': 'Url not found'
            })
        
        # update visits
        urls.update_one({ 'code': url_name }, { '$set': { 'visits': find_query['visits'] + 1 } })

        return redirect(find_query['redirect_url'])
        
    else:
        return JsonResponse(data={
            'code': 405,
            'message': 'Method not allowed'
        })