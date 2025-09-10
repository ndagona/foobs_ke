import psycopg2
import pandas as pd
from PostgresSQL.queryData import getQuery


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
        # Convert pd.NA and np.nan to None for DB compatibility
        df = df.where(pd.notna(df), None)
        columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
        create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        drop_table_query = f'DROP TABLE IF EXISTS "{table_name}";'

        with conn.cursor() as cur:
            cur.execute(drop_table_query)  # Drop table if exists
            cur.execute(create_table_query)
            for _, row in df.iterrows():
                placeholders = ", ".join(["%s"] * len(row))
                insert_query = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
                cur.execute(insert_query, tuple(row))
            conn.commit()

    def queryData(self, sqlQuery, conn) -> pd.DataFrame:
        try:
            with conn.cursor() as cur:
                cur.execute(sqlQuery)
                data = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            printer(f"Failed to execute because : {e}")
            return pd.DataFrame([1, 2, 3, 4, 5, 6, 7, 8])

    def main(self, table_name, data: pd.DataFrame) -> None:

        conn = self.connect_postgres()
        self.create_table_from_csv(conn, table_name, data)
        conn.close()
        printer(f"Table '{table_name}' created successfully")


if __name__ == "__main__":
    sqlQuery = getQuery()
    print("Execution started")
    cls = DatabaseConnect()
    conn = cls.connect_postgres()
    data = cls.queryData(sqlQuery, conn)
    printer(data)
    print("Execution ended")
