from django.test import TestCase
import json
from gates.logic_gates import *

class TestGenericLogicGate(TestCase):
    def test_generic_gate_creation(self):
        gate_manager = LogicGateManager()
        name = "G1"
        type = "GATE"
        inputs=['A', 'B']
        outputs=['O']
        gate_manager.add_gate(type, name, inputs, outputs)

        self.assertEqual(gate_manager[name].type, type)
        self.assertEqual(gate_manager[name].inputs.pins, dict(zip(inputs, [0]*len(inputs))))
        self.assertEqual(gate_manager[name].outputs.pins, dict(zip(outputs, [0]*len(outputs))))
