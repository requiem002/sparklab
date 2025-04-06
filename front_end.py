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
    "sa2879": "Saad",
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
    selected_component = {"name": None}
    ui.query('body').classes('bg-gray-900 text-white')  # Dark mode styling

    # ------------------ Header ------------------
    with ui.row().classes("w-full justify-between items-center p-4 bg-gradient-to-r from-blue-700 to-indigo-800 shadow-lg"):
        ui.label("🧰 Component Control Dashboard").classes("text-2xl font-bold text-white")
        ui.label(f"👋 Welcome, {user_name}").classes("text-md text-gray-200")

    with ui.grid(columns=2).classes("gap-6 p-6"):

        # Serial Search
        with ui.card().classes("bg-gray-800 p-6 shadow-xl rounded-xl"):
            ui.label("🔎 Serial Search").classes("text-xl font-semibold text-blue-300 mb-3")
            serial_input = ui.input(label="Serial Number").classes("w-full text-black mb-2")
            ui.button("Search", on_click=lambda: asyncio.create_task(search_by_serial())).props("color=primary")

        # Category Filters
        with ui.card().classes("bg-gray-800 p-6 shadow-xl rounded-xl"):
            ui.label("🧠 Smart Filter").classes("text-xl font-semibold text-purple-300 mb-3")
            category_dropdown = ui.select([], label="Category", on_change=lambda e: asyncio.create_task(update_subcategories(e))).classes("w-full text-black mb-2")
            subcategory_dropdown = ui.select([], label="Subcategory", on_change=lambda e: asyncio.create_task(update_components(e))).classes("w-full text-black mb-2")
            component_dropdown = ui.select([], label="Component", on_change=lambda e: show_component_info(e)).classes("w-full text-black")

    # Component Info Section
    ui.label("📦 Component Info").classes("text-2xl text-green-400 px-6 mt-4")
    component_info = ui.column().classes("gap-4 px-6")

    # Request Section
    with ui.card().classes("bg-gray-800 p-6 shadow-xl rounded-xl m-6 max-w-3xl mx-auto"):
        ui.label("📤 Request Component").classes("text-xl font-semibold text-yellow-300 mb-3")
        with ui.row().classes("gap-4"):
            quantity_input = ui.number(label="Quantity").classes("w-full text-black")
            ui.button("Request", on_click=lambda: asyncio.create_task(request_quantity())).props("color=accent")
        request_status = ui.label("").classes("mt-2 text-gray-300")

    # ------------------- Async Functions ------------------

    async def search_by_serial():
        serial = serial_input.value.strip()
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
                    selected_component['name'] = data[0]['name']
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

    async def update_subcategories(e):
        selected_category = e.value
        if not selected_category:
            subcategory_dropdown.options = []
            subcategory_dropdown.update()
            return
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/fetch_subcats/", params={"category": selected_category})
                if response.status_code == 200:
                    data = response.json()
                    subcategory_list = [item["subcategory"] for item in data["subcategories"]]
                    subcategory_dropdown.options = subcategory_list
                    subcategory_dropdown.update()
        except Exception as e:
            print("Error fetching subcategories:", e)

    async def fetch_categories():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/fetch_cats")
                if response.status_code == 200:
                    data_raw = response.json()
                    if isinstance(data_raw, str):
                        data = json.loads(data_raw)
                    else:
                        data = data_raw
                    categories = [entry["category"] for entry in data["categories"]]
                    category_dropdown.options = categories
                    category_dropdown.update()
        except Exception as e:
            print("Error fetching categories:", e)

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
                    component_dropdown.options = component_names
                    component_dropdown.metadata = components
                    component_dropdown.update()
        except Exception as e:
            print("Error fetching components:", e)

    def show_component_info(e):
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

        matching_components = [c for c in component_dropdown.metadata if c["name"] == name]
        if not matching_components:
            request_status.text = '❌ Please search and select a valid component first.'
            return
        selected_serial = matching_components[0]["serialID"]
        if req_qty <= matching_components[0]["quantity"]:
            request_status.text = f'✅ {req_qty} of "{name}" requested successfully.'
            payload = {
                "user": user_name,
                "serial": selected_serial,
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
        else:
            request_status.text = '❌ Not enough stock available.'

    ui.timer(0.1, fetch_categories, once=True)

# ------------------ Routing ------------------

@ui.page('/')
def main_page():
    login_screen()

@ui.page('/dashboard/{user_id}')
def dashboard(user_id: str):
    dashboard_screen(user_id)

# ------------------ Run the App ------------------

ui.run(title="Component Storage System")