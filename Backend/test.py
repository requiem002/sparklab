from Database import *
from JsonPacker import *

def main():
    db = Database("example.db")
    db.create_table()
    if(db.isTableEmpty()):
        db.fill_random_electronic(10)  # Fill the table with 10 random electronic components
    users = db.search_all("SELECT * FROM components;") 
    for user in users:    
        print(user)
    db.close_connection()
    json = convert_db_response_to_json(users)  # Convert the database response to JSON
    print("JSON conversion complete.")
    print(json)  # Print the JSON output
    



if __name__ == "__main__":
    main()