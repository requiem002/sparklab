# mock_backend.py
from fastapi import FastAPI, Request
from fastapi import Query
app = FastAPI()

#category_list = ['Passive', 'Active']
#@app.get("/components/categories")
#def get_categories():
#    return category_list
    #return list(sorted(set(c['category'] for c in components)))


#API Call for the subcategories
@app.get("/api/fetch_subcats")  
async def get_subcategories(category: str = Query(...)):
    # Example data — normally you'd query from DB or data file
    subcategories_db = {
        "Passive": ["Resistors", "Capacitors", "Inductors"],
        "Active": ["Transistors", "ICs", "LEDs"],
        "Connectors": ["Headers", "Sockets", "Cables"]
    }
    return subcategories_db.get(category, [])

@app.get("/api/fetch_cats")
async def get_categories():
    return ["Passive", "Active", "Connectors"]

@app.get("/api/component_by_serial")
async def get_by_serial(serial: str):
    # In real case: query DB
    components = [
        {"name": "Capacitor_100uF", "serial": "ABC123", "quantity": 40, "location": "A2", "cabinet": "Cabinet_1"},
        {"name": "Resistor_10k", "serial": "XYZ789", "quantity": 20, "location": "C3", "cabinet": "Cabinet_2"},
    ]
    return [c for c in components if c['serial'] == serial] 

@app.get("/api/get_components")
async def get_components(category: str, subcategory: str):
    # Replace with your real DB logic
    return [
        {
            "name": "Resistor_10k",
            "quantity": 120,
            "location": "A1",
            "cabinet": "Cabinet_1"
        },
        {
            "name": "Resistor_10k",
            "quantity": 20,
            "location": "B4",
            "cabinet": "Cabinet_2"
        }
    ]


@app.post("/api/request")
async def handle_request(request: Request):
    data = await request.json()
    print("🛎️ Received request from frontend:", data)
    return {"status": "ok"}