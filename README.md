# Securin Recipe Finder Project

This project is a full-stack web application that allows users to browse, search, and view recipes. It includes a PostgreSQL database, a Python Flask backend API, and a dynamic frontend built with HTML, CSS, and JavaScript.

## Features

- **Recipe Database**: Stores recipe information in a PostgreSQL database.
- **RESTful API**: Exposes endpoints to fetch and search for recipes.
- **Pagination**: Fetches recipes in a paginated manner.
- **Search & Filter**: Allows filtering recipes by title and cuisine.
- **Detailed View**: A slide-in drawer shows detailed information for each recipe.
- **Responsive UI**: A clean and simple user interface.

## Project Structure

```
securin-recipe-project/
│
├── app.py                 # Main Flask API application
├── import_data.py         # Script to populate the database
├── recipes.json           # Raw recipe data
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── templates/
│   └── index.html         # Frontend HTML
│
└── static/
    ├── css/
    │   └── style.css      # Stylesheet
    └── js/
        └── script.js      # Frontend JavaScript
```

## Setup and Installation

### 1. Prerequisites

- Python 3.x
- PostgreSQL
- pip (Python package installer)

### 2. Clone the Repository

```bash
git clone <your-git-repo-url>
cd securin-recipe-project
```

### 3. Install Dependencies

Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 4. Database Setup

1.  **Create a PostgreSQL database.** For example, named `recipes_db`.
2.  **Update Database Credentials**: Open `import_data.py` and `app.py` and replace the placeholder values for `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`, and `DB_PORT` with your actual PostgreSQL credentials.
3.  **Run the Import Script**: Execute the following command to create the `recipes` table and populate it with data from `recipes.json`.

    ```bash
    python import_data.py
    ```

## How to Run the Application

Once the setup is complete, run the Flask application:

```bash
flask run
# or
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### 1. Get All Recipes

- **URL**: `/api/recipes`
- **Method**: `GET`
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `limit`: Recipes per page (default: 10)
- **Example Request**:
  `GET http://127.0.0.1:5000/api/recipes?page=1&limit=15`

### 2. Search Recipes

- **URL**: `/api/recipes/search`
- **Method**: `GET`
- **Query Parameters**:
  - `title`: Partial match on recipe title.
  - `cuisine`: Exact match on cuisine.
  - `rating`, `total_time`, `calories`: Filter with operators (e.g., `>=4`, `<=400`).
- **Example Request**:
  `GET http://127.0.0.1:5000/api/recipes/search?title=pie&rating=>=4.5`
