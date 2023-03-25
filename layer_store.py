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

        Time complexity : O(1)
        There is no loop and no reversive calls.
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

        Time complexity : O(1)
        There is no loop and no reversive calls.)
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

        Time complexity : O(1)
        There is no loop and no reversive calls.
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
        
        Time complexity : O(1)
        There is no loop and no reversive calls.
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

        Time complexity : O(1)
        There is no loop and no reversive calls.
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

        Time complexity: O(n), where n is the length of the queue. 

        The "get_color" function iterates over each element in the queue and applies a function to it. 
        Furthermore, the complexity of applying a function to an element is O(1).
        Therefore, the overall time complexity of the function is O(n).
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
        The erase action with this layer, Returns true if the LayerStore was changed.
        
        The argument for erase does not matter for an AdditiveLayerStore,
        because as per assignment brief, it always removes the oldest remaining layer.

        Time complexity: O(1)

        The function removes the oldest remaining layer from the queue.
        It can be done in constant time regardless of the size of the queue.
        """

        # If the queue is empty, there is nothing to erase.
        # Therefore return False.
        if self.queue.is_empty(): 
            return False
        
        # Else, That means we need to erase the latest one.
        # Therefore we will return true after we serve.
        else: 
            self.queue.serve()
            return True

    def special(self):
        """
        Special mode. Different for each store implementation.

        It uses the stack to create a reversed queue.

        1. it serves from the self.queue and push to special_stack.

        2. the index in special_stack will be pop, and appended again to self.queue

        Time complexity: O(n), where n is the length of the queue.

        The "special" iterates each element in the queue. 
        The time complexity of each operation is O(1).
        Therefore, the overall time complexity of the function is O(n).
        """

        # Temporary stack, making for reverse array. Last In First Out.
        special_stack = ArrayStack(self.queue.length)

        # The number of length, they will continue push to stack from that we served in queue.
        for i in range(self.queue.length):
            special_stack.push(self.queue.serve())

        # Now we have stack.
        # Again, need to append to queue from the stack we pop.
        # Therefore, it will be reversed queue. 
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

    # I used the ArraySortedList for SequenceLayerStore.
    # The maximum_capacity will be 9, cuz the the number of layers is total 9.
    def __init__(self) -> None:
        self.list = ArraySortedList(9)



    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Time complexity: O(n), where the n is length of the list.

        "add" function iteraties each element in the list and performs on each element.
        Each time complexity of operation is O(1).
        Therefore, the overall time complexity is O(n).
        """

        for i in range(self.list.length):
            
            # Make the "key_value" for check list[i].key
            # It will be index in list
            key_value = self.list[i].key 

            # If layer.index is equal to key_value(index),
            # it means that the layer is already exist in the list.
            # Therefore, it will return False.
            if layer.index == key_value: 
                return False
            
        # if there is no layer in list
        # it will make ListItem called new_item so that it will be added to self.list
        new_item = ListItem(layer, layer.index)
        self.list.add(new_item)

        #LayerStore is actually changed, so return True.
        return True
        

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        """
        Returns the colour this square should show, given the current layers.

        Time complexity: O(n), where n is length of the list.

        The "get_color" function iterates each element in the list. 
        The time complexity of element is O(1).
        Therefore, the overall time complexity is O(n).

        """

        # If there is nothing (checked with length), then return start color.
        if self.list.length == 0:
            return start
        
        # The number of length of list.
        for i in range(len(self.list)):
            layer = self.list[i].value
            
            # If this loop is first time, color will be applied with "start"
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

        Time complexity: O(n), where n is length of the list.

        The "erase" function iterates each element in the list.
        It check one by one, the number of element in the list.
        Also, the each operation time complexity is O(1).

        Therefore, the overall time complexity is O(1).
        """

        #The number of length of list.
        for i in range(len(self.list)):

            # If key is same value with index. delete at index.
            if self.list[i].key == layer.index:

                #As using the funtion "delete_at_index",
                #  the index i+1 will be shuffle_left.
                self.list.delete_at_index(i)

                return True
            
        return False

    def special(self):  
        """
        Special mode. Different for each store implementation.

        Time complexity: O(n log n), where n is the length of the list.
        
        n : it checks the number of elements in the list by n.
        log n : this "special" function compare elements in the list to each other and make it sort in _index_to_add.

        Therefore, the time complexity is n log n.

        """
        # I am going to make new sorted list, the length is based on self.list.length
        alpha_sort = ArraySortedList(self.list.length)

        if len(self.list) > 0 : 

        # The number of length of list.
        # time complexity O(n)
            for i in range(self.list.length):
                list_item = self.list[i]
                
                #black, darken, rainbow etc 
                key = list_item.value.name 
                
                #layer
                value = list_item.value

                #based on the sort, add into alpha_sort
                # so the value will be sorted with alphabetically.  
                # this part is the time complexity: O(log n)
                # Because in add function, it uses index_to_add (log n part).
                alpha_sort.add(ListItem(value, key))
                
            # if the number of length is odd number
            if len(alpha_sort) % 2 == 1:
                layer = alpha_sort[len(alpha_sort)//2].value

            # if the number of length is even number
            else:
                layer = alpha_sort[(len(alpha_sort)//2)-1].value
            
            # erase that layer.
            self.erase(layer)
