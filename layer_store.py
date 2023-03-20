from __future__ import annotations
from abc import ABC, abstractmethod
from layers import invert
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList

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
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        self.queue = CircularQueue(900)
        
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if self.queue.is_full():
            return False
        else:
            self.queue.append(layer)
            return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        The argument for erase does not matter for an AdditiveLayerStore, because as per assignment brief,
          it always removes the oldest remaining layer.
          It nevertheless requires an arbitrary argument for the same reasons
        """
        # no length, return start
        if self.queue.is_empty():
            return start

 
        for i in range(self.queue.front,self.queue.length+self.queue.front):
            #first time
            if i == self.queue.front:
                color = self.queue.array[i].apply(start, timestamp, x, y)

            #after first time
            else:
                color = self.queue.array[i].apply(color, timestamp, x, y)

        return color
        

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
 
        if self.queue.is_empty(): 
            return False
        
        else: 
            self.queue.serve()
            return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        # first, we have queue
        # Queue : [R, L1, L2] -> serve (return item)
        # item -> push to stack [R, L1, L2]
        # Stack : pop -> push to another stack [L2, L1, R]

        special_stack = ArrayStack(self.queue.length)

        # the number of length, they will continue push from that we served.
        for i in range(self.queue.length):
            special_stack.push(self.queue.serve())

        # now we have stack. still need to pop and push again.
        for i in range(special_stack.length):
            self.queue.append(special_stack.pop())

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
    def __init__(self) -> None:
        self.Seq_sorted_list = ArraySortedList(9)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        # if aldy contain
        if self.Seq_sorted_list.__contains__(layer):
            return False
        
        # if there is no layer
        else:
            pass    

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass
    
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass
