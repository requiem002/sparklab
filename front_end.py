from nicegui import ui, app, context
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
    "il356": "Ian",
    "dms60": "Dylan",
    "oa562": "Toni"
}

# ------------------ Login Screen ------------------

def login_screen():
    ui.query('body').classes('m-0 p-0 bg-gray-900 text-white h-screen overflow-hidden')

    with ui.row().classes('w-full h-screen items-center justify-center'):
        with ui.card().classes('bg-gray-800 p-10 rounded-2xl shadow-2xl w-[600px] max-w-full text-center'):
            ui.image('backend/logo.png').classes('mx-auto mb-4 w-40')
            ui.label('🔐 SparkLab Login').classes('text-2xl font-bold text-cyan-400 mb-4')

            id_input = ui.input(label='Enter your ID').props('dark dense').classes('w-full text-black mb-4')
            status = ui.label('').classes('text-red-400 text-sm')

            def login():
                user_id = id_input.value.strip()
                if user_id in users:
                    ui.navigate.to(f'/dashboard/{user_id}')
                else:
                    status.text = '❌ Invalid User ID'

            ui.button('Login', on_click=login).props('color=primary').classes('w-full')

# ------------------ Dashboard ------------------

def dashboard_screen(user_id: str):
    user_name = users.get(user_id, "Unknown")
    selected_component = {"name": None}
    ui.query('body').classes('m-0 p-0 bg-gray-900 text-white h-screen overflow-hidden')

    with ui.row().classes("w-screen h-[100vh] items-center justify-center overflow-hidden no-wrap"):

        with ui.card().classes("bg-gray-800 p-6 rounded-2xl shadow-xl w-full max-w-4xl max-h-full"):
            ui.label(f"👋 Welcome, {user_name}, to your SparkLab Dashboard").classes("text-3xl font-bold text-white mb-4")

            with ui.grid(columns=2).classes("gap-6 w-full max-h-full"):
                # Serial Search Card

                ##### The Search Bars
                with ui.card().classes("bg-gray-700 p-4 rounded-xl shadow-lg w-full"):
                    ui.label("🔍 Serial ID Search").classes("text-xl font-semibold text-blue-300 mb-2")
                    serial_input = ui.input(label="Serial Number").classes("w-full text-black mb-2")
                    ui.button("Search", on_click=lambda: asyncio.create_task(search_by_serial())).props("color=primary")

                # Component Filter Card
                with ui.card().classes("bg-gray-700 p-6 rounded-xl shadow-lg max-h-full w-full"):
                    ui.label("📂 Category Search").classes("text-xl font-semibold text-purple-300 mb-3")
                    category_dropdown = ui.select([], label="Category", on_change=lambda e: asyncio.create_task(update_subcategories(e)))
                    category_dropdown.props("dark").classes("w-full text-black mb-3")

                    subcategory_dropdown = ui.select([], label="Subcategory", on_change=lambda e: asyncio.create_task(update_components(e)))
                    subcategory_dropdown.props("dark").classes("w-full text-black mb-3")

                    component_dropdown = ui.select([], label="Component", on_change=lambda e: show_component_info(e)).classes("w-full text-black")
                    component_dropdown.props("dark")

                ui.separator()

            # Side-by-side row for Component Info and Request
            with ui.row().classes("w-full gap-6 justify-center"):
                # Component Info (2/3 width)
                with ui.card().classes("bg-gray-700 p-4 rounded-xl shadow-lg w-2/3"):
                    ui.label("🧾 Component Information").classes("text-xl font-semibold text-green-300 mb-2")
                    with ui.scroll_area().classes("max-h-60 overflow-y-auto"):
                        component_info = ui.column().classes("gap-4")

            with ui.row().classes("w-full gap-6 justify-center"):
                # Request (1/3 width)
                with ui.card().classes("bg-gray-700 p-4 rounded-xl shadow-lg w-2/3"):
                    ui.label("📦 Request Component").classes("text-xl font-semibold text-yellow-300 mb-3 ")
                    quantity_input = ui.number(label="Quantity").classes("w-full text-black mb-2")
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
                response = await client.get("http://localhost:8000/api/component_by_serial/", params={"serial": serial})
                if response.status_code == 200:
                    raw = response.json()
                    data = json.loads(raw) if isinstance(raw, str) else raw

                    print("Serial search data:", data)

                    components = data.get("components", [])

                    if not components:
                        with component_info:
                            ui.label("❌ No component found with that serial number")
                        return

                    selected_component['name'] = components[0]['name']

                    with component_info:
                        for c in components:
                            with ui.card().classes("bg-gray-600 p-4 shadow-md text-white rounded-lg"):
                                ui.label(f"📦 {c['name']} (Serial: {serial})").classes("text-lg font-bold")
                                ui.label(f"📍 Cabinet: {c['cabinet_ID']}")
                                ui.label(f"📌 Location: {c['location']}")
                                ui.label(f"🔢 Quantity: {c['quantity']}")
                else:
                    ui.notify("⚠️ Backend error during serial search")
        except Exception as e:
            print("Error in serial search:", e)

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
                with ui.card().classes("bg-gray-600 p-4 shadow-md text-white rounded-lg w-full h-full justify-center"):
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