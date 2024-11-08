import psycopg2
from datetime import datetime
from backend.utils.constants import postgreSQLConstants

db_config = postgreSQLConstants.db_config


def store_embedding_in_postgres(file_name, chunk_text, embedding, chunk_number, page):
    """
    Stores file, chunk, and embedding information in a PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO files (file_name, created_at)
            VALUES (%s, %s)
            ON CONFLICT (file_name) DO NOTHING
            RETURNING id;
        """, (file_name, datetime.now()))

        file_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        if not file_id:
            cursor.execute(
                "SELECT id FROM files WHERE file_name = %s;", (file_name,))
            file_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO chunks (file_id, chunk_text, chunk_number, page, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (file_id, chunk_text, chunk_number, page, datetime.now()))

        chunk_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO embeddings (chunk_id, embedding, created_at)
            VALUES (%s, %s, %s);
        """, (chunk_id, embedding, datetime.now()))

        conn.commit()
        print(
            f"Chunk {chunk_number} embedding for file '{file_name}' (page {page}) successfully stored.")

    except Exception as e:
        print(f"Error storing embedding: {e}")

    finally:
        cursor.close()
        conn.close()


def delete_file_from_postgres(file_name):
    """
    Deletes a file and its associated chunks and embeddings from the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM files WHERE file_name = %s;", (file_name,))
        conn.commit()
        print(f"File '{file_name}' and associated data successfully deleted.")
    except Exception as e:
        print(f"Error deleting file: {e}")
    finally:
        cursor.close()
        conn.close()
