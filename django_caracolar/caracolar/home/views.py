from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def HomeView(request):
    ''' Vista para ver los tipos de servicios ofrecidos. '''
    # tmp_ofertas = open("ofertas.html", 'w')
    # template = Template(tmp_ofertas)
    # tmp_ofertas.close()
    # contexto = Context()
    # documento = template.render(contexto)
    # data = {
    #     "name": "Pepo"
    # }
    # return render(request, "index.html", data)
    return HttpResponse('vista')

def HomeCategoryView(request):
    ''' Vista para ver los tipos de servicios ofrecidos. '''
    # tmp_ofertas = open("ofertas.html", 'w')
    # template = Template(tmp_ofertas)
    # tmp_ofertas.close()
    # contexto = Context()
    # documento = template.render(contexto)
    # data = {
    #     "name": "Pepo"
    # }
    # return render(request, "index.html", data)
    return HttpResponse('vista de categorias')
