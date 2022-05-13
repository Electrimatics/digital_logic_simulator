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
    gate = LogicGate()
    gate.gate_type = request.POST['gate']
    gate.input_a = request.POST['input1']
    gate.input_b = request.POST['input2']
    gate.image_url = request.POST['image_url']

    if(gate.input_a == "" or gate.input_b == ""):
        return HttpResponseRedirect(reverse('index'))
    gate.save()
    return HttpResponseRedirect(reverse('index'))

def update(request, id):
    ob = LogicGate.objects.get(id=id)
    if request.method == 'POST':
        ob.gate_type = request.POST['gate']
        ob.input1 = request.POST['input1']
        ob.input2 = request.POST['input2']
        ob.image_url = request.POST['image_url']
        ob.save()
        return HttpResponseRedirect(reverse('index'))
    else:   
        context = {
            'gate':ob
        }
        return render(request, 'logicsim/update.html', context=context)        

def delete(request, id):
    ob = LogicGate.objects.get(id=id)
    ob.delete()
    return HttpResponseRedirect(reverse('index'))