from statistics import NormalDist
from django.test import TestCase
from gates.logic_gates import *
import pprint

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

class TestXORGate(TestCase):
    def testBothTrue(self):
        gate = XORGate("XOR", "X1")
        gate.set_input('A')
        gate.set_input('B')

        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testOneFalse(self):
        gate = XORGate("XOR", "X1")
        gate.set_input('A')

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testBothFalse(self):
        gate = XORGate("XOR", "X1")
        
        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

class TestNOTGate(TestCase):
    def testTrue(self):
        gate = NOTGate("NOR", "N1")
        gate.set_input('A')

        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testFales(self):
        gate = NOTGate("NOR", "N1")

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

class TestNANDGate(TestCase):
    def testBothTrue(self):
        gate = NANDGate("NAND", "NA1")
        gate.set_input('A')
        gate.set_input('B')

        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testOneFalse(self):
        gate = NANDGate("NAND", "NA1")
        gate.set_input('A')

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testBothFalse(self):
        gate = NANDGate("NAND", "NA1")
        
        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

class TestNORGate(TestCase):
    def testBothTrue(self):
        gate = NORGate("NOR", "NO1")
        gate.set_input('A')
        gate.set_input('B')

        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testOneFalse(self):
        gate = NORGate("NOR", "NO1")
        gate.set_input('A')

        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testBothFalse(self):
        gate = NORGate("NOR", "NO1")
        
        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

class TestXNORGate(TestCase):
    def testBothTrue(self):
        gate = XNORGate("XNOR", "XN1")
        gate.set_input('A')
        gate.set_input('B')

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testOneFalse(self):
        gate = XNORGate("XNOR", "XN1")
        gate.set_input('A')

        expected_output = {'O': 0}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testBothFalse(self):
        gate = XNORGate("XNOR", "XN1")
        
        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

class TestVCC(TestCase):
    def testHigh(self):
        gate = VCC("VCC", "VCC1")

        expected_output = {'O': 1}
        gate._logic()

        self.assertEqual(gate.outputs.pins, expected_output)

    def testLow(self):
        gate = VCC("VCC", "VCC1")

        expected_output = {'O': 1}
        gate._logic()

        self.assertNotEqual(gate.outputs.pins, expected_output)

class TestGND(TestCase):
    def testHigh(self):
        gate = VCC("VCC", "VCC1")

        expected_output = {'O': 1}
        gate._logic()

        self.assertNotEqual(gate.outputs.pins, expected_output)

    def testLow(self):
        gate = VCC("VCC", "VCC1")

        expected_output = {'O': 1}
        gate._logic()

        self.assertNotEqual(gate.outputs.pins, expected_output)


class TestClock(TestCase):
    # This test sometimes fails due to a bug in the threaded clock and scanner code
    def test_clock_pulse(self):
        manager = LogicGateManager()
        clock = Clock(frequency=1)
        manager.clock = clock
        pulse_count = manager.start_clock(max_cycles=10)

        self.assertEqual(pulse_count, 10)

class TestCircuit(TestCase):
    def test_simple_circuit(self):
        manager = LogicGateManager()
        clock = Clock(frequency=1)
        manager.clock = clock

        vcc1 = VCC("VCC", "VCC1")
        vcc2 = VCC("VCC", "VCC2")
        gnd1 = GND("GND", "GND1")
        and1 = ANDGate("AND", "AND1")
        or1 = ORGate("OR", "OR1")

        manager.add_gate(vcc1)
        manager.add_gate(vcc2)
        manager.add_gate(gnd1)
        manager.add_gate(and1)
        manager.add_gate(or1)

        manager.add_connection(GatePin(vcc1.name, 'O'), GatePin(and1.name, 'A'))
        manager.add_connection(GatePin(vcc2.name, 'O'), GatePin(and1.name, 'B'))
        manager.add_connection(GatePin(and1.name, 'O'), GatePin(or1.name, 'A'))
        manager.add_connection(GatePin(gnd1.name, 'O'), GatePin(or1.name, 'B'))

        manager.start_clock(max_cycles=2)

        self.assertEqual(and1.outputs.pins, {'O': 1})
        self.assertEqual(or1.outputs.pins, {'O': 1})

class TestAdder(TestCase):
    def create_full_adder(self):
        # Setup the full adder
        manager = LogicGateManager()
        clock = Clock(frequency=1)
        manager.clock = clock

        xor1 = XORGate("XOR", "XOR1")
        xor2 = XORGate("XOR", "XOR2")
        and1 = ANDGate("AND", "AND1")
        and2 = ANDGate("AND", "AND2")
        or1 = ORGate("OR", "OR1")

        manager.add_gate(xor1)
        manager.add_gate(xor2)
        manager.add_gate(and1)
        manager.add_gate(and2)
        manager.add_gate(or1)

        manager.add_connection(GatePin(xor1.name, 'O'), GatePin(xor2.name, 'A'))
        manager.add_connection(GatePin(xor1.name, 'O'), GatePin(and1.name, 'A'))
        manager.add_connection(GatePin(and1.name, 'O'), GatePin(or1.name, 'A'))
        manager.add_connection(GatePin(and2.name, 'O'), GatePin(or1.name, 'B'))

        return (manager, xor1, xor2, and1, and2, or1)

    def test_adder_zero(self):
        manager, xor1, xor2, and1, and2, or1 = self.create_full_adder()
        A = GND("VCC", "GND1")
        B = GND("GND", "GND2")
        C = GND("GND", "GND3")

        manager.add_gate(A)
        manager.add_gate(B)
        manager.add_gate(C)

        manager.add_connection(GatePin(A.name, 'O'), GatePin(xor1.name, 'A'))
        manager.add_connection(GatePin(A.name, 'O'), GatePin(and2.name, 'A'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(xor1.name, 'B'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(and2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(xor2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(and1.name, 'B'))

        manager.start_clock(max_cycles=2)

        self.assertEqual(xor1.outputs.pins, {'O': 0})
        self.assertEqual(xor2.outputs.pins, {'O': 0})
        self.assertEqual(and1.outputs.pins, {'O': 0})
        self.assertEqual(and2.outputs.pins, {'O': 0})
        self.assertEqual(or1.outputs.pins, {'O': 0})

    def test_adder_one(self):
        manager, xor1, xor2, and1, and2, or1 = self.create_full_adder()
        A = VCC("VCC", "VCC1")
        B = GND("GND", "GND1")
        C = GND("GND", "GND2")

        manager.add_gate(A)
        manager.add_gate(B)
        manager.add_gate(C)

        manager.add_connection(GatePin(A.name, 'O'), GatePin(xor1.name, 'A'))
        manager.add_connection(GatePin(A.name, 'O'), GatePin(and2.name, 'A'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(xor1.name, 'B'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(and2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(xor2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(and1.name, 'B'))

        manager.start_clock(max_cycles=2)

        self.assertEqual(xor1.outputs.pins, {'O': 1})
        self.assertEqual(xor2.outputs.pins, {'O': 1})
        self.assertEqual(and1.outputs.pins, {'O': 0})
        self.assertEqual(and2.outputs.pins, {'O': 0})
        self.assertEqual(or1.outputs.pins, {'O': 0})

    def test_adder_two(self):
        manager, xor1, xor2, and1, and2, or1 = self.create_full_adder()
        A = VCC("VCC", "VCC1")
        B = VCC("VCC", "VCC2")
        C = GND("GND", "GND2")

        manager.add_gate(A)
        manager.add_gate(B)
        manager.add_gate(C)

        manager.add_connection(GatePin(A.name, 'O'), GatePin(xor1.name, 'A'))
        manager.add_connection(GatePin(A.name, 'O'), GatePin(and2.name, 'A'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(xor1.name, 'B'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(and2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(xor2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(and1.name, 'B'))

        manager.start_clock(max_cycles=2)

        self.assertEqual(xor1.outputs.pins, {'O': 0})
        self.assertEqual(xor2.outputs.pins, {'O': 0})
        self.assertEqual(and1.outputs.pins, {'O': 0})
        self.assertEqual(and2.outputs.pins, {'O': 1})
        self.assertEqual(or1.outputs.pins, {'O': 1})

    def test_adder_three(self):
        manager, xor1, xor2, and1, and2, or1 = self.create_full_adder()
        A = VCC("VCC", "VCC1")
        B = VCC("VCC", "VCC2")
        C = VCC("VCC", "VCC3")

        manager.add_gate(A)
        manager.add_gate(B)
        manager.add_gate(C)

        manager.add_connection(GatePin(A.name, 'O'), GatePin(xor1.name, 'A'))
        manager.add_connection(GatePin(A.name, 'O'), GatePin(and2.name, 'A'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(xor1.name, 'B'))
        manager.add_connection(GatePin(B.name, 'O'), GatePin(and2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(xor2.name, 'B'))
        manager.add_connection(GatePin(C.name, 'O'), GatePin(and1.name, 'B'))

        manager.start_clock(max_cycles=2)

        self.assertEqual(xor1.outputs.pins, {'O': 0})
        self.assertEqual(xor2.outputs.pins, {'O': 1})
        self.assertEqual(and1.outputs.pins, {'O': 0})
        self.assertEqual(and2.outputs.pins, {'O': 1})
        self.assertEqual(or1.outputs.pins, {'O': 1})

        
