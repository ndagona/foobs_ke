import psycopg2
import pandas as pd
import os


def printer(msg: str) -> None:
    print()
    print()
    print(msg)


class DatabaseConnect:
    def __init__(self):
        self.host = "localhost"
        self.dbname = "dwoperation"
        self.user = "esige"
        self.password = "esige"
        self.port = 5432

    def connect_postgres(self):
        conn = psycopg2.connect(
            host=self.host,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            port=self.port,
        )
        return conn

    def create_table_from_csv(self, conn, table_name, data: pd.DataFrame):
        df = data
        columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
        create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            for _, row in df.iterrows():
                placeholders = ", ".join(["%s"] * len(row))
                insert_query = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
                cur.execute(insert_query, tuple(row))
            conn.commit()

    def main(self, table_name, data: pd.DataFrame) -> None:

        conn = self.connect_postgres()
        self.create_table_from_csv(conn, table_name, data)
        conn.close()
        printer(f"Table '{table_name}' created successfully")


if __name__ == "__main__":
    print("Execution started")
    cls = DatabaseConnect()
    cls.connect_postgres()
    print("Execution ended")
