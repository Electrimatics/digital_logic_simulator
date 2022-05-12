from cgi import test
import collections
import threading
import time
from typing import Type

Pin = collections.namedtuple("Pin", ('name', 'status'))
GatePin = collections.namedtuple("GatePin", ('gate', 'pin'))
PinConnection = collections.namedtuple("PinConnection", ('o_pin', 'i_pin'))

tlock = threading.Lock()
clock_cycles = -1;
pulse_count = 0;

# TODO: Convert this to a django model

"""
Clock class to send a pulse through the logic gates at a specified frequency.

Defaults to 1 Hz
"""
class Clock(threading.Thread):
    def __init__(self, frequency = 1) -> None:
        super().__init__()
        self._clock = None
        self._frequency = frequency
        self._send_pulse = 0

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency : int) -> None:
        if(type(frequency) != int):
            raise TypeError(f"Frequency can only be of type int, not {type(frequency)}")
        self._frequency = frequency

    @property
    def send_pulse(self) -> int:
        return self._send_pulse

    @send_pulse.setter
    def send_pulse(self, pulse):
        self._send_pulse = pulse

    def run(self):
        global clock_cycles

        while(clock_cycles > 0):
            time.sleep(1/self._frequency)
            with tlock:
                self._send_pulse = 1;
            if(clock_cycles >= 0):
                clock_cycles -= 1

        self._clock = None
        
"""
Custom exception type for errors with PinCollections
"""
class PinCollectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

"""
Class that defines a set of pins that share a common function.
PinCollections store a dictionary of pins where the key is the
name of the pin and the value is the status of that pin (either
0 or 1).  Pins can be added or removed dynamically from a
PinCollection.
"""
class PinCollection:
    def __init__(self, pins : list = []) -> None:
        self._pins = dict(zip(pins, [0]*len(pins)))
        self._setpins = dict(zip(pins, [0]*len(pins)))

    @property
    def pins(self) -> dict:
        return self._pins

    @property
    def setpins(self) -> dict:
        return self._setpins

    # Returns the pin's value using the PinCollection[key] operation
    def __getitem__(self, name : str) -> collections.namedtuple:
        if name in self._pins:
            return self._pins.get(name)
        else:
            raise PinCollectionException(f"A pin with the name {name} does not exist")
        

    # Setes the pin value using the PinCollection[key] = value operation
    def __setitem__(self, name : str, value : int) -> None:
        if abs(value) > 1:
            raise PinCollectionException(f"A pin ({name}) cannot be set to value {value}. Must be 0 or 1")
        if name in self._pins:
            self._pins[name] = value
            self._setpins[name] = 1
        else:
            raise PinCollectionException(f"A pin with the name {name} cannot be set as it does not exist")

    # Adds a pin to the collection with the += operator
    def __iadd__(self, name : str):
        self._pins[name] = 0
        self._setpins[name] = 0
        return self

    # Removes a pin from the collection using the -= operator
    def __isub__(self, name : str):
        try:
            self._pins.pop(name)
            self._setpins.pop(name)
        except KeyError:
            raise PinCollectionException(f"A pin with the name {name} cannot be removed as it does not exist")
        return self

    def get_all_pins(self):
        return [Pin(key, self._pins[key]) for key in self._pins]

    def get_all_setpins(self):
        return [self._setpins[key] for key in self._setpins]

    def clear_all_setpins(self):
        for key in self._setpins.keys:
            self._setpins[key] = 0
    
    # Called when a PinCollection is printed
    def __repr__(self):
        return f"{self._pins}"

'''
Base class for all logic gates to inherit from.  This gate is a generic gate
that should not be used directly in any circuit.

Logic gates are only aware of their own inputs and produce the corresponding output.
An external manager will control signal and clock cycle management.
'''
class LogicGate:
    def __init__(self, type : str, name : str, inputs : list = [], outputs : list = []) -> None:
        self._type = type
        self._name = name
        self._inputs = PinCollection(inputs)
        self._outputs = PinCollection(outputs)

    # Sets a pin in the inputs
    def _handle_input_receive(self, pin : str) -> None:
        self._inputs[pin] = 1

    # Placeholder function for child classes to implement the gate's logic
    def _logic(self, *args, **kwargs) -> None:
        raise NotImplementedError("Logic not implemented for the generic logic gate")
    
    # Sets a pin in the output
    def _handle_output_request(self, pin : str) -> bool:
        return self._outputs[pin]

    @property
    def type(self) -> str:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name : str) -> None:
        self._name = name

    @property
    def inputs(self) -> list:
        return self._inputs

    @property
    def outputs(self) -> list:
        return self._outputs

    # Adds a set of pins to the input
    def add_inputs(self, inputs : list):
        for i in inputs:
            self._inputs += i

    # Sets a pin in the input
    def set_input(self, name : str, val : int = 1):
        self._inputs[name] = val

    # Adds a set of pins to the output
    def add_outputs(self, outputs : list):
        for o in outputs:
            self._outputs += o

    # Gets a pin's output
    def get_output(self, name : str) -> int:
        return self._outputs[name]

    # Called with a LogicGate is printed
    def __repr__(self):
        return f"Gate '{self.name}' ({self._type}): \n\tInputs: {self._inputs} \n\tOutputs: {self._outputs}"

'''
Class to implement the AND gate.

Can support an arbitrary number of inputs into 1 output.
'''
class ANDGate(LogicGate):
    def __init__(self, type: str, name: str, inputs: list = ['A', 'B'], outputs: list = ['O']) -> None:
        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        outputs = [pin.name for pin in self._outputs.get_all_pins()]
        if all([pin.status for pin in self._inputs.get_all_pins()]):
            output_val = 1
        else:
            output_val = 0

        for o in outputs:
            self._outputs[o] = output_val

'''
Class to implement the OR gate.

Can support an arbitrary number of inputs into 1 output.
'''
class ORGate(LogicGate):
    def __init__(self, type: str, name: str, inputs: list = ['A', 'B'], outputs: list = ['O']) -> None:
        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        outputs = [pin.name for pin in self._outputs.get_all_pins()]
        if any([pin.status for pin in self._inputs.get_all_pins()]):
            output_val = 1
        else:
            output_val = 0

        for o in outputs:
            self._outputs[o] = output_val

'''
Class to implement the XOR gate.

Can support 2 inputs into 1 output.
'''
class XORGate(LogicGate):
    def __init__(self, type: str, name: str, inputs: list = ['A', 'B'], outputs: list = ['O']) -> None:
        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        self._outputs['O'] = self._inputs['A'] ^ self._inputs['B']

'''
Class to implement the NOT gate.

Can support 1 input into 1 output.
'''
class NOTGate(LogicGate):
    def __init__(self, type: str, name: str, inputs: list = ['A'], outputs: list = ['O']) -> None:
        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        # This is a quick way to switch a bit from 0 -> 1 or 1 -> 0
        self._outputs['O'] = abs(self._inputs['A'] - 1)

'''
Class to implement the NAND gate.

Can support an arbitrary number of inputs into 1 output.
'''
class NANDGate(ANDGate, LogicGate):
    def __init__(self, type: str, name: str, inputs: list = ['A', 'B'], outputs: list = ['O']) -> None:
        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        super()._logic(args, kwargs)
        self._outputs['O'] = abs(self._outputs['O'] - 1)

'''
Class to implement the NOR gate.

Can support an arbitrary number of inputs into 1 output.
'''
class NORGate(ORGate, LogicGate):
    def __init__(self, type: str, name: str, inputs: list = ['A', 'B'], outputs: list = ['O']) -> None:
        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        super()._logic(args, kwargs)
        self._outputs['O'] = abs(self._outputs['O'] - 1)

'''
Class to implement the XNOR gate.

Can support 2 inputs into 1 output.
'''
class XNORGate(XORGate, LogicGate):
    def __init__(self, type: str, name: str, inputs: list = ['A', 'B'], outputs: list = ['O']) -> None:
        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        super()._logic(args, kwargs)
        self._outputs['O'] = abs(self._outputs['O'] - 1)

"""
VCC source.  Always outputs a high signal
"""
class VCC(LogicGate):
    def __init__(self, type: str, name: str, inputs: list = [], outputs: list = ['O']) -> None:
        if len(inputs) > 0:
            raise LogicGateManagerException(f"VCC gate does not take any inputs")

        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        self._outputs['O'] = 1

"""
GND source.  Always outputs a low signal
"""
class GND(LogicGate):
    def __init__(self, type: str, name: str, inputs: list = [], outputs: list = ['O']) -> None:
        if len(inputs) > 0:
            raise LogicGateManagerException(f"GND gate does not take any inputs")

        super().__init__(type, name, inputs, outputs)

    def _logic(self, *args, **kwargs) -> None:
        self._outputs['O'] = 0

"""
Custom exception type for errors with PinCollections
"""
class LogicGateManagerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


"""
Class that manages a collection of LogicGates.  LogicGate connections are stored
in two ways: logical connections and a connection mapping.  The logical connections
are the mechanims that will allow a gate to send or receive input from another gate
(not yet implemented).  The connection mapping is a dictionary that describes how
gates are connected.  This is a dictionary of characters, which will make storing
it in a database easier than the logical connections.  The connection mapping can
also be used to re-create the logical connections.
"""
class LogicGateManager:
    def __init__(self) -> None:
        self._gateMapper = {}
        self._gateKeeper = {}
        self._clock = None

    @property
    def connections(self) -> dict:
        return self._gateMapper

    @property
    def clock(self) -> list:
        return self._clocks

    @clock.setter
    def clock(self, clock : Clock):
        if type(clock) != Clock:
            raise TypeError(f"A clock must be of type Clock, not {type(clock)}")
        self._clock = clock

    # Method to run the circuit simulator. 
    def _run_logic(self):
        complete = False
        limiter = 1000
        counter = 0

        # Continue to run the circuit until all of the circuit inputs are satisfied
        while not complete and counter < limiter:
            complete = True

            # Go through all of the gates in the circuit and run their logic if all input
            # pins were satisfied
            for name, gate in self._gateKeeper.items():
                if all(gate.inputs.get_all_setpins()):
                    gate._logic()

                    # Gather the gate's output gate and pin connections and send the signal
                    # to those gates (either 0 or 1, depending on the output pin)
                    for gate, connection in self._gateMapper[name].items():
                        for conn in connection:
                            self._gateKeeper[gate].set_input(conn.i_pin, self._gateKeeper[name].get_output(conn.o_pin))

                # This gate's inputs have not been satisfied yet
                else:
                    complete = False

            # "Runaway" limiter for circuits that will never satisfy all inputs
            counter += 1

    # Method to scan for an active clock pulse. Should be put in a thread
    def _scan_for_pulse(self):
        global clock_cycles, pulse_count

        # If a clock pulse is detected, set it back to 0 to acknowledge it
        while clock_cycles > 0:
            if self._clock.send_pulse:
                with tlock:
                    pulse_count += 1
                    self._clock.send_pulse = 0
                self._run_logic()

    # Start the clock and the associated scanner to scan for clock pulses. These pulses will be sent into
    # the circuit
    def start_clock(self, max_cycles = -1):
        if not self._clock:
            raise LogicGateManagerException(f"No clock is attached to this LogicGateManager")

        global clock_cycles, pulse_count
        clock_cycles = max_cycles

        scanner = threading.Thread(target=self._scan_for_pulse, args=())
        scanner.start()
        self._clock.start()

        self._clock.join()
        scanner.join()

        return pulse_count

    # Returns a LogicGate with the specified name using the LogicGateManager[key] operation
    def __getitem__(self, name : str):
        return self._gateKeeper.get(name)

    # Adds a gate to the manager
    def add_gate(self, gate) -> None:
        self._gateKeeper.update({gate.name: gate})
        self._gateMapper.update({gate.name:{}})

    # Removes a gate from the manager
    def remove_gate(self, name):
        self._gateKeeper.pop(name)
        self._gateMapper.pop(name)

    # Adds a connection (both logical and mapping) between two pins on gates
    def add_connection(self, output_gate : GatePin, input_gate : GatePin):
        if output_gate.gate not in self._gateMapper or input_gate.gate not in self._gateMapper:
            raise LogicGateManagerException(f"Cannot create a conneection between {output_gate.gate} and {input_gate.gate} because at least one gate does not exist")

        connections = self._gateMapper.get(output_gate.gate).get(input_gate.gate, [])
        connections.append(PinConnection(output_gate.pin, input_gate.pin))
        self._gateMapper[output_gate.gate].update({input_gate.gate: connections})

    # Called when a LogicGateManager is printed
    def __repr__(self):
        gate_string = ''
        for gate in self._gateMapper:
            gate_string += f"{self._gateKeeper[gate]}"

            for connection in self._gateMapper[gate]:
                pin_connections = [f"{pin.o_pin} -> {pin.i_pin}" for pin in self._gateMapper[gate][connection]]
                gate_string += f"\n\tConnection to '{connection}' on pins: {pin_connections}"

            gate_string += "\n"
        return gate_string

# def test_simple_circuit():
#     manager = LogicGateManager()
#     clock = Clock(frequency=1)
#     manager.clock = clock

#     vcc1 = VCC("VCC", "VCC1")
#     vcc2 = VCC("VCC", "VCC2")
#     gnd1 = GND("GND", "GND1")
#     and1 = ANDGate("AND", "AND1")
#     or1 = ORGate("OR", "OR1")

#     manager.add_gate(vcc1)
#     manager.add_gate(vcc2)
#     manager.add_gate(gnd1)
#     manager.add_gate(and1)
#     manager.add_gate(or1)

#     manager.add_connection(GatePin(vcc1.name, 'O'), GatePin(and1.name, 'A'))
#     manager.add_connection(GatePin(vcc2.name, 'O'), GatePin(and1.name, 'B'))
#     manager.add_connection(GatePin(and1.name, 'O'), GatePin(or1.name, 'A'))
#     manager.add_connection(GatePin(gnd1.name, 'O'), GatePin(or1.name, 'B'))

#     manager.start_clock(max_cycles=2)

# test_simple_circuit()