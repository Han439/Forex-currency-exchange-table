from django.shortcuts import render
from django.http import HttpResponseServerError

from dotenv import load_dotenv
import requests
import os
# Create your views here.

load_dotenv()


def isEven(number):
    n = str(number)
    for i in range(len(n) - 1, -1, -1):
        if n[i] == '0':
            continue

        if n[i] == '.':
            break

        if int(n[i]) % 2 == 0:
            return True
        else:
            return False

    return int(number) % 2 == 0


def index(request):
    url = 'http://data.fixer.io/api/latest?'
    params = {'access_key': os.getenv('access_key')}

    # make a get request to url
    res = requests.get(url, params=params).json()

    if res['success']:
        # compile data for the template to render
        rates = {}
        increasement = 10.0002
        for k, v in res['rates'].items():
            increased_rate = round(v + increasement, 6)
            v = round(v, 6)
            rates[k] = [
                {'rate': v, 'isEven': isEven(v)},
                {'rate': increased_rate,
                    'isEven': isEven(increased_rate)}
            ]

        context = {
            'date': res['date'],
            'base': res['base'],
            'rates': rates,
        }
        return render(request, 'index.html', context=context)
    else:
        return HttpResponseServerError("<h1>The API call is not working.</h1>")
