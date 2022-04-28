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

    @property
    def pins(self) -> dict:
        return self._pins

    # Returns the name and status of a pin using the PinCollection[key] operation
    def __getitem__(self, name : str) -> collections.namedtuple:
        return Pin(self._pins.get(name, ('', -1)))

    # Setes the pin value using the PinCollection[key] = value operation
    def __setitem__(self, name : str, value : int) -> None:
        if abs(value) > 1:
            raise PinCollectionException(f"A pin cannot be set to value {value}. Must be 0 or 1")
        if name in self._pins:
            self._pins[name] = value
        else:
            raise PinCollectionException(f"A pin with the name {name} cannot be set as it does not exist")

    # Adds a pin to the collection with the += operator
    def __iadd__(self, name : str):
        self._pins[name] = 0
        return self

    # Removes a pin from the collection using the -= operator
    def __isub__(self, name : str):
        try:
            self._pins.pop(name)
        except KeyError:
            raise PinCollectionException(f"A pin with the name {name} cannot be removed as it does not exist")
        return self
    
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
    def set_input(self, name : str):
        self._inputs[name] = 1

    # Adds a set of pins to the output
    def add_outputs(self, outputs : list):
        for o in outputs:
            self._outputs += o

    # Sets a pin in the output
    def set_output(self, name : str):
        self._outputs[name] = 0;

    # Called with a LogicGate is printed
    def __repr__(self):
        return f"Gate '{self.name}' ({self._type}): \n\tInputs: {self._inputs} \n\tOutputs: {self._outputs}"

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

    # Method to scan for an active clock pulse. Should be put in a thread
    def _scan_for_pulse(self):
        global clock_cycles, pulse_count

        # If a clock pulse is detected, set it back to 0 to acknowledge it
        while clock_cycles > 0:
            if self._clock.send_pulse:
                with tlock:
                    pulse_count += 1
                    self._clock.send_pulse = 0

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
    def __getitem__(self, name : str) -> LogicGate:
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
