from unittest import TestCase
from urllib.request import Request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import urllib.request

from django.urls import reverse

# Create your views here.
from logicsim.models import LogicGate

class logicsimTest(TestCase):
    def test_add_element(self):
        logicsim = LogicGate.objects.filter()
        request = HttpRequest()
        request.method = 'GET'
        context = {
          'logicsim':logicsim,
        }
        return render(request, 'logicsim/displaytest.html', context=context)

    def test_add_Button_element(self):
        logicsim = LogicGate.objects.filter()
        request = HttpRequest()
        request.method = 'GET'
        context = {
           'logicsim':logicsim,
        }
        return render(request, 'logicsim/buttonTest.html', context=context)

    def test_user_input(self):
        logicsim = LogicGate.objects.filter()
        request = HttpRequest()
        request.method = 'GET'
        context = {
           'logicsim':logicsim,
        }
        return render(request, 'logicsim/UserInput.html', context=context)

    def test_add_UserInput(self):
        logicsim = LogicGate.objects.filter()
        request = HttpRequest()
        request.method = 'GET'
        context = {
           'logicsim':logicsim,
        }
        return render(request, 'logicsim/UserInput.html', context=context)

    def test_add_data(self):
        gate = LogicGate()
        return LogicGate.objects.filter(gate_id = 1).exists()

    def test_update_element(self):
        and_gate = LogicGate(gate_type="AND", input_a=1, input_b=2, image_url=".jpg")
        and_gate.save()
        self.assertEqual(and_gate.gate_type, "AND")
       
        and_gate.gate_type = "or"
        and_gate.input_a = 2
        and_gate.input_b = 3
        and_gate.image_url = ".png"
        and_gate.save()
        self.assertEqual(and_gate.gate_type, "or")
        self.assertEqual(and_gate.input_a, 2)
        self.assertEqual(and_gate.input_b, 3)
        self.assertEqual(and_gate.image_url, ".png")

    def test_delete_element(self):
        and_gate = LogicGate(gate_type="and", image_url=".jpg")
        and_gate.save()
        self.assertEqual(len(LogicGate.objects.all()), 1)
        
        and_gate.delete()
        self.assertEqual(len(LogicGate.objects.all()), 0)

    def test_add_database(self):
        gate = LogicGate(gate_type="or gate", image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Or-gate-en.svg/500px-Or-gate-en.svg.png?20060601172209")
        gate.save()
        #Check to see if data saved properly
        self.assertEqual("or gate", gate.gate_type)
        self.assertEqual("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Or-gate-en.svg/500px-Or-gate-en.svg.png?20060601172209", gate.image_url)
        gate.delete()

        gate2 = LogicGate(gate_type = "", image_url = "")
        gate2.save()
        #Check to see if gates save separately
        self.assertEqual("", gate2.gate_type)
        self.assertEqual("", gate2.image_url)
        self.assertNotEqual("", gate.image_url)

        gate3 = LogicGate(gate_type = "", image_url = "")
        gate3.save()
        #Check to see if two gates have same gate type
        self.assertEqual(gate3.gate_type, gate2.gate_type)
        #Check to see if gates are independent
        self.assertNotEqual(gate2.__str__, gate3.__str__)
        
        gate2.delete()
        gate3.delete()

        #Try with no additional fields
        gate4 = LogicGate()
        gate4.save()
        self.assertNotEqual(gate4.gate_type, "or gate")
        self.assertEqual(gate4.gate_type, "")
        gate4.delete()


