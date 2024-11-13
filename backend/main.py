from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import ask_routes, file_routes
from backend.utils import constants
import atexit
import psycopg2
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(ask_routes.router)
app.include_router(file_routes.router)

app.mount("/uploads", StaticFiles(directory="temp"), name="uploads")

# Database configuration (replace with your actual configuration)
db_config = constants.postgreSQLConstants.db_config

# Function to delete data from PostgreSQL on server shutdown


def delete_temp_data():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # SQL command to delete temporary data (adjust based on your table and conditions)
        delete_query = """DELETE FROM files;
                        DELETE FROM chunks;
                        DELETE FROM embeddings;"""
        cursor.execute(delete_query)

        connection.commit()
        print("Temporary data deleted from PostgreSQL.")

    except Exception as e:
        print(f"Error deleting temporary data: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Register the database cleanup function to run on server shutdown
atexit.register(delete_temp_data)
