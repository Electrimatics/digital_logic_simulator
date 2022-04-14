import collections
from distutils.log import Log
import logging
from typing import Type

Pin = collections.namedtuple("Pin", ('name', 'status'))
GatePin = collections.namedtuple("GatePin", ('gate', 'pin'))
PinConnection = collections.namedtuple("PinConnection", ('o_pin', 'i_pin'))

# TODO: Convert this to a django model

class PinCollectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PinCollection:
    def __init__(self, pins : list = []) -> None:
        self._pins = dict(zip(pins, [0]*len(pins)))

    @property
    def pins(self) -> dict:
        return self._pins

    def __getitem__(self, name : str) -> collections.namedtuple:
        return Pin(self._pins.get(name, ('', -1)))

    def __setitem__(self, name : str, value : int) -> None:
        if abs(value) > 1:
            raise PinCollectionException(f"A pin cannot be set to value {value}. Must be 0 or 1")
        if self._pins.has_key(name):
            self._pins[name] = value
        else:
            raise PinCollectionException(f"A pin with the name {name} cannot be set as it does not exist")

    def __iadd__(self, name : str):
        self._pins[name] = 0
        return self

    def __isub__(self, name : str):
        try:
            self._pins.pop(name)
        except KeyError:
            raise PinCollectionException(f"A pin with the name {name} cannot be removed as it does not exist")
        return self
    
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

    def _handle_input_receive(self, pin : str) -> None:
        self._inputs[pin] = 1

    def _logic(self, *args, **kwargs) -> None:
        raise NotImplementedError("Logic not implemented for the generic logic gate")
    
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

    def add_inputs(self, inputs : list):
        for i in inputs:
            self._inputs += i

    def add_outputs(self, outputs : list):
        for o in outputs:
            self._outputs += o

    def __repr__(self):
        return f"Gate '{self.name}' ({self._type}): \n\tInputs: {self._inputs} \n\tOutputs: {self._outputs}"

class LogicGateManagerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


# idea - each gate has a unique name in the dictionary
# the value is a sub dictionary with each of the gates it connects to
# each connected gate's value is a list of the pin mappings
# {G1:
#   {G2: [(p1, p1), (p2, p3)]
#    ...
#   }
# ...
# }
class LogicGateManager:
    def __init__(self) -> None:
        self._gateMapper = {}
        self._gateKeeper = {}

    @property
    def gates(self):
        return self._gateMapper;

    def __getitem__(self, name : str) -> LogicGate:
        return self._gateKeeper.get(name)

    def add_gate(self, type : str, name : str, inputs : list = [], outputs : list = []) -> None:
        self._gateKeeper.update({name: LogicGate(type, name, inputs, outputs)})
        self._gateMapper.update({name:{}})

    def remove_gate(self, name):
        self._gateKeeper.pop(name)
        self._gateMapper.pop(name)

    def add_connection(self, output_gate : GatePin, input_gate : GatePin):
        if output_gate.gate not in self._gateMapper or input_gate.gate not in self._gateMapper:
            raise LogicGateManagerException(f"Cannot create a conneection between {output_gate.gate} and {input_gate.gate} because at least one gate does not exist")

        connections = self._gateMapper.get(output_gate.gate).get(input_gate.gate, [])
        connections.append(PinConnection(output_gate.pin, input_gate.pin))
        self._gateMapper[output_gate.gate].update({input_gate.gate: connections})

    def __repr__(self):
        gate_string = ''
        for gate in self._gateMapper:
            gate_string += f"{self._gateKeeper[gate]}"

            for connection in self._gateMapper[gate]:
                pin_connections = [f"{pin.o_pin} -> {pin.i_pin}" for pin in self._gateMapper[gate][connection]]
                gate_string += f"\n\tConnection to '{connection}' on pins: {pin_connections}"

            gate_string += "\n"
        return gate_string

def main():
    gate_manager = LogicGateManager()
    gate_manager.add_gate(type='GATE', name="G1", inputs=['A', 'B'], outputs=['O'])
    gate_manager.add_gate(type='GATE', name="G2", inputs=['A', 'B'], outputs=['O'])

    gate_manager.add_connection(GatePin("G1", 'O'), GatePin("G2", 'A'))
    gate_manager.add_connection(GatePin("G1", 'O'), GatePin("G2", 'B'))

    print(gate_manager)

main()
