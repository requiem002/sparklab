from fastapi import FastAPI, HTTPException, Request
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

@app.get("/api/fetch_subcats/")
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

@app.get("/api/search_cats/")
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

@app.get("/api/get_components/")
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

@app.get("/api/component_by_serial/")
async def search_id(serial: str):
    """
    Fetches components based on the provided serial ID.
    """
    try:
        db_response = db.search_componet_by_serialID(serial)
        json_response = convert_db_response_to_json(db_response) 
    except Exception as e:
        print(f"An error occurred while fetching components: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")
    return json_response

@app.get("/api/search_item/")
async def search_item(category: str, subcategory: str, value: str):
    """
    Fetches components based on the provided name.
    """
    try:
        db_response = db.search_component_by_category_subcategory_and_value(category, subcategory, value)
        json_response = convert_db_response_to_json(db_response) 
    except Exception as e:
        print(f"An error occurred while fetching components: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")
    return json_response

@app.post("/api/request")
async def handle_request(request: Request):
    """
    Handles incoming POST requests with JSON data.
    FastAPI automatically parses and validates the JSON based on the type hint.
    Processes the data and returns a JSON response.
    """
    try:
        # Parse the incoming JSON request
        data = await request.json()
        serial = data.get("serial")
        quantity = data.get("quantity")
        print(f"Received request data: {data}")  # Debugging line
        if not serial or not quantity:
            raise ValueError("Missing required fields: 'serial' and 'quantity'")
        elif quantity < 0:
            raise ValueError("Quantity must be a positive integer")
        
        searchIDResult = db.search_componet_by_serialID(serial)
        if searchIDResult is None:
            raise ValueError("Serial ID not found in the database")
        elif searchIDResult[0][7] < quantity or searchIDResult[0][7] <= 0:
            raise ValueError("Insufficient quantity in the database")
        db.subtract_quantity(serial, quantity)  # Update the database with the new quantity
        # update arduino drawer
        return {"status": "ok"}
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail="Invalid input data")
    except ValueError as e:
        print(f"Value error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")

# Check if the script is being run directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)