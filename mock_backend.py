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



@app.post("/api/request")
async def handle_request(request: Request):
    data = await request.json()
    print("🛎️ Received request from frontend:", data)
    return {"status": "ok"}