import psycopg2
import pandas as pd


def fetchData(sqlQuery) -> pd.DataFrame:
    conn = psycopg2.connect(
        dbname="dwoperation",
        user="esige",
        password="esige",
        host="localhost",
        port=5432,
    )

    with conn.cursor() as cur:
        cur.execute(sqlQuery)
        data = cur.fetchone()
        print(data)


def getQuery() -> str:
    with open(
        "C:/Users/Esige Ndagona/Desktop/Migration FOOBS/Kenya/PostgresSQL/CoreRaw.sql",
        "r",
        encoding="utf-8",
    ) as file:
        query = file.read()
        print()
        print()
        print()
        print()
        print(query)
        print()
        print()
        print()
        return query


if __name__ == "__main__":
    sqlQuery = getQuery()
    fetchData(sqlQuery)
