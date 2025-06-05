# Scrapes all available player stats from the given URL

from playwright.sync_api import Page
from .data import PlayerStats, GeneralPlayerStats, ShotsStats, AttackingStats, PassingStats, DefensiveStats, GoalKeepingStats
from .utils import scrape_locator_lists
from .func_util import remove_duplicate_strings, split_capital_string, split_digit

SHOTS_MAP = {
    "total shots": "total_shots",
    "goals": "goals",
    "expected goals (xg)": "xG",
    "xg on target": "xGOT",
    "shots on target": "shots_on_target",
    "shots off target": "shots_off_target",
    "blocked shots": "blocked_shots",
    "shots inside the box": "shots_inside_the_box",
    "shots outside the box": "shots_outside_the_box",
    "headed shots": "headed_shots"
}

ATTACK_MAP = {
    "touches in opposition box": "touches_in_opposition",
    "successful dribbles": ["successful_dribbles", "total_dribbles", "percentage_dribbles_won"],
    "big chances missed": "big_chances_missed",
    "touches": "touches",
    "fouls suffered": "fouls_suffered",
    "offsides": "offsides",
}

PASSES_MAP = {
    "accurate passes": ["accurate_passes", "total_passes", "passes_accuracy"],
    "big chances created": "big_chances_created",
    "assists": "assists",
    "expected assists (xa)": "xA",
    "accurate passes in final third": ["accurate_passes_in_final_third", "total_passes_in_final_third", "accuracy_passes_in_final_third"],
    "accurate long passes": ["accurate_long_passes", "total_long_passes", "accuracy_long_passes"],
    "accurate crosses": ["accurate_crosses", "total_crosses", "accuracy_crosses"]
}

DEFENSE_MAP = {
    "duels": "total_duels",
    "aerial duels won": ["aerial_duels_won", "total_aerial_duels", "percentage_aerial_duels_won"],
    "ground duels won": ["ground_duels_won", "total_ground_duels", "percentage_ground_duels_won"],
    "tackles won": ["tackles_won", "total_tackles", "percentage_tackles_won"],
    "fouls committed": "fouls_committed",
    "interceptions": "interceptions",
    "clearances": "clearances",
    "errors leading to goal": "errors_leading_to_goal",
    "errors leading to shot": "errors_leading_to_shot",
}

GOALKEEPING_MAP = {
    "goalkeeper saves": "saves",
    "goals conceded": "goals_conceded",
    "goals prevented": "goals_prevented",
    "xgot faced": "xGOT_faced",
    "punches": "punches",
    "throws": "throws",
    "act as sweeper": "act_as_sweeper",
}

GENERAL_MAP = {
    "player rating": "rating",
    "minutes played": "minutes_played",
    "goals": "goals",
    "own goals": "own_goals",
    "assists": "assists",
    "yellow cards": "yellow_cards",
    "red cards": "red_cards",
}


# Page -> list
# helper function to scrape raw stats and return a list of dictionary
#   containing different player stats
async def scrape_stats_to_list(page: Page, map_type: dict, data_class) -> list:
    try:
        stats_headers = []
        table_heads_locator = await scrape_locator_lists(page=page, selector="thead .wcl-tableHeadCell_sux-6")

        for head_locator in table_heads_locator:
            header = await head_locator.text_content()
            header = remove_duplicate_strings(string=header)
            stats_headers.append(header.lower())

        all_stats = []
        table_rows_locator = await scrape_locator_lists(page=page, selector="tbody tr")
        
        for row_locator in table_rows_locator:
            cells_locator = await row_locator.locator("td").all()

            row_stats = data_class()
            for index, cell_locator in enumerate(cells_locator):
                cell_text = await cell_locator.text_content()
                if index == 0:
                    name, position = split_capital_string(string=cell_text)
                    setattr(row_stats, "player_name", name.strip())
                    setattr(row_stats, "position", position.strip())

                else:
                    keys = map_type.get(stats_headers[index], None)
                    if keys is None:
                        continue
        
                    if isinstance(keys, list) and len(keys) == 3:
                        print(cell_text.strip())
                        percentage_value, first_value, second_value = split_digit(cell_text.strip())
                        setattr(row_stats, keys[0], int(first_value))
                        setattr(row_stats, keys[1], int(second_value))
                        setattr(row_stats, keys[2], int(percentage_value))

                    elif isinstance(keys, str):
                        print(keys, stats_headers[index], cell_text.strip())
                        setattr(row_stats, keys, cell_text.strip())
        
            all_stats.append(row_stats)
        return all_stats
    except Exception as e:
        print(e)


# Page, str -> Dataclass Object
# Scrapes player stats from the given page and returns any of the provide stats object
async def navigate_and_scrape_stats(page: Page, url: str, map_type: dict, data_class):
    try:
        url = await page.url.rsplit('/', 1)[0] + url
        await page.goto(url)
        await page.wait_for_selector(".container__livetable .container__detailInner .section .wcl-tableWrapper_Z9oKt .wcl-table_tQq-F")

        stats = await scrape_stats_to_list(page=page, map_type=map_type, data_class=data_class)
        return stats
    except Exception as e:
        return []


async def get_player_stats(page: Page) -> PlayerStats:
    shots_stats = await scrape_stats_to_list(page=page, map_type=SHOTS_MAP, data_class=ShotsStats)
    attacking_stats = await navigate_and_scrape_stats(page=page, url="attack", map_type=ATTACK_MAP, data_class=AttackingStats)
    passing_stats = await navigate_and_scrape_stats(page=page, url="passes", map_type=PASSES_MAP, data_class=PassingStats)
    defensive_stats = await navigate_and_scrape_stats(page, url="defense", map_type=DEFENSE_MAP, data_class=DefensiveStats)
    goalkeeping_stats = await navigate_and_scrape_stats(page, url="goalkeeping", map_type=GOALKEEPING_MAP, data_class=GoalKeepingStats)
    general_stats = await navigate_and_scrape_stats(page, url="general", map_type=GENERAL_MAP, data_class=GeneralPlayerStats)

    return PlayerStats(
        shots=shots_stats,
        attacking=attacking_stats,
        passing=passing_stats,
        defensive=defensive_stats,
        goalkeeping=goalkeeping_stats,
        general=general_stats
    )


    
