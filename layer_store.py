from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self) -> None:
        self.layer = None

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        # 만약 기존 레이어가 추가하는 것과 같다면 true가 나오면 안된다
        
        if self.layer == None or self.layer.bg != layer.bg:
            return True
        else:
            return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        self.start = start
        self.timestamp = timestamp
        self.x = x
        self.y = y

        #how we know the format of parameter of .apply?
        return self.layer.apply(self.start,self.timestamp,self.x,self.y)

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if self.layer == None:
            return False
        else:
            self.layer = None
            return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        #The special mode keeps the current layer,
        #  but always applies an inversion of the colours after the layer has been applied. 
        # So if previously your Layer output (100, 100, 100) , 
        # then it would now output (155, 155, 155).
        #  See tests/test_layer_stores/test_set_layer.py for examples of this at play.

        #layer_util 에서 class Layer 을 써야하는 것 같음
        pass

class AdditiveLayerStore(LayerStore):
    #stack_adt or queue_adt
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    pass

class SequenceLayerStore(LayerStore):
    # ArraySortedList
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    pass
