from nicegui import ui, app
import json
import os
import httpx
import asyncio


# ------------------ Load Component Data from JSON ------------------

json_path = os.path.join(os.path.dirname(__file__), 'components.json')

folder = os.path.dirname(__file__)
print("Files in folder:", os.listdir(folder))

with open(json_path, 'r') as file:
    component_data = json.load(file)['components']

# Simulated user login database
users = {
    "abc123": "Alice",
    "xyz789": "Bob",
    "test001": "Charlie"
}

# ------------------ Login Screen ------------------

def login_screen():
    ui.label('🔐 Login to Component System').classes('text-2xl mb-4')
    id_input = ui.input(label='Enter User ID').classes('mb-2')
    status = ui.label('')

    def login():
        user_id = id_input.value.strip()
        if user_id in users:
            ui.navigate.to(f'/dashboard/{user_id}')
        else:
            status.text = '❌ Invalid User ID'

    ui.button('Login', on_click=login)

# ------------------ Dashboard ------------------


def dashboard_screen(user_id: str):
    user_name = users.get(user_id, "Unknown")
    ui.label(f'👋 Welcome, {user_name}').classes('text-xl mb-4')

    serial_input = ui.input(label="Search by Serial Number").classes("mb-2")
    ui.button("🔍 Search Serial", on_click=lambda: asyncio.create_task(search_by_serial())).classes("mb-4")

    #component_input = ui.input(label='Search for component', placeholder='e.g. Resistor_10k').classes('mb-2')
    category_dropdown = ui.select([], label='Select Category', on_change=lambda e: asyncio.create_task(update_subcategories(e)))
    category_dropdown.classes('mb-2')
    
    subcategory_dropdown = ui.select([], label='Select Subcategory', on_change=lambda e: asyncio.create_task(update_components(e)))
    subcategory_dropdown.classes('mb-2')

    component_dropdown = ui.select([], label='Select Component', on_change= lambda e: show_component_info(e))
    component_dropdown.classes('mb-2')

    ###########################
    async def search_by_serial():
        
        serial = serial_input.value.strip()

        print(f"Serial: {serial}")
        if not serial:
            ui.notify("⚠️ Enter a serial number")
            return

        component_info.clear()
        selected_component['name'] = None

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/component_by_serial", params={"serial": serial})
                if response.status_code == 200:
                    data = response.json()
                    if not data:
                        with component_info:
                            ui.label("❌ No component found with that serial number")
                        return

                    selected_component['name'] = data[0]['name']  # Save for requesting
                    with component_info:
                        for c in data:
                            with ui.card().classes("p-4 shadow-md"):
                                ui.label(f"📦 {c['name']} (Serial: {serial})").classes("text-lg font-bold")
                                ui.label(f"📍 Cabinet: {c['cabinet']}")
                                ui.label(f"📌 Location: {c['location']}")
                                ui.label(f"🔢 Quantity: {c['quantity']}")
                else:
                    ui.notify("⚠️ Backend error during serial search")
        except Exception as e:
            print("Error in serial search:", e)
            ui.notify(f"❌ Error: {e}")
    
    #################################
    #Fetch a list of relevant subcategories for given category!
    async def update_subcategories(e):
        selected_category = e.value
        print("Category selected:", e.value)
        if not selected_category:
            subcategory_dropdown.options = []
            subcategory_dropdown.update()
            return

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/fetch_subcats/", params={"category": selected_category})

                print(f"Response: {response}")
                if response.status_code == 200:
                    data = response.json()

                    subcategory_list = [item["subcategory"] for item in data["subcategories"]]
                    subcategory_dropdown.options = subcategory_list
                    subcategory_dropdown.update()
                    #print(f"Subcategories for {selected_category}:", subcategory_list)
                else:
                    subcategory_dropdown.options = []
                    subcategory_dropdown.update()
                    print("⚠️ Failed to load subcategories")

        except Exception as e:
            print("Error fetching subcategories:", e)


    #fetch list of available categories
    async def fetch_categories():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/fetch_cats")
                
                if response.status_code == 200:
                    data_raw = response.json()

                    if isinstance(data_raw, str):
                        data = json.loads(data_raw)  # <-- This fixes the double-encoded string
                    else:
                        data = data_raw

                    categories = [entry["category"] for entry in data["categories"]]
                    category_dropdown.options = categories
                    category_dropdown.update()

                else:
                    category_dropdown.options = []
        except Exception as e:
            print("Error fetching categories:", e)
            #ui.notify("❌ Backend connection error")

    ui.timer(0.1, fetch_categories, once=True)
    component_info = ui.column().classes('gap-2 mt-2')
    result_area = ui.column().classes('gap-4')
    quantity_input = ui.number(label='Request quantity').classes('mb-2')
    request_status = ui.label('')
    selected_component = {"name": None}  # To keep track of the last matched component


    #get relevant components
    async def update_components(e):
        selected_subcategory = e.value
        selected_category = category_dropdown.value

        if not selected_category or not selected_subcategory:
            component_dropdown.options = []
            component_dropdown.update()
            return

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/get_components/", params={
                    "category": selected_category,
                    "subcategory": selected_subcategory
                })
                if response.status_code == 200:
                    data = response.json()

                    components = data["components"]                    
                    component_names = sorted(set(item["name"] for item in components))

                    # Group by component name (ignore cabinet for now)
                    component_dropdown.options = component_names
                    component_dropdown.update()

                    # Save full component list for later display
                    component_dropdown.metadata = components  # attach raw data
                    print("✅ Components loaded:", component_names)
                else:
                    component_dropdown.options = []
                    component_dropdown.update()
                    ui.notify("⚠️ Failed to load components")
        except Exception as e:
            print("Error fetching components:", e)
            #ui.notify("❌ Backend connection error")


     # 🔍 Show details of selected component (multiple cabinets)
    def show_component_info(e):
        print(e)
        selected_name = e.value
        selected_component['name'] = selected_name
        matches = [c for c in component_dropdown.metadata if c['name'] == selected_name]

        component_info.clear()
        if not matches:
            component_info.append(ui.label("❌ No info found"))
            return

        with component_info:
            for c in matches:
                with ui.card().classes("p-4 shadow-md"):
                    ui.label(f"📦 {c['name']}").classes("text-lg font-bold")
                    ui.label(f"📍 Cabinet: {c['cabinet_ID']}")
                    ui.label(f"📌 Location: {c['location']}")
                    ui.label(f"🔢 Quantity: {c['quantity']}")

    async def request_quantity():
        name = selected_component['name']
        try:
            req_qty = int(quantity_input.value or 0)
        except ValueError:
            request_status.text = "❌ Please enter a valid number."
            return

        for c in component_data:
            if c['name'] == name:
                if req_qty <= c['quantity']:
                    request_status.text = f'✅ {req_qty} of "{name}" requested successfully.'
                    # 👉 Send this request to the backend
                    payload = {
                        "serial_id": user_name,
                        "component": name,
                        "quantity": req_qty
                    }

                    try:
                        async with httpx.AsyncClient() as client:
                            response = await client.post("http://localhost:8000/api/request", json=payload)
                            if response.status_code == 200:
                                request_status.text += " (✅ Backend notified)"
                            else:
                                request_status.text += " (⚠️ Backend error)"
                    except Exception as e:
                        request_status.text += f" (❌ Failed to notify backend: {e})"
                        print(e)


                else:
                    request_status.text = '❌ Not enough stock available.'
                return
        request_status.text = '❌ Please search and select a valid component first.'



    ui.button('📤 Request', on_click=request_quantity).classes('mb-4')

# ------------------ Routing ------------------

@ui.page('/')
def main_page():
    login_screen()

@ui.page('/dashboard/{user_id}')
def dashboard(user_id: str):
    dashboard_screen(user_id)



# ------------------ Run the App ------------------

ui.run(title="Component Storage System")