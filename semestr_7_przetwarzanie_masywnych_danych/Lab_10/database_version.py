import codecs
import sqlite3, csv
from datetime import datetime

SOURCE_FILE_NAME = 'facts.csv'


def create_facts_table(conn):
    conn.execute('DROP TABLE IF EXISTS facts')
    sql = '''
    CREATE TABLE facts (
      user_id     INTEGER NOT NULL,
      song_id     INTEGER NOT NULL,
      UNIQUE(user_id, song_id)
    )
    '''
    conn.execute(sql)


def insert_into_facts(conn):
    with open(SOURCE_FILE_NAME,'r') as f:
        reader = csv.DictReader(f)
        records = [(row['user_id'], row['song_id']) for row in reader]

        sql_command = "INSERT OR REPLACE INTO facts (user_id, song_id) VALUES (:user_id, :song_id)"
        print('LOAD started')
        conn.executemany(sql_command, records)


def create_facts_indexes(conn):
    conn.execute('DROP INDEX IF EXISTS facts_user_id_index')
    conn.execute('CREATE INDEX facts_user_id_index ON facts (user_id)')
    conn.execute('DROP INDEX IF EXISTS facts_song_id_index')
    conn.execute('CREATE INDEX facts_song_id_index ON facts (song_id)')


def create_similarity_table(conn):
    conn.execute('DROP TABLE IF EXISTS similarity')
    sql = '''
    CREATE TABLE similarity (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id     INTEGER NOT NULL,
      partner_id  INTEGER NOT NULL,
      value       INTEGER NOT NULL
    )
    '''
    conn.execute(sql)


def create_similarity_indexes(conn):
    conn.execute('DROP INDEX IF EXISTS similarity_index')
    conn.execute('CREATE INDEX similarity_index ON similarity (user_id, value)')


def maximum_user_id(conn):
    sql = '''
    SELECT max(user_id) FROM FACTS LIMIT 1;
    '''
    return conn.execute(sql)


def show(row):
    print(' '.join([str(i) for i in row]))


def exercise_1(conn):
    sql = '''
    SELECT tracks.title, tracks.artist, sub.total_count
    FROM (
      SELECT
        song_id,
        COUNT(song_id) AS total_count
      FROM
        samples
      GROUP BY
        song_id
      ORDER BY
        total_count DESC
      LIMIT 10
    ) sub
    INNER JOIN tracks ON (tracks.song_id = sub.song_id)
    ORDER BY sub.total_count DESC;
    '''

    return conn.execute(sql)


def main():
    # Set connection with SQLite database
    conn = sqlite3.connect('pmd.db')
    # conn = sqlite3.connect(':memory:')

    # Create facts table
    create_facts_table(conn)
    print('Facts table created')

    # Prepare and load data to table
    insert_into_facts(conn)
    print('Records inserted into facts')

    create_facts_indexes(conn)
    print('Facts table - indexes ready')

    create_similarity_table(conn)
    print('Similarity table created')

    sed '1d' facts.csv > facts_no_header.csv
    DROP TABLE IF EXISTS facts;
    CREATE TABLE facts (
      user_id     INTEGER NOT NULL,
      song_id     INTEGER NOT NULL,
      UNIQUE(user_id, song_id)
    );
    .mode csv
    .separator ','
    .import facts_no_header.csv facts

    SELECT
        *,
        COUNT(song_id) AS total_count
    FROM
        facts
    WHERE
        user_id == 1
        AND
        

    # max_user_id = 0
    # for row in maximum_user_id(conn):
    #     max_user_id = row[0]
    # print(f'Max UserID = {max_user_id}')

    # for user_id in range(1, max_user_id):
        # prepare_jaccard_index(conn, user_id)

    # # Exercise 1
    # for row in exercise_1(conn):
    #     show(row)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
