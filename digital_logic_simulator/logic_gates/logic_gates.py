import collections
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

    def __getitem__(self, name : str) -> collections.namedtuple:
        return Pin(self._pins.get(name, ('', -1)))

    def __setitem__(self, name : str, value : int) -> None:
        if abs(value) > 1:
            raise PinCollectionException(f"A pin cannot be set to value {value}. Must be 0 or 1")
        if self._pins.has_key(name):
            self._pins[name] = value
        else:
            raise PinCollectionException(f"A pin with the name {name} cannot be set as it does not exist")

    def __iadd__(self, name : str) -> None:
        self._pins[name] = 0

    def __isub__(self, name : str) -> None:
        try:
            self._pins.pop(name)
        except KeyError:
            raise PinCollectionException(f"A pin with the name {name} cannot be removed as it does not exist")
    
    def __repr__(self):
        return f"{self._pins}"

'''
Base class for all logic gates to inherit from.  This gate is a generic gate
that should not be used directly in any circuit.

Logic gates are only aware of their own inputs and produce the corresponding output.
An external manager will control signal and clock cycle management.
'''
class LogicGate:
    def __init__(self, name : str, inputs : list = [], outputs : list = []) -> None:
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
        return f"Logic gate '{self.name}' \n\tInputs: {self._inputs} \n\tOutputs: {self._outputs}"

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
        self._gates = {}

    @property
    def gates(self):
        return self._gates;

    def __iadd__(self, gate : LogicGate) -> None:
        if type(gate) != LogicGate:
            raise TypeError(F"Only gates may be added to the logic gate manager, not {type(gate)}")
        self._gates.update({gate.name:{}})

    def __isub__(self, gate : LogicGate) -> None:
        if type(gate) != LogicGate:
            raise TypeError(F"Only gates may be removed to the logic gate manager, not {type(gate)}")
        self._gates.pop(gate.name)

    def add_connection(self, output_gate : GatePin, input_gate : GatePin):
        if not self._gates.haskey(input_gate.gate) or not self._gates.haskey(output_gate.gate):
            raise LogicGateManagerException(f"Cannot create a conneection between {output_gate.gate} and {input_gate.gate} because at least one gate does not exist")

        connections = self._gates.get(input_gate.gate).get(output_gate.gate)
        self._gates[input_gate.gate].update({output_gate.gate: connections.append(PinConnection(output_gate.pin, input_gate.pin))})

    def __repr__(self):
        return ''

def main():
    gate1 = LogicGate("G1", ['A', 'B'], ['O'])
    gate2 = LogicGate("G2", ['A', 'B'], ['O'])
    print(gate1)
    print(gate2)

main()
