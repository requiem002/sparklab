from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, ValidationError
from typing import Dict, Any

from Database import Database # Import the Database class from your Database module
from JsonPacker import * # Import the JSON conversion function if needed

# Create a FastAPI application instance
app = FastAPI()
db = Database("example.db") # Initialize the database connection
db.create_table() # Create the table if it doesn't exist
if db.isTableEmpty(): # Check if the table is empty
    db.fill_random_electronic(10)  # Fill the table with 10 random electronic components


@app.get("/api/fetch_cats")
async def get_categories():
    """
    Handles incoming POST requests with JSON data.
    FastAPI automatically parses and validates the JSON based on the type hint.
    Processes the data and returns a JSON response.
    """
    try:

        # Prepare the response data
        db_response = db.get_unique_categories() 
        json_response = convert_catergory_to_json(db_response) 
        print(f"JSON response: {json_response}") 
        return json_response

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")

@app.get("/api/fetch_subcats")
async def get_subcategories(category: str):
    """
    Fetches subcategories based on the provided category.
    """
    try:
        # Example data — normally you'd query from DB or data file
        db_response = db.get_unique_sub_categories(category)
        json_response = convert_subcategory_to_json(db_response)
    except Exception as e:
        print(f"An error occurred while fetching subcategories: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")
    return json_response

@app.get("/api/search_cats")
async def search_cats(category: str):
    """
    Fetches components based on the provided category and subcategory.
    """
    try:
        db_response = db.search_component_by_category(category)
        json_response = convert_db_response_to_json(db_response) 
    except Exception as e:
        print(f"An error occurred while fetching components: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")
    return json_response

@app.get("/api/search_subcats/")
async def search_subcats(category: str, subcategory: str):
    """
    Fetches components based on the provided category and subcategory.
    """
    try:
        db_response = db.search_component_by_category_and_sub_category(category, subcategory)
        json_response = convert_db_response_to_json(db_response) 
    except Exception as e:
        print(f"An error occurred while fetching components: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")
    return json_response

# Check if the script is being run directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)