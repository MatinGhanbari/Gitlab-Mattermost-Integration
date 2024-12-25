import time
import psycopg2

from src.constants.users import users
from src.repositories.sql_queries import *
from src.utils.utils import log

class UserRepository:
    def __init__(self, dbname, user, password, host, port):
        while (True):
            try:
                log(f"Connecting to the database {host}:{port}/{dbname}")
                self.conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                self.init_db()
                break
            except:
                log(f"Unable to connect to the database {host}:{port}!")
                log("retrying after 30 seconds...")
                time.sleep(30)

    def init_db(self):
        with self.conn.cursor() as cur:
            try:
                cur.execute(init_db_query)
                self.conn.commit()
            except Exception as e:
                print(e)

            try:
                for user_id in users:
                    user_name = users[user_id]["Name"]
                    cur.execute(insert_user_query.format(user_id, user_name))
                self.conn.commit()
            except Exception as e:
                self.conn.commit()
                print(e)

    def increase_push_count(self, user_id):
        with self.conn.cursor() as cur:
            try:
                cur.execute(increase_push_count_query.format(user_id))
                self.conn.commit()
            except Exception as e:
                print(e)

    def increase_commit_count(self, user_id, commit_count):
        with self.conn.cursor() as cur:
            try:
                cur.execute(increase_commit_count_query.format(commit_count, user_id))
                self.conn.commit()
            except Exception as e:
                print(e)

    def get_user_push_merge_count(self, user_id):
        commit_count = 0
        merge_count = 0
        push_count = 0
        with self.conn.cursor() as cur:
            try:
                cur.execute(get_user_push_merge_count_query.format(user_id))
                row = cur.fetchone()
                if row: commit_count, push_count, merge_count = row
                self.conn.commit()
            except Exception as e:
                print(e)
        return commit_count, push_count, merge_count

    def refresh_counts(self):
        with self.conn.cursor() as cur:
            try:
                cur.execute(refresh_counts_query)
                self.conn.commit()
            except Exception as e:
                print(e)

    def increase_merge_count(self, user_id):
        with self.conn.cursor() as cur:
            try:
                cur.execute(increase_merge_count_query.format(user_id))
                self.conn.commit()
            except Exception as e:
                print(e)
