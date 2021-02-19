from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import json
import requests

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from authy.forms import SignUpForm
# Create your views here.
def index(request):
    
    response = call_api('GET', 'totals')
    world_data = response.json()
    print(world_data)
    
    countries_data = []
    # aqui llamariamos a la api para almacenar el listado de los paises
    countries_list = ['Afghanistan']
    # for que recorreria el json creado anteriormente para hacer get a la api con el nombre de cada pais 
    for country in countries_list:
        countries_data.append(call_api('GET', 'country', country).json())
    list_abc = []
    for country in countries_data:
        for a_country in country:
            list_abc.append(a_country)
    
    context = {
        'world_data': world_data[0],
        'countries_data': list_abc,
    }



    
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

#funcion que llama al endpoint de la api
def call_api(http_method, endpoint, country_name=''):
    headers = {
    'x-rapidapi-key': "4124ae810dmshe3719b1d87ccef7p1de791jsn25045c93e3d5",
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }
    url = "https://covid-19-data.p.rapidapi.com/" + endpoint
    
    
    return requests.request(http_method, url, headers=headers, params={"name":country_name})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})