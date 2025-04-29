import pytest
from scraping.events import scrape_events, scrape_match_link
from unittest.mock import MagicMock, patch
from scraping.match import scrape_match_data_from_link, scrape_loadable_match_data
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


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


@pytest.fixture
def mock_match_info():
    mock_info = MagicMock()
    mock_header_locators = [MagicMock(inner_text=MagicMock(return_value="referee:")),
                           MagicMock(inner_text=MagicMock(return_value="stadium:"))]
    mock_value_locators = [MagicMock(inner_text=MagicMock(return_value="Mike Dean")),
                          MagicMock(inner_text=MagicMock(return_value="Emirates Stadium"))]

    mock_info.locator(".wcl-overline_rOFfd").all.return_value = mock_header_locators
    mock_info.locator(".wcl-simpleText_Asp-0").all.return_value = mock_value_locators
    return mock_info


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


def test_scrape_loadable_match_data(mock_page, mock_match_info):
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.return_value = [mock_match_info]
    with patch('scraping.utils.util.append_to_list', side_effect=[["referee:"], ["Mike Dean", "Emirates Stadium"]]), \
         patch('scraping.utils.data_rep.parse_list_details', return_value={"referee": "Mike Dean", "stadium": "emirates stadium"}):
        result = scrape_loadable_match_data(mock_page)
        assert result == {"referee": "Mike Dean", "stadium": "emirates stadium"}

    mock_page.wait_for_selector.assert_called_once_with(".loadable__section")
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.assert_called_once()
    mock_match_info.locator(".wcl-overline_rOFfd").all.assert_called_once()
    mock_match_info.locator(".wcl-simpleText_Asp-0").all.assert_called_once()


def test_scrape_loadable_match_data_timeout(mock_page):
    mock_page.wait_for_selector.side_effect = PlaywrightTimeoutError("Timeout")
    result = scrape_loadable_match_data(mock_page)
    assert result == {}
    mock_page.wait_for_selector.assert_called_once_with(".loadable__section")
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.assert_not_called()


def test_scrape_loadable_match_data_no_extra_info(mock_page):
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.return_value = []
    result = scrape_loadable_match_data(mock_page)
    assert result == {}
    mock_page.wait_for_selector.assert_called_once_with(".loadable__section")
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.assert_called_once()


def test_scrape_loadable_match_data_empty_header_value(mock_page):
    mock_match_info = MagicMock()
    mock_match_info.locator(".wcl-overline_rOFfd").all.return_value = []
    mock_match_info.locator(".wcl-simpleText_Asp-0").all.return_value = []
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.return_value = [mock_match_info]

    with patch('scraping.utils.util.append_to_list', side_effect=[[], []]), \
         patch('scraping.utils.data_rep.parse_list_details', return_value={}):
        result = scrape_loadable_match_data(mock_page)
        assert result == {}

    mock_page.wait_for_selector.assert_called_once_with(".loadable__section")
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.assert_called_once()
    mock_match_info.locator(".wcl-overline_rOFfd").all.assert_called_once()
    mock_match_info.locator(".wcl-simpleText_Asp-0").all.assert_called_once()


def test_scrape_loadable_match_data_skips_tv_channel(mock_page):
    mock_match_info = MagicMock()
    mock_header_locators = [MagicMock(inner_text=MagicMock(return_value="tv channel:")),
                           MagicMock(inner_text=MagicMock(return_value="stadium:"))]
    mock_value_locators = [MagicMock(inner_text=MagicMock(return_value="Sky Sports")),
                          MagicMock(inner_text=MagicMock(return_value="anfield"))]

    mock_match_info.locator(".wcl-overline_rOFfd").all.return_value = mock_header_locators
    mock_match_info.locator(".wcl-simpleText_Asp-0").all.return_value = mock_value_locators

    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.return_value = [mock_match_info, MagicMock()] 

    with patch('scraping.utils.util.append_to_list', side_effect=[["tv channel:", "stadium:"], ["Sky Sports", "anfield"], [], []]), \
         patch('scraping.utils.data_rep.parse_list_details', side_effect=[{}, {"stadium": "anfield"}]):
        result = scrape_loadable_match_data(mock_page)
        assert result == {"stadium": "anfield"} 

    mock_page.wait_for_selector.assert_called_once_with(".loadable__section")
    mock_page.locator(".wclDetailSection .wcl-content_J-1BJ").all.assert_called_once()
    mock_match_info.locator(".wcl-overline_rOFfd").all.assert_called_once()
    mock_match_info.locator(".wcl-simpleText_Asp-0").all.assert_called_once()
