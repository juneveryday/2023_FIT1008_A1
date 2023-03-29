from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack


class UndoTracker:
    '''
    Be able to undo and redo draw actions on the grid. 

    The user's actions were initially saved to the undo_list, 
    and when undo was performed, they were saved to the redo_list.

    Attributes : used Arraystack because it needs to undo from the lastest action. LIFO (Last In First Out)
    - self.Undo_list : when action is added, it will be pushed to Undo_list first.
    - self.Redo_list : when the action is undo from the Undo_list, the action will be added to Redo_list.
    '''

    def __init__(self) -> None:
        self.Undo_list = ArrayStack(10000)                          #O(1)
        self.Redo_list = ArrayStack(10000)                          #O(1)
        
    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If collection is already full, free to exit early and not add the action.
        
        Args:
        - action: return which action is added.

        Returns:
        - result: returns true if the Undo_list was actually changed.

        Time complexity 
        - Worst case: O(1), there is no loop and no reversive calls.
        - Best case : O(1), when Undo_list is already full.
        """

        # After Redo if we add_action again, the inside Redo_list should be reset.
        if self.Redo_list.length > 0:                               #O(1)
            self.Redo_list = ArrayStack(10000)                      #O(1)
        
        # If Undo_list is full, it cannot add anymore, so return False
        if self.Undo_list.is_full():                                #O(1)
            return False                                            #O(1)
        
        # Else, it still can push to Undo_list.
        # After we push, return True.
        else:
            self.Undo_list.push(action)                             #O(1)                      
            return True                                             #O(1)
    

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        Returns:
        - result: return grid which action is poped.

        Time complexity 
        - Worst case: O(undo_apply), the worst case will be depends on undo_apply function.
        - Best case : O(1), when Undo_list is empty.

        The number of operations perform regardless of the size of the input.
        """

        # if Undo_list is empty, return None.
        if self.Undo_list.is_empty():                               #O(1)
            return None                                             #O(1)
        
        # Undo_item is that we pop from the Undo_list.
        Undo_item = self.Undo_list.pop()                            #O(1)

        # After that, apply undo by using undo_apply.
        Undo_item.undo_apply(grid)                                  #O(undo_apply)                      

        # Push the item from undo to Redo_list.
        self.Redo_list.push(Undo_item)                              #O(1)                 


        return Undo_item

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        Returns:
        - result: return grid which action is poped from Redo_item.
                               = which action it redid.

        Time complexity 
        - Worst case: O(redo_apply), the worst case will be depends on redo_apply function.
        - Best case : O(1), when Undo_list is empty.

        The number of operations perform regardless of the size of the input.
        """

        # if Redo_list is empty, return None.
        if self.Redo_list.is_empty():                               #O(1)
            return None                                             #O(1)

        # Redo_item is that we pop from the Redo_list.
        Redo_item = self.Redo_list.pop()                            #O(1)

        # After that, apply redo by using redo_apply.
        Redo_item.redo_apply(grid)                                  #O(redo_apply)

        # Push the item from the redo to Redo_list.
        self.Undo_list.push(Redo_item)                              #O(1)

        return Redo_item                                            #O(1)
