import pytest
from scraping.utils.data_rep import parse_score, parse_list_details, parse_date_dd_mm_yyyy, split_string

@pytest.mark.parametrize("input_str,expected", [
    ("1\n-\n2", (1, 2)),
    ("2\n-\n0", (2, 0)),
    ("-\n-\n-", (None, None)),        
    ("-", (None, None)),              
    ("1\n2", (None, None)),           
    ("abc\n-\ndef", (None, None)),    
    ("3\n-\n", (None, None)),            
    ("-\n-\n3", (None, None)),
    ("1\n-\nabc", (None, None)),
    ("abc\n-\n2", (None, None)),
    ("1\n-\n-", (None, None)),
    ("-\n-\n1", (None, None)),
])
def test_parse_score(input_str, expected):
    assert parse_score(input_str) == expected


@pytest.mark.parametrize("keys, values, expected", [
    (["referee:", "stadium:", "capacity:"], ["Mike Dean", "ENG", "Emirates", "50000"],
     {"referee": "Mike Dean ENG", "stadium": "Emirates", "capacity": "50000"}),
    (["referee:", "stadium:", "capacity:"], ["Mark Smith", "SCO", "Trafford"],
     {"referee": "Mark Smith SCO", "stadium": "Trafford"}),
    (["referee:", "stadium:"], ["Mike Dean", "ENG", "Emirates"],
     {"referee": "Mike Dean ENG", "stadium": "Emirates"}),
    (["referee:", "stadium:", "capacity:"], ["Mike Dean", "WAL"],
     {"referee": "Mike Dean WAL"}),
])
def test_parse_list_details(keys, values, expected):
    assert parse_list_details(keys, values) == expected


@pytest.mark.parametrize("input_str,expected", [
    ("01.11.2023 15:30", ("2023-11-01", "15:30")),
    ("Invalid date string", (None, None)),
    ("2023.10.01", (None, None)),
    ("2023.10.02 15:30:00", (None, None)),
    ("2023/10/03 15:30", (None, None)),
    ("01-10-2024 15:30", (None, None)),
    ("2025-01-01 15:30:00", (None, None)),
])
def test_parse_date_dd_mm_yyyy(input_str, expected):
    assert parse_date_dd_mm_yyyy(input_str) == expected


@pytest.mark.parametrize("input_str,expected", [
    ("premium league - round 1", ("premium league", "round 1")),
    ("uefa champions league - league phase - round 2", ("uefa champions league", "league phase - round 2")),
    ("la liga", ("la liga", None))
])
def test_split_string(input_str, expected):
    assert split_string(input_str) == expected