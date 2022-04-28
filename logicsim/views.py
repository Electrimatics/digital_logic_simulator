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

def createGate(request):

    if request.method == 'GATE':
        if request.GATE.get('gate'):
            gate = LogicGate()
            gate.gate_type = request.GATE.get('gate')
            gate.input_a = request.GATE.get('input1')
            gate.input_b = request.GATE.get('input2')
            gate.save()
            return render(request, 'logicsim/UserInput.html')
    else:
        return render(request, 'logicsim/UserInput.html')