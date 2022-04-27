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

        expected_input = dict(zip(inputs, [0]*len(inputs)))
        expected_output = dict(zip(outputs, [0]*len(outputs)))

        gate_manager.add_gate(type, name, inputs, outputs)
        self.assertEqual(gate_manager[name].type, type)
        self.assertEqual(gate_manager[name].inputs.pins, expected_input)
        self.assertEqual(gate_manager[name].outputs.pins, expected_output)

    def test_generic_gate_set_pin(self):
        gate_manager = LogicGateManager()
        name = "G1"
        type = "GATE"
        inputs=['A', 'B']
        outputs=['O']

        expected_input = dict(zip(inputs, [0]*len(inputs)))
        expected_input['A'] = 1
        expected_output = dict(zip(outputs, [0]*len(outputs)))

        gate_manager.add_gate(type, name, inputs, outputs)
        gate_manager[name].set_input("A");
        self.assertEqual(gate_manager[name].type, type)
        self.assertEqual(gate_manager[name].inputs.pins, expected_input)
        self.assertEqual(gate_manager[name].outputs.pins, expected_output)

    def test_generic_gate_add_connection(self):
        gate_manager = LogicGateManager()
        name1 = "G1"
        name2 = "G2"
        type = "GATE"
        inputs=['A', 'B']
        outputs=['O']

        expected_connections = {'G1': {'G2': [PinConnection(o_pin='O', i_pin='A')]}, 'G2': {}}

        gate_manager.add_gate(type, name1, inputs, outputs)
        gate_manager.add_gate(type, name2, inputs, outputs)
        gate_manager.add_connection(GatePin(name1, 'O'), GatePin(name2, 'A'))

        self.assertEqual(gate_manager.connections, expected_connections)

class TestANDGate(TestCase):
    def testBothTrue(self):
        gate = ANDGate("AND", "A1")
        gate.set_input('A')
        gate.set_input('B')

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testOneFalse(self):
        gate = ANDGate("AND", "A1")
        gate.set_input('A')

        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testBothFalse(self):
        gate = ANDGate("AND", "A1")
        
        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

class TestORGate(TestCase):
    def testBothTrue(self):
        gate = ORGate("OR", "O1")
        gate.set_input('A')
        gate.set_input('B')

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testOneFalse(self):
        gate = ORGate("OR", "O1")
        gate.set_input('A')

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testBothFalse(self):
        gate = ORGate("OR", "O1")
        
        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)
