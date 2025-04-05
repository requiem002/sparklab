from nicegui import ui
import json
import os
import httpx


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

    component_input = ui.input(label='Search for component', placeholder='e.g. Resistor_10k').classes('mb-2')
    result_area = ui.column().classes('gap-4')
    quantity_input = ui.number(label='Request quantity').classes('mb-2')
    request_status = ui.label('')

    selected_component = {"name": None}  # To keep track of the last matched component

    def search():
        result_area.clear()
        request_status.text = ''
        name = component_input.value.strip().lower()
        found = False
        for c in component_data:
            if name in c['name'].lower():
                found = True
                selected_component['name'] = c['name']
                with result_area:
                    with ui.card().classes("p-4 w-full shadow-md"):
                        ui.label(f"📦 Name: {c['name']}").classes("text-lg font-bold")
                        ui.label(f"🔢 Quantity: {c['quantity']}")
                        ui.label(f"📍 Location: {c['location']}")
                        ui.label(f"📂 Category: {c['category']} > {c['subcategory']}")
        if not found:
            result_area.clear()
            result_area.append(ui.label("❌ Component not found."))
            selected_component['name'] = None

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
                    # You could emit JSON here for backend interaction

                    # 👉 Send this request to the backend
                    payload = {
                        "user": user_name,
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

    ui.button('🔍 Search', on_click=search).classes('mb-2')
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