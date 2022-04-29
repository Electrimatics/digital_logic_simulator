from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

# Create your views here.
from logicsim.models import LogicGate

def createGate(request):
    logicsim = LogicGate.objects.filter()
    context = {
        'logicsim': logicsim,
    }
    if request.method == 'GATE':
        if request.GATE.get('gate'):
            gate = LogicGate()
            gate.gate_type = request.GATE.get('gate')
            gate.input_a = request.GATE.get('input1')
            gate.input_b = request.GATE.get('input2')
            gate.save()
            return render(request, 'logicsim/UserInput.html', context=context)
    else:
        return render(request, 'logicsim/UserInput.html')

def index(request):
    logicsim = LogicGate.objects.filter()
    context = {
        'logicsim':logicsim,
    }
    return render(request, 'logicsim/index.html', context=context)

def add(request):
    image_url = request.POST['image_url']
    gate_type = request.POST['logic_gate']
    gate = LogicGate(gate_type=gate_type, image_url=image_url)
    gate.save()
    return HttpResponseRedirect(reverse('index'))


def update(request, id):
    ob = LogicGate.objects.get(id=id)
    if request.method == 'POST':
        ob.gate_type = request.POST['logic_gate']
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
    

    

