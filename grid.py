from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_util import Layer
from layer_store import *

class Grid:
    '''
    The Grid class should store all current grid information, 
    including the individual Layer Stores.

    Args
    draw_style:
        The style (colours will be drawn) should be one of DRAW_STYLE_OPTIONS
        This draw style determines the LayerStore used on each grid square.

    x, y: The dimensions of the grid.

    '''
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    #Initialise the grid object.
    def __init__(self, draw_style, x, y) -> None:
        '''
        Time complexity 
        - Worst & Best case: O(x * y) 
        
        __init__ makes the 2 dimension grid. depends on domain(x) and range(y).

        depends on value of draw_style, it will enter 2 times for loop.
        self.grid in i, and j in i.

        There is 2 loop, therefore the time complexity is O(n^2)
        '''
        self.brush_size = self.DEFAULT_BRUSH_SIZE
        self.draw_style = draw_style
        self.x = x
        self.y = y

        # grid object initialising
        self.grid = ArrayR(x) 

        for i in range(len(self.grid)):                     #O(1)
            self.grid[i] = ArrayR(y)                        #O(1)
        
        if draw_style == self.DRAW_STYLE_SET:
            for i in range(len(self.grid)):                 #O(x)
                for j in range(len(self.grid[i])):          #O(y)
                    self.grid[i][j] = SetLayerStore()
                    
        elif draw_style == self.DRAW_STYLE_ADD:
            for i in range(len(self.grid)):                 #O(x)
                for j in range(len(self.grid[i])):          #O(y)
                    self.grid[i][j] = AdditiveLayerStore()

        elif draw_style == self.DRAW_STYLE_SEQUENCE:
            for i in range(len(self.grid)):                 #O(x)
                for j in range(len(self.grid[i])):          #O(y)
                    self.grid[i][j] = SequenceLayerStore()
    
    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        Time complexity 
        - Worst & Best case: O(1)
        There is no loop and no reversive calls.
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        Time complexity 
        - Worst & Best case: O(1)
        There is no loop and no reversive calls.
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.

        Time complexity
        - Worst & Best case: O(k * n^2)

         k: time complexity of special.
         n^2 : there is 2 loop in special function.

        """
        for list in self.grid:
            for layer in list:
                layer.special()

    def __getitem__(self, i):
        '''
        Time complexity 
        - Worst & Best case: O(1)
        There is no loop and no reversive calls.
        '''
        
        return self.grid[i]

