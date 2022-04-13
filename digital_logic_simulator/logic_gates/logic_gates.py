import collections
from typing import Type

Pin = collections.namedtuple("Pin", ('name', 'status'))

class Clock:
    def __init__(self) -> None:
        self.frequency = 1000000

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
'''
class LogicGate:
    def __init__(self, name : str) -> None:
        self._name = name
        self._inputs = None
        self._outputs = None

    def _handle_input_receive(self):
        pass

    def _handle_output_signal(self):
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name : str) -> None:
        self._name = name

    @property
    def inputs(self) -> list[Pin]:
        return self._inputs

    @inputs.setter
    def inputs(self, input : Pin) -> None:
        self += input

    def __iadd__(self, pin : Pin) -> None:
        if type(pin) != Pin:
            raise TypeError(f"LogicGates can only add Pin types, not {type(pin)}")
        self._name.append(pin)

    @property
    def outputs(self) -> list[Pin]:
        return self._outputs

    @outputs.setter
    def outputs(self, output : Pin) -> None:
        self -= output

    def __isub__(self, pin : Pin) -> None:
        if type(pin) != Pin:
            raise TypeError(f"LogicGates can only remove Pin types, not {type(pin)}")
