from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ListItem

class ReplayTracker:
    """
    a simpler version of the UndoTracker, keep track of every action taken (Including Undos, Redos, Drawing, and Specials)
    when playback has started, feed all of these actions back to the game so that it can be re-run. 
    
    Attributes:
        - self.replay_sample_list: Replay should be start from the oldest action to latest acton. 
                                   Therefore, I used CircularQueue (First in First Out)
                                   The maximum capacity will be same with undotracker.
    """

    def __init__(self) -> None:
        self.replay_sample_list = CircularQueue(10000)                  #O(1)

    def start_replay(self) -> None:
        pass

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        Args
        - action : which action is added.
        - is_undo: (bool) specifies whether the action was an undo action or not.

        Returns:
        - result: returns true if the Undo_list was actually changed.

        Time complexity 
        - Worst & Best case: O(1)
        "add_action" function has all constant time complexity.
        """

        # It makes the listitem based on action and boolean.
        action = ListItem(action, is_undo)                              #O(1)

        # Append the action to the replay_sample_list.
        self.replay_sample_list.append(action)                          #O(1)

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.

        Args
        - grid: grid

        Returns
        - result: Boolean, If there were no more actions to play, and so nothing happened, return True.

        Time complexity 
        - Worst & Best case: O(1)
        "play_next_action" function has all constant time complexity.
        """
       
        # It checks the replay_sample_list is empty or not.
        # If its empty, return True
        if self.replay_sample_list.is_empty():                          #O(1)
            return True
        
        # Get action from the list by serve.
        action = self.replay_sample_list.serve()                        #O(1)
       
        # If action.key is true, it means the action was undo.
        # Therefore, it applys to undo.
        if action.key:                                                  #O(1)
            action.value.undo_apply(grid)                               #O(1)

        # If action.key is false, it applys to redo.
        else:
            action.value.redo_apply(grid)                               #O(1)

        return False                                                    #O(1)
        

        

        

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

