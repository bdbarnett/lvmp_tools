# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import gc
from .animations import move_xy
from tools.misc import obj_details

############################## View Focus Callbacks

def pan_focus_cb(group, cont, scroll_gp=False, **args):
    current_obj = group.get_focused()

    while current_obj.get_parent() != cont:
        current_obj = current_obj.get_parent()

    move_to_obj = current_obj
    parent = move_to_obj.get_parent()
    grandparent = parent.get_parent()


    if scroll_gp == True:
        # ZRoundPanels and CircularLivePanels scroll the grandparent
        x_offset = (grandparent.get_width() - move_to_obj.get_width()) // 2
        y_offset = (grandparent.get_height() - move_to_obj.get_height()) // 2
        position = (move_to_obj.get_x() - x_offset, move_to_obj.get_y() - y_offset)
        grandparent.scroll_to(*position, lv.ANIM.ON)
    else:
        # FlexFlowLivePanels scroll the parent
        position = (move_to_obj.get_x(), move_to_obj.get_y())
        parent.scroll_to(*position, lv.ANIM.ON)

def rotate_focus_cb(group, cont, exclude=[], **args):
    """
    A focus callback function for a group.  Except for objects in the 'exclude' list, moves all objects
    on the focused object's parent to an adjacent object's coordinates in round-robin fashion.

    Note:
    Currently moves objects until the focused object is higher than all other objects on the parent.
    Could be universal if there was a method to determine which object lost focus.  Then it could
    rotate until the focused object was in the previously focused object's position.

    Usage:
        from focus_callbacks import rotate_focus_cb
        exclude_list = [] # a list of objects to exclude
        group = lv.group_get_default()   # Can be any group, not just the default
        group.set_focus_cb(lambda g: rotate_focus_cb(g, cont, exclude=exclude_list))
    """
    current_obj = group.get_focused()
    if current_obj in exclude: return

    while current_obj.get_parent() != cont:
        current_obj = current_obj.get_parent()
 
    move_to_obj = current_obj
    if move_to_obj in exclude: return  # return if focused object is excluded
    parent = move_to_obj.get_parent()  # parent of focused object

    # Build lists of objects and their coordinates that are of the same type as focused, excluding objects in exclude list
    siblings = parent.get_child_cnt()  # number of siblings
    objects = []
    positions = []
    for i in range(siblings):
        object = parent.get_child(i)
        if object not in exclude:
            objects.append(object)
            positions.append((object.get_x_aligned(), object.get_y_aligned()))
    if len(objects) == 1:
        return  # return if there's a single item

    while objects[0] != move_to_obj:  # shift the lists until move_to_obj is first
        objects.append(objects.pop(0))
        positions.append(positions.pop(0))

    group.focus_freeze(True)  # prevent new focus changes until animation has run
    _rotate(group, objects, positions)

############################## Focus Callback Helpers


def _rotate(group, objects, positions):
    # call this function until focused object's y is less than adjacent objects' y, meaning it is at the top.
    first_y = positions[0][1]
    next_y = positions[1][1]
    prev_y = positions[-1][1]

    if first_y < next_y and first_y < prev_y:  # first obj is at the top
        group.focus_freeze(False)
        gc.collect()
        return

    new_positions = positions.copy()  # create a copy of the positions list
    if first_y > next_y:
        new_positions.append(new_positions.pop(0))  # shift that copy to the right
    else:
        new_positions.insert(0, new_positions.pop())  # shift that copy to the left

    last_item = len(objects) - 1
    for i, obj in enumerate(objects):
        # on the last item, set the animation ready callback to call this function again
        ready_cb = (
            None
            if i < last_item
            else lambda a: _rotate(group, objects, new_positions)
        )
        move_xy(
            obj, positions[i], new_positions[i], ready_cb=ready_cb
        )  # move the object from current to new position
