from __future__ import annotations
from data_structures.referential_array import ArrayR

class Grid:
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
        """
        - draw_style:
            The style (colours will be drawn) should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.

        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.brush_size = self.DEFAULT_BRUSH_SIZE
        self.draw_style = draw_style

        self.layer_x = x
        self.layer_y = y

        self.grid_x = ArrayR(self.layer_x) #[n,n,n,n,n,n]

        for i in self.grid_x:
            self.grid_x[i] = ArrayR(self.layer_y)
    
    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        pass
