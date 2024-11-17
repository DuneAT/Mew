from backend.utils.constants import postgreSQLConstants, legifrance_postgreSQLConstants
from datetime import datetime
import psycopg2


db_config = postgreSQLConstants.db_config


# Functions to store and delete data in PostgreSQL

def store_embedding_in_postgres(file_name, chunk_text, embedding, chunk_number, page):
    try:
        # Ensure embedding is a list by extracting if necessary
        if isinstance(embedding, dict) and "embedding" in embedding:
            embedding = embedding["embedding"]

        # Establish connection
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        conn.autocommit = False

        # Insert file into files table if it doesn't exist
        cursor.execute("""
            INSERT INTO files (file_name, created_at)
            VALUES (%s, %s)
            ON CONFLICT (file_name) DO NOTHING;
        """, (file_name, datetime.now()))

        # Fetch the file_id for the given file_name
        cursor.execute(
            "SELECT id FROM files WHERE file_name = %s;", (file_name,))
        row = cursor.fetchone()
        if row:
            file_id = row[0]
        else:
            raise ValueError(f"File '{file_name}' not found in database.")

        # Insert chunk into chunks table with page number
        cursor.execute("""
            INSERT INTO chunks (file_id, chunk_text, chunk_number, page, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (file_id, chunk_text, chunk_number, page, datetime.now()))

        chunk_id = cursor.fetchone()[0]

        # Insert embedding as an array because column type is vector from pgvector extension
        cursor.execute("""
            INSERT INTO embeddings (chunk_id, embedding, created_at)
            VALUES (%s, %s, %s);
        """, (chunk_id, embedding, datetime.now()))  # Insert embedding directly if it's now a list

        conn.commit()
        print(
            f"Chunk {chunk_number} embedding for file '{file_name}' (page {page}) successfully stored.")

    except (ValueError, psycopg2.Error) as e:
        conn.rollback()  # Rollback if any exception occurs
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_file_from_postgres(file_name):
    """
    Deletes a file and its associated chunks and embeddings from the PostgreSQL database.

    Args:
        file_name (str): The name of the file to delete.
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
