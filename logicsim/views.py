from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

# Create your views here.
from logicsim.models import LogicGate

def index(request):
    logicsim = LogicGate.objects.filter()
    context = {
        'logicsim':logicsim,
    }
    return render(request, 'logicsim/index.html', context=context)

def add(request):
    fact_text = request.POST['logic_gate']
    image_url = request.POST['image_url']
    fact = LogicGate(gate_type=fact_text, image_url=image_url)
    fact.save()
    return HttpResponseRedirect(reverse('index'))

def delete(request, id):
    ob = LogicGate.objects.get(id=id)
    ob.delete()
    return HttpResponseRedirect(reverse('index'))
