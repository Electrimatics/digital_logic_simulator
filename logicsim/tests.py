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
        response = render(request, 'logicsim/index.html', context=context)
