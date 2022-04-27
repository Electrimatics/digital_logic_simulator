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

    def test_update_element(self):
      and_gate = LogicGate(gate_type="and", image_url=".jpg")
      and_gate.save()

      self.assertEqual(and_gate.gate_type, "and")
      
      and_gate.gate_type = "or"
      and_gate.image_url = ".png"
      and_gate.save()

      self.assertEqual(and_gate.gate_type, "or")
      self.assertEqual(and_gate.image_url, ".png")

      def test_delete_element(self):
        and_gate = LogicGate(gate_type="and", image_url=".jpg")
        and_gate.save()

        self.assertEqual(len(LogicGate.objects.all()), 1)
        
        and_gate.delete()

        self.assertEqual(len(LogicGate.objects.all()), 0)