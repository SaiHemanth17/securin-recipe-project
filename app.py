from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
import json
import re

# --- IMPORTANT: Replace with your actual PostgreSQL connection details ---
DB_NAME = "recipes_db"  # The name you chose in step 3.1
DB_USER = "postgres"    # Your PostgreSQL username (default is postgres)
DB_PASS = "Nvrrnmsh@17" # The password you set during installation
DB_HOST = "localhost"   # Usually correct if the DB is on your machine
DB_PORT = "5432"        # The default PostgreSQL port


app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the database."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    return conn

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/recipes', methods=['GET'])
def get_all_recipes():
    """API endpoint to get all recipes, paginated and sorted by rating."""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    offset = (page - 1) * limit

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT COUNT(*) FROM recipes;")
    total = cur.fetchone()[0]

    cur.execute("SELECT * FROM recipes ORDER BY rating DESC NULLS LAST LIMIT %s OFFSET %s;", (limit, offset))
    recipes = [dict(row) for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": recipes
    })

@app.route('/api/recipes/search', methods=['GET'])
def search_recipes():
    """API endpoint to search for recipes based on multiple filters."""
    query_params = []
    sql_conditions = []

    title = request.args.get('title')
    if title:
        sql_conditions.append("title ILIKE %s")
        query_params.append(f"%{title}%")

    cuisine = request.args.get('cuisine')
    if cuisine:
        sql_conditions.append("cuisine ILIKE %s")
        query_params.append(f"%{cuisine}%")

    for param in ['rating', 'total_time']:
        val = request.args.get(param)
        if val:
            match = re.match(r"(>=|<=|>|<)(\d+\.?\d*)", val)
            if match:
                operator, number = match.groups()
                sql_conditions.append(f"{param} {operator} %s")
                query_params.append(float(number))

    calories = request.args.get('calories')
    if calories:
        match = re.match(r"(>=|<=|>|<)(\d+)", calories)
        if match:
            operator, number = match.groups()
            sql_conditions.append(f"CAST(SPLIT_PART(nutrients->>'calories', ' ', 1) AS INTEGER) {operator} %s")
            query_params.append(int(number))

    base_query = "SELECT * FROM recipes"
    if sql_conditions:
        base_query += " WHERE " + " AND ".join(sql_conditions)

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(base_query, tuple(query_params))
    recipes = [dict(row) for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify({"data": recipes})

if __name__ == '__main__':
    app.run(debug=True)
