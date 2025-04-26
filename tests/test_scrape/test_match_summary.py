import pytest
from scraping.events import scrape_events, scrape_match_link
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_page_event(atr):
    mock_event = MagicMock()
    mock_locator_result = MagicMock()
    mock_first_link = MagicMock()
    mock_first_link.get_attribute.return_value = atr
    mock_locator_result.first = mock_first_link
    mock_event.locator.return_value = mock_locator_result
    return mock_event


@pytest.fixture
def mock_page():
    mock_page = MagicMock()
    return mock_page


@pytest.mark.parametrize("atr, expected", [
    ("https://example.com/match/#WrTeF", "https://example.com/match/#WrTeF"),
    (None, None),
    ("", None),
])
def test_scrape_match_link(mock_page_event, atr, expected):
    assert scrape_match_link(mock_page_event) == expected
    mock_page_event.locator.assert_called_once_with("a")
    if expected:
        mock_page_event.locator().first.get_attribute.assert_called_once_with("href")


@pytest.mark.parametrize("input_list, expected", [
    (["https://example.com/match/#WrTeF", "invalid_url", None, ""],
     ["https://example.com/match/#WrTeF"]),
    ([], []),
    ([None, None], []),
])
def test_scrape_events(mock_page, input_list, expected):
    mock_events = [MagicMock() for _ in input_list]
    mock_locator = MagicMock()
    mock_locator.all.return_value = mock_events
    mock_page.locator.return_value = mock_locator

    with patch('scraping.events.scrape_match_link') as mock_scrape:
        mock_scrape.side_effect = input_list
        links = scrape_events(mock_page)
        assert links == expected

        assert mock_scrape.call_count == len(input_list)
        for mock_event in mock_events:
            mock_scrape.assert_any_call(mock_event)

    mock_page.locator.assert_called_once_with(".event__match")
    mock_locator.all.assert_called_once()  
    mock_page.wait_for_selector.assert_called_once_with(".event__match")


