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
    Any further additions to the store wipe the previous layers,
    and erasing a SetLayerStore just means having no layers applied.

    Attributes:
        - self.layer: The last layer that was applied to the store.
        - self.special_switch: A boolean that checks a special function is called or not.
    """
    
    def __init__(self) -> None:
        self.layer = None
        self.special_switch = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Args:
        - layer : a color based on layers.py (black,lighten,invert etc)

        Returns:
        - result: boolean depends on added correctly or not.

        Time complexity 
        - Worst & Best case: O(1)
        There is no loop and no reversive calls.
        """

        if self.layer == None or self.layer.bg != layer.bg:
            self.layer = layer
            return True
        
        # if self.layer.bg and layer.bg is same, then we will just return False.
        # becasue the layer is already in the layer.
        else:
            return False
    

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        get the value of current color in layer.

        Args:
        - start: tuple that explain inital color of layer.
        - timestamp: time (?)
        - x: integer that is in the horizontal position of the layer.
        - y: integer that is in the vertical position of the layer.

        Returns:
        - result: it returns the colour this square should show, given the current layers.

        Time complexity 
        - Worst & Best case: O(1)
        There is no loop and no reversive calls.
        """
        
        # if self.layer is not None, the color will be applied into "start".
        if self.layer is not None:
            start = self.layer.apply(start,timestamp,x,y)

        # if the special function is called, the inverted color will be applied to "start".
        if self.special_switch:
            start = invert.apply(start,timestamp,x,y)

        return start 
        
   
    def erase(self, layer: Layer) -> bool:
        """
        The erase function returns true if the LayerStore was actually changed.

        Args:
        - layer : a color based on layers.py (black,lighten,invert etc)

        Returns:
        - result: it returns boolean if the layerstore is changed.

        Time complexity 
        - Worst & Best case: O(1)
        There is no loop and no reversive calls.
        """

        if self.layer == None:
            return False
        
        # if there is a layer existing in self.layer, it will make None.
        else:
            self.layer = None
            return True

    def special(self):  
        """
        Special mode. Sets a boolean to true, so that get_color will invert the color.

        Time complexity
        - Worst case: O(1)
        - Best case: O(1)
        """
        # if true, change the switch to false. 
        # it will make it work only one time.
        if self.special_switch == True:
            self.special_switch = False

        else:
            self.special_switch = True

class AdditiveLayerStore(LayerStore):
    """
    The Additive Layer Store simply applies layers consecutively. 
    Whenever a store has a collection of layers, 
    these layers are applied one-by-one,from earliest added to latest added.

    Attributes:
        - self.queue : QueueADT, so that it can work with FIFO(First In First Out) logic.

    Since multiple copies of the same layer can be used in this mode,
    make the capacity of the store at least 100 times the number of layers.
    Therefore, The Maximum of CircularQueue will be 9*100 = 900.
    """

    def __init__(self) -> None:
        self.queue = CircularQueue(900)
        
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
    
        Args:
        - layer : a color based on layers.py (black,lighten,invert etc)

        Returns:
        - result: boolean depends on if the LayerStore was actually changed or not.

        Time complexity 
        - Worst & Best case: O(1)
        There is no loop and no reversive calls.
        """

        if self.queue.is_full():
            return False
        
        # if the queue is not full, append layer to queue.
        # return True.
        else:
            self.queue.append(layer)
            return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Args
        - start: tuple that explain inital color of layer.
        - timestamp: time (?)
        - x: integer that is in the horizontal position of the layer.
        - y: integer that is in the vertical position of the layer.

        Returns
        - result: the color in this layer should show.

        Time complexity 
        - Worst case: O(n), where n is the length of the queue. 
        - Best case: O(1), where n is the length of the queue is empty.
        """

        if self.queue.is_empty():
            return start
 
        # From the "queue.front" to "queue.front+queue.length"
        # It means we will check all the value that is not empty.
        for i in range(self.queue.front,self.queue.length+self.queue.front):

            # First time will be start.
            if i == self.queue.front:
                color = self.queue.array[i].apply(start, timestamp, x, y)

            # After first time, we will keep apply the last color to current color.
            # the time complexity is O(n-1) therefore, it can be considered to O(n).
            else:
                color = self.queue.array[i].apply(color, timestamp, x, y)

        return color
        

    def erase(self, layer: Layer) -> bool:
        """
        Remove the first layer that was added. Ignore what is currently selected.

        The argument for erase does not matter for an AdditiveLayerStore.
        It always removes the oldest remaining layer.

        The function removes the oldest remaining layer from the queue.
        It can be done in constant time regardless of the size of the queue.

        Args
        - layer : a color based on layers.py (black,lighten,invert etc)

        Returns
        - result: the colour this square should show, given the currexnt layers.

        Time complexity 
        - Worst case: O(n), where n is the length of the queue. 
        - Best case: O(1), where n is the length of the queue is empty.
        """

        # If the queue is empty, there is nothing to erase.
        if self.queue.is_empty(): 
            return False
        
        # Else, That means we need to erase the latest one.
        # Therefore we will return true after we serve.
        else: 
            self.queue.serve()
            return True

    def special(self):
        """
        Reverse the order of current layers (first becomes last, etc.)

        Special mode. Different for each store implementation.

        *** Logic of how special function is working ***

        It uses the stack to create a reversed queue for using LIFO(Last In First Out) logic.
        Therefore, if we pop from the stack and append to queue, it will be reversed.

        1. it serves from the self.queue and push to special_stack.
        2. the index in special_stack will be pop, and appended again to self.queue

        Returns
        - result: reverse order of current layers.

        Time complexity 
        - Worst case: O(n), when the queue is not empty and has n elements, so the loops run n times each.
        - Best case: O(1), where n is the length of the queue is empty.

        The "special" iterates each element in the queue. 
        The time complexity of each operation is O(1).
        Therefore, the overall time complexity of the function is O(n).
        """

        # Temporary stack, making for reverse array for Last In First Out.
        special_stack = ArrayStack(self.queue.length)

        # The number of length, they will continue push to stack from that we served in queue.
        for i in range(self.queue.length):
            special_stack.push(self.queue.serve())

        # Append to queue from the stack we pop.
        # Therefore, it will be reversed queue. 
        for i in range(special_stack.length):
            self.queue.append(special_stack.pop())

class SequenceLayerStore(LayerStore):
    """
    Each layer type is either applied / not applied, and is applied in order of index.
    
    """

    # I used the ArraySortedList for SequenceLayerStore.
    # The maximum_capacity will be 9, cuz the the number of layers is total 9.
    def __init__(self) -> None:
        self.list = ArraySortedList(9)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.

        Args
        - layer : a color based on layers.py (black,lighten,invert etc)

        Returns
        - result: returns true if the LayerStore was actually changed.

        Time complexity 
        - Worst case: O(n), where n is the length of the queue. 
        - Best case: O(1), where n is the length of the queue is empty.

        "add" function iteraties each element in the list and performs on each element.
        Each time complexity of operation is O(1).
        Therefore, the overall time complexity is O(n).
        """

        for i in range(self.list.length): #O(n)
            
            # key : index in list
            key_value = self.list[i].key 

            # If layer.index is equal to key_value(index), the layer is already exist.
            # Therefore, it will return False.
            if layer.index == key_value:  #O(n)
                return False
            
        # it makes ListItem called new_item so that it will be added to self.list
        new_item = ListItem(layer, layer.index)
        self.list.add(new_item)

        #LayerStore is actually changed, so return True.
        return True
        

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        """

        Args
        - start: tuple that explain inital color of layer.
        - timestamp: time (?)
        - x: integer that is in the horizontal position of the layer.
        - y: integer that is in the vertical position of the layer.

        Returns
        - result: returns the colour this square should show, given the current layers.

        Time complexity 
        - Worst case: O(n), where n is the length of the queue. 
        - Best case: O(1), where n is the length of the queue is empty.

        The "get_color" function iterates each element in the list. 
        The time complexity of element is O(1).
        Therefore, the overall time complexity is O(n).
        """

        # If there is nothing (checked with length), then return start color.
        if self.list.length == 0:
            return start
        
        # The number of length of list.
        for i in range(len(self.list)): #O(n)
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
        Ensure this layer type is not applied.

        Args
        - layer : a color based on layers.py (black,lighten,invert etc)

        Returns
        - result: returns true if the LayerStore was actually changed.

        Time complexity 
        - Worst case: O(n), when the layer is in the last index in layer. (n times) 
        - Best case: O(1), where n is the length of the queue is empty.
  
        The "erase" function iterates each element in the list.
        It check one by one, the number of element in the list.
        Also, the each operation time complexity is O(1).
        """

        #The number of length of list.
        for i in range(len(self.list)): 

            # If key is same value with index. delete at index.
            if self.list[i].key == layer.index: #O(n)

                #As using the funtion "delete_at_index",
                #  the index i+1 will be shuffle_left.
                self.list.delete_at_index(i) #O(n)
                return True
            
        return False

    def special(self):  
        """
        Special mode. 
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.

        *** ArraySortedList ***
        Special function used ArraySortedList, Maximum length is based on the self.length
        It will add the item in list using ListItem to alpha_sort so that item will be sorted with Alphabetically.
        After that, we can detect the median 'name', then erase that value in layer.

        Time complexity 
        - Worst case: O(n log n) 

        n : it checks the number of elements in the list by n.
        log n : this "special" function compare elements in the list to each other and make it sort in _index_to_add.

        - Best case: O(1), where n is the length of the queue is empty.
        
        """
        # Make new sorted list, the length is based on self.list.length
        alpha_sort = ArraySortedList(self.list.length)

        if len(self.list) > 0 : 

        # time complexity O(n)
            for i in range(self.list.length):
                list_item = self.list[i]
                
                #black, darken, rainbow etc 
                key = list_item.value.name 
                
                #layer
                value = list_item.value
 
                # this part is the time complexity: O(log n)
                # Because in add function, it uses index_to_add (log n).
                alpha_sort.add(ListItem(value, key))
                
            # if the number of length is odd number
            if len(alpha_sort) % 2 == 1:
                layer = alpha_sort[len(alpha_sort)//2].value

            # if the number of length is even number
            else:
                layer = alpha_sort[(len(alpha_sort)//2)-1].value
            
            # erase that layer.
            self.erase(layer)
