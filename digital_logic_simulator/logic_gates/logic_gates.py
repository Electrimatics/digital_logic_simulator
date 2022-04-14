import collections
from typing import Type

Pin = collections.namedtuple("Pin", ('name', 'status'))


class PinCollectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PinCollection:
    def __init__(self, pins : list[str] = []) -> None:
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

'''
Base class for all logic gates to inherit from.  This gate is a generic gate
that should not be used directly in any circuit.

Logic gates are only aware of their own inputs and produce the corresponding output.
An external manager will control signal and clock cycle management.
'''
class LogicGate:
    def __init__(self, name : str, inputs : list[str] = [], outputs : list[str] = []) -> None:
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
    def inputs(self) -> list[Pin]:
        return self._inputs

    @property
    def outputs(self) -> list[Pin]:
        return self._outputs

    def add_inputs(self, inputs : list[str]):
        for i in inputs:
            self._inputs += i

    def add_outputs(self, outputs : list[str]):
        for o in outputs:
            self._outputs += o

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
        self._gates.append(gate)

    def __isub__(self, gate : LogicGate) -> None:
        if type(gate) != LogicGate:
            raise TypeError(F"Only gates may be added to the logic gate manager, not {type(gate)}")
        self._gates.remove(gate)

    
