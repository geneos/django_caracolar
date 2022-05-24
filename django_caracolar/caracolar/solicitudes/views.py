from django.shortcuts import render


from django.http import HttpResponse
# Create your views here.
def SolicitudesView(request):
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