from .model import create_async_engine
from sqlalchemy.orm import sessionmaker
from .team import FootballTeam, AsyncSession, select
import asyncio
import pandas as pd
from sqlalchemy.orm import aliased
from .stats import Stats
from scrape.data import MatchStats, fields
from .game import FootballGame

from .base import Base, ADMIN_URL, DB_NAME, ASYNC_DATABASE_URL

async def select_all_teams(session: AsyncSession):
    async with session() as sess:
        HomeTeam = aliased(FootballTeam)
        AwayTeam = aliased(FootballTeam)

        valid_column_names = Stats.__table__.columns.keys()
        stats_fields = [getattr(Stats, f.name) for f in fields(MatchStats) if f.name in valid_column_names]

        base_fields = [
            FootballGame.id.label("game_id"),
            FootballGame.date,
            FootballGame.league,
            FootballGame.country,
            FootballGame.round,
            FootballGame.referee,
            FootballGame.venue,
            FootballGame.capacity,
            HomeTeam.name.label("home_team"),
            AwayTeam.name.label("away_team"),
            FootballGame.home_score,
            FootballGame.away_score,
        ]

        query = (
            select(*base_fields, *stats_fields)
            .join(Stats, FootballGame.id == Stats.game_id)
            .join(HomeTeam, FootballGame.home_team_id == HomeTeam.id)
            .join(AwayTeam, FootballGame.away_team_id == AwayTeam.id)
        )

        results = await sess.execute(query)
        df = pd.DataFrame(results.fetchall())
        return df
    
def df_function(df):
    team_data = {}
    for team in df['home_team'].unique():
        filtered = df[(df['home_team'] == team) | (df['away_team'] == team)]
        if not filtered.empty:
            #team_data[team] = filtered
            select_match_for_prediction(filtered, team)
            #print(f"Team: {team}")
            #print(filtered)

def get_goal_difference(row):
    return abs(row['home_score'] - row['away_score'])

def get_total_score(row):
    return row['home_score'] + row['away_score']

def analyze_team_df(df, team, func):
    # team difference
    df = df.copy()
    df['gd'] = df.apply(func, axis=1)
    mean = df['gd'].mean()
    std = df['gd'].std()
    std = 0 if pd.isna(std) else std
    if std:
        rsd = std / mean * 100
        predict = is_predictable(rsd)
        return predict

def select_match_for_prediction(df, team):
    # team difference
    if analyze_team_df(df, team, get_goal_difference):
        print(f"{team} selected for gd")
    if analyze_team_df(df, team, get_total_score):
        print(f"{team} selected for over / under")


def is_predictable(rsd):
    if rsd <= 50:
        return True
    return False

import pandas as pd
import numpy as np
from xgboost import XGBClassifier, XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV

def get_result(row):
    if row['home_score'] > row['away_score']:
        return 1   # Home Win
    elif row['home_score'] < row['away_score']:
        return -1  # Away Win
    else:
        return 0   # Draw
    
def augumentation(df):
    df['match_result'] = df.apply(get_result, axis=1)
    label_map = {-1: 0, 0: 1, 1: 2}
    df['match_result'] = df['match_result'].map(label_map)
    df = df.drop(['home_score', 'away_score'], axis=1)
    df = df.drop(['game_id', 'date', 'round'], axis=1, errors='ignore')

    categorical_cols = ['league', 'country', 'referee', 'venue', 'home_team', 'away_team']
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    return df

def augmentation_goal_difference(df):
    df['goal_diff'] = df['home_score'] - df['away_score']
    df = df.drop(['home_score', 'away_score', 'game_id', 'date', 'round'], axis=1, errors='ignore')
    categorical_cols = ['league', 'country', 'referee', 'venue', 'home_team', 'away_team']
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    return df

def train_and_test_match_results(df, df2):
    params = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.3],
        'n_estimators': [100, 200],
        'subsample': [0.8, 1],
        'colsample_bytree': [0.8, 1]
    }

    df = augumentation(df)
    df2 = augumentation(df2)
    X = df.drop('match_result', axis=1)
    y = df['match_result']
    X2 = df2.drop('match_result', axis=1)
    y2 = df2['match_result']

    X_train, X_test, y_train, y_test = X, X2, y, y2 #train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


    model = XGBClassifier(
        max_depth=5,
        learning_rate=0.1,
        n_estimators=200,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='mlogloss',
        
    )
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred, digits=3, zero_division=1))  # Added zero_division=1

def train_and_test_goal_difference(df, df2):
    df = augmentation_goal_difference(df)
    df2 = augmentation_goal_difference(df2)
    X = df.drop('goal_diff', axis=1)
    y = df['goal_diff']
    X2 = df2.drop('goal_diff', axis=1)
    y2 = df2['goal_diff']

    X_train, X_test, y_train, y_test = X, X2, y, y2 #train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)  

    print(f"Mean Squared Error: {mse:.3f}")
    print(f"Mean Absolute Error: {mae:.3f}") 

    def map_result(diff):
        if diff > 0.5:
            return 1   # Home Win
        elif diff < -0.5:
            return -1  # Away Win
        else:
            return 0   # Draw

    pred_outcomes = [map_result(val) for val in y_pred]
    true_outcomes = [map_result(val) for val in y_test]

    accuracy = np.mean(np.array(pred_outcomes) == np.array(true_outcomes))
    print(f"Outcome Accuracy (W/D/L from predicted goal diff): {accuracy:.3f}")

if __name__ == '__main__':
    async def main():
        engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
        session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        df2 = await select_all_teams(session=session)
        df = pd.read_csv("todays_stats.csv")
        #print(df.count())
        #df_function(df)
        train_and_test_match_results(df, df2)
        #train_and_test_goal_difference(df, df2)
        await engine.dispose()

    asyncio.run(main())