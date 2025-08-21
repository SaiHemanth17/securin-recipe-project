import json
import psycopg2
import math

# --- IMPORTANT: Replace with your actual PostgreSQL connection details ---
DB_NAME = "recipes_db"  
DB_USER = "postgres"    
DB_PASS = "Nvrrnmsh@17" 
DB_HOST = "localhost"   
DB_PORT = "5432"        


def clean_value(value):
    """Converts NaN float values to None (for SQL NULL)."""
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

def create_table():
    """Creates the recipes table if it doesn't exist."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # SQL to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS recipes (
            id SERIAL PRIMARY KEY,
            cuisine VARCHAR(255),
            title VARCHAR(255) NOT NULL,
            rating FLOAT,
            prep_time INT,
            cook_time INT,
            total_time INT,
            description TEXT,
            nutrients JSONB,
            serves VARCHAR(50)
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'recipes' created successfully or already exists.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while creating table: {error}")

    finally:
        if conn:
            cur.close()
            conn.close()

def import_recipes_to_db(json_file_path):
    """Parses a JSON file and inserts recipe data into the PostgreSQL database."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        with open(json_file_path, 'r') as f:
            recipes = json.load(f)

        for recipe in recipes:
            rating = clean_value(recipe.get('rating'))
            prep_time = clean_value(recipe.get('prep_time'))
            cook_time = clean_value(recipe.get('cook_time'))
            total_time = clean_value(recipe.get('total_time'))

            insert_query = """
                INSERT INTO recipes (
                    cuisine, title, rating, prep_time, cook_time, total_time,
                    description, nutrients, serves
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            record_to_insert = (
                recipe.get('cuisine'),
                recipe.get('title'),
                rating,
                prep_time,
                cook_time,
                total_time,
                recipe.get('description'),
                json.dumps(recipe.get('nutrients')),
                recipe.get('serves')
            )

            cur.execute("TRUNCATE TABLE recipes RESTART IDENTITY;")
            cur.execute(insert_query, record_to_insert)
            

        conn.commit()
        print(f"{len(recipes)} recipes have been successfully imported.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL or importing data: {error}")

    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_table()
    import_recipes_to_db('recipes.json')
