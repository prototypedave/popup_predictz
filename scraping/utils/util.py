# This file contains reusable functions for parsing and formatting data

# ========================================================
# Reusable functions
# ========================================================

# ==========================================================
# Append string to a list
# append_to_list: (lst: list) -> list
# interp. append_to_list takes a list and strips strings from it and appends to a new list

def append_to_list(lst: list) -> list:
    """
    Append string to a list.

    Args:
        lst (list): The list to append strings to.

    Returns:
        list: A new list with stripped strings.
    """
    new_list = []
    for item in lst:
        new_list.append(item.inner_text().strip().lower())
    return new_list