from datetime import datetime


def parse_date_dd_mm_yyyy(input_str: str) -> tuple:
    try:
        dt = datetime.strptime(input_str, "%d.%m.%Y %H:%M")
        date_str = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M")
        return date_str, time
    except ValueError as e:
        return None, None


print(parse_date_dd_mm_yyyy("25.10.2023 15:30"))