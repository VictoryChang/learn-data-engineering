from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
import dagster as dg
import pandas as pd
import pymongo
import requests


load_dotenv(Path("~/.env").expanduser())


@dg.asset(group_name="sources", kinds={"csv"})
def extract_csv() -> dg.MaterializeResult:
    pandas_df = pd.read_csv("src/etl_tutorial/defs/data/csv_demo.csv")

    return dg.MaterializeResult(
        metadata={
            "row_count": pandas_df.shape[0],
            "preview": dg.MarkdownMetadataValue(pandas_df.to_markdown(index=False))
        }
    )

@dg.asset(group_name="sources", kinds={"postgres"})
def extract_postgres() -> dg.MaterializeResult:
    postgres_engine = create_engine(
        f"postgresql://{os.environ['POSTGRES_USERNAME']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/postgres_demo")

    pandas_df = pd.read_sql_query("SELECT * FROM users", con=postgres_engine)
    
    return dg.MaterializeResult(
        metadata={
            "row_count": pandas_df.shape[0],
            "preview": dg.MarkdownMetadataValue(pandas_df.to_markdown(index=False))
        }
    )


@dg.asset(group_name="sources", kinds={"mongodb"})
def extract_mongodb() -> dg.MaterializeResult:
    mongo_client = pymongo.MongoClient(
        host=os.environ['MONGODB_HOST'],
        port=int(os.environ['MONGODB_PORT']))

    cursor = mongo_client.mongodb_demo.users.find({}, {'_id': False})
    
    pandas_df = pd.DataFrame(cursor)
    
    return dg.MaterializeResult(
        metadata={
            "row_count": pandas_df.shape[0],
            "preview": dg.MarkdownMetadataValue(pandas_df.to_markdown(index=False))
        }
    )


@dg.asset(group_name="sources", kinds={"api"})
def extract_api() -> dg.MaterializeResult:
    response = requests.get(
        url="https://reqres.in/api/users?page=2",
        headers={"x-api-key": os.environ["REQRES_API_KEY"]})
    assert response.status_code == 200

    pandas_df = pd.DataFrame(response.json()["data"])

    return dg.MaterializeResult(
        metadata={
            "row_count": pandas_df.shape[0],
            "preview": dg.MarkdownMetadataValue(pandas_df.to_markdown(index=False))
        }
    )


@dg.asset(
    group_name="transformations",
    deps=[extract_csv, extract_mongodb, extract_postgres, extract_api])
def transform():
    pass
