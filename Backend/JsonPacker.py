import json

def convert_db_response_to_json(db_response):
    """
    Converts a database response (list of tuples) from the 'items' table
    into a JSON list with the specified format.

    Args:
        db_response (list): A list of tuples, where each tuple represents a row
                           from the 'items' table (name, category, sub_category,
                           cabinet_ID, location, quantity).

    Returns:
        str: A JSON string representing the data in the desired format.
    """
    components_list = []
    for row in db_response:
        component = {
            "name": row[1],
            "serialID": row[2],
            "category": row[3],
            "sub_category": row[4],
            "cabinet_ID": row[5],
            "location": row[6],
            "quantity": row[7],
            "value": row[8]
        }
        components_list.append(component)

    json_output = {
        "components": components_list
    }

    return json.dumps(json_output, indent=4)

def convert_catergory_to_json(db_response):
    """
    Converts a database response (list of tuples) from the 'items' table
    into a JSON list with the specified format.

    Args:
        db_response (list): A list of tuples, where each tuple represents a row
                           from the 'items' table (name, category, sub_category,
                           cabinet_ID, location, quantity).

    Returns:
        str: A JSON string representing the data in the desired format.
    """
    components_list = []
    for row in db_response:
        component = {
            "category": row[0]
        }
        components_list.append(component)

    json_output = {
        "components": components_list
    }

    return json.dumps(json_output, indent=4)

def convert_subcategory_to_json(db_response):
    """
    Converts a database response (list of tuples) from the 'items' table
    into a JSON list with the specified format.

    Args:
        db_response (list): A list of tuples, where each tuple represents a row
                           from the 'items' table (name, category, sub_category,
                           cabinet_ID, location, quantity).

    Returns:
        str: A JSON string representing the data in the desired format.
    """
    components_list = []
    for row in db_response:
        component = {
            "subcategory": row[0]
        }
        components_list.append(component)

    json_output = {
        "components": components_list
    }

    return json.dumps(json_output, indent=4)