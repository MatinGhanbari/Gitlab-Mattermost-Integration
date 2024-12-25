init_db_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        today_commit_count INTEGER NOT NULL DEFAULT 0,
        today_push_count INTEGER NOT NULL DEFAULT 0,
        today_merge_request_count INTEGER NOT NULL DEFAULT 0
    )
"""

insert_user_query="""
    INSERT INTO users (id, username, today_commit_count, today_push_count, today_merge_request_count)
    VALUES ({}, '{}', 0, 0, 0)
"""

increase_push_count_query = """
    UPDATE users SET today_push_count=today_push_count+1 WHERE id = {}
"""

increase_commit_count_query = """
    UPDATE users SET today_commit_count=today_commit_count+{} WHERE id = {}
"""

increase_merge_count_query = """
    UPDATE users SET today_merge_request_count=today_merge_request_count+1 WHERE id = {}
"""

get_user_push_merge_count_query="""
    SELECT today_commit_count, today_push_count, today_merge_request_count FROM users WHERE id = {}
"""

refresh_counts_query = """
    UPDATE users SET today_commit_count = 0, today_push_count = 0, today_merge_request_count = 0;
"""