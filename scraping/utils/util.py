from datetime import datetime, timedelta

# This file contains reusable functions for parsing and formatting data

# ==========================================================
# Reusable functions
# ==========================================================

# ==========================================================
# Append string to a list
# append_to_list: (lst: list) -> list
# interp. append_to_list takes a list of playwright locator and strips 
#       strings from it and appends to a new list

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


# ==========================================================
# Get events that already played

# get_events_already_played: (Date, Time) -> Bool
# interp. takes a date and time and returns True if the event has already played
#      False otherwise
def is_event_already_played(date: str, time: str) -> bool:
    """
        Args:
            date (str): The date of the event in 'dd-mm-yyyy' format.
            time (str): The time of the event in 'HH:MM' format.
        Returns:
            bool: True if the event has already played, False otherwise.
    """
    try:
        event_datetime_str = f"{date} {time}"
        event_datetime = datetime.strptime(event_datetime_str, '%Y-%m-%d %H:%M')
        check_time = datetime.now() - timedelta(hours=2)
        return event_datetime <= check_time
    except ValueError:
        return False