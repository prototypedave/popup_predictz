# This file contains reusable functions for parsing and formatting data

# ==========================================================
# Reusable functions
# ==========================================================

# ==========================================================
# Append string to a list
# append_to_list: (lst: list) -> list
# interp. append_to_list takes a list of playwright locator and strips strings from it and appends to a new list

def append_to_list(lst: list) -> list:
    """
        Append string to a list.

        Args:
            lst (list): The list (of playwright locator) to append strings to.

        Returns:
            list: A new list with stripped strings.
    """
    new_list = []
    for item in lst:
        try:
            new_list.append(item.inner_text().strip().lower())
        except AttributeError:
            print(f"AttributeError: {item} does not have 'inner_text' method.")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
    return new_list