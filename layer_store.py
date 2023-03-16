from __future__ import annotations
from abc import ABC, abstractmethod
from layers import invert
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
        self.special_switch = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if self.layer == None or self.layer.bg != layer.bg:
            self.layer = layer
            return True
        else:
            return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
 
        # Here we can see that there is no layer currently applied, 
        # and so the color we give as input is also the color we receive as output. 
        # You can look through the other tests and see how the layers modify the input color. 

        if self.layer == None:
            return start


        if self.special_switch == True:
            new_bg = (self.layer.bg[0]-start[0], self.layer.bg[1]-start[1], self.layer.bg[2]-start[2])

            return invert.apply(new_bg,timestamp,x,y)
            
        
        else:
            return self.layer.apply(start,timestamp,x,y)
        

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

        everytiime special is called, make a random variable, set it to true.
        in get color, I check if the value is true, then after I apply the layer, then I invert if the value is ture
        otherwise, get_color.
        """

        if self.special_switch == True:
            self.special_switch = False
        
        else:
            self.special_switch = True


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
