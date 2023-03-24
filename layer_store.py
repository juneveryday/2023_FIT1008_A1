from __future__ import annotations
from abc import ABC, abstractmethod
from layers import *
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem


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
    The SetLayerStore simply remembers the last layer that was applied, and applies that.

    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    
    def __init__(self) -> None:
        self.layer = None

        # we will make special_switch for sepcial function.
        # so, when special is called, special switch will become True.
        self.special_switch = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """

        # if layer is None or layer.bg is different with layer.bg,
        # we will add the layer to our layer.
        # For example : s.add(black) 
        # '.bg' is from layer_util.py tuple[int,int,int] format.
         
        if self.layer == None or self.layer.bg != layer.bg:
            self.layer = layer
            return True
        
        # if self.layer.bg and layer.bg is same, then we will just return False.
        else:
            return False
    

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
 
        # if self.layer is None, return start.
        if self.layer == None:
            return start


        # if this get_color function is called after we used special function.
        if self.special_switch == True:

            # new_bg will calculate each index from tuple.
            # (a,b,c) - (x,y,z) -> (a-x), (b-y), (c-z)
            new_bg = (self.layer.bg[0]-start[0], self.layer.bg[1]-start[1], self.layer.bg[2]-start[2])

            # it will return the value after we apply to new_bg.
            return invert.apply(new_bg,timestamp,x,y)
            
        # if special_switch is not called, just apply start.
        else:
            return self.layer.apply(start,timestamp,x,y)
        

    def erase(self, layer: Layer) -> bool:
        """
        The erase function returns true if the LayerStore was actually changed.

        For example: erase(invert)
        """

        # If self.layer is None, the LayerStore wont be changed anything.
        # Therefore, we will return False.
        if self.layer == None:
            return False
        
        # If self.layer is not None, it means, the LayerStore will be actually changed.
        # Therefore, we will make our layer empty(None), then we will return True. 
        else:
            self.layer = None
            return True

    def special(self):  
        """
        Special mode. Different for each store implementation.

        The special mode on a SetLayerStore keeps the current layer,
        but always applies an inversion of the colours after the layer has been applied. 
        So if previously your Layer output (100, 100, 100) , then it would now output (155, 155, 155).
        """

        #If special function is called. We will make the switch is False again.
        #So that, If the special function is called again, we can use this switch repeated.
        #After that, we will calculate in the function get_color. 

        # If special function is called already, make it False.
        if self.special_switch == True:
            self.special_switch = False

        # If special function is just called, switch(False) make it True.
        else:
            self.special_switch = True

class AdditiveLayerStore(LayerStore):
    """
    The Additive Layer Store simply applies layers consecutively. 
    Whenever a store has a collection of layers,
    these layers are applied one-by-one,
    from earliest added to latest added.


    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    # I used QueueADT which is called in CircularQueue()
    # so that I can use FIFO(First In First Out)
    def __init__(self) -> None:
        # Since multiple copies of the same layer can be used in this mode,
        # make the capacity of the store at least 100 times the number of layers.
        # Therefore, The Maximum of CircularQueue will be 9*100 = 900.
        self.queue = CircularQueue(900)
        
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        For example, s.add(black)
        """

        # First, I am going to check the queue is full or not.
        # Because if queue is full, we need to return False cuz we cannot add anymore.
        if self.queue.is_full():
            return False
        
        # If the layer is not full, it means I stll can add the layer to our queue.
        # Therefore, I am going to add with the function in array, called append.
        # Also, I will return True cuz the LayerStore will be actaully changed.
        else:
            self.queue.append(layer)
            return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        # If the queue is empty, I will return start.
        if self.queue.is_empty():
            return start
 

        # From the "queue.front" to "queue.front+queue.length"
        # It means we will check all the value that is not empty.
        for i in range(self.queue.front,self.queue.length+self.queue.front):
            # First time will be start.
            if i == self.queue.front:
                color = self.queue.array[i].apply(start, timestamp, x, y)

            # After first time, we will keep apply the last color to current color.
            else:
                color = self.queue.array[i].apply(color, timestamp, x, y)

        # Return color
        return color
        

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer, Returns true if the LayerStore was actually changed.
        
        The argument for erase does not matter for an AdditiveLayerStore,
        because as per assignment brief, it always removes the oldest remaining layer.
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
        self.list = ArraySortedList(9)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        for i in range(self.list.length):
            index = self.list[i].key #it will be index in list
            if layer.index == index: #lighten, darken etc
                return False
            
        # if there is no layer in list
        new_item = ListItem(layer, layer.index)
        self.list.add(new_item)
        return True
        

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        """
        Returns the colour this square should show, given the current layers.
        """

        # if there is nothing, then return start color
        if self.list.length == 0:
            return start
        
        # the number of length of list.
        for i in range(len(self.list)):
            layer = self.list[i].value
            #layer is (index=0, apply=<function rainbow at 0x105313ba0>, name='rainbow', bg=(200, 0, 120)
            #check this is first or not.
            if i == 0:
                color = layer.apply(start, timestamp, x, y)
            #if not first, keep apply.
            else:   
                color = layer.apply(color, timestamp, x, y)
        return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        #the number of length of list.
        for i in range(len(self.list)):
            # if key is same value with index. delete at index.
            if self.list[i].key == layer.index:
                self.list.delete_at_index(i)
                return True
        return False

    def special(self):  
        """
        Special mode. Different for each store implementation.
        """
        # I am going to make new sorted list, the length is based on self.list.length
        alpha_sort = ArraySortedList(self.list.length)
        if len(self.list) > 0 : 
        # the number of length of list.
            for i in range(self.list.length):
                list_item = self.list[i]
                
                #black, darken, rainbow etc 
                key = list_item.value.name 
                
                #layer
                value = list_item.value

                #based on the sort, add into alpha_sort
                # so the value will be sorted with alphabetically.  
                alpha_sort.add(ListItem(value, key))
                
            # if the number of length is odd number
            if len(alpha_sort) % 2 == 1:
                layer = alpha_sort[len(alpha_sort)//2].value

            # if the number of length is even number
            else:
                layer = alpha_sort[(len(alpha_sort)//2)-1].value
            
            # erase that layer.
            self.erase(layer)
