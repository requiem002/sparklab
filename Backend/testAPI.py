import httpx
import json

async def test_api():
    # tempJson = {
    #     ""
    # }
    url = "http://localhost:8000/api/fetch_cats"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                print("Completed API request - fetch_cats")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/fetch_subcats/?category=Resistor"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                print("Completed API request - fetch_subcats")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/fetch_subcats/?category=Resist"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:",response.json().get("subcategories"), len(response.json().get("subcategories")))
                if response.json().get("subcategory") is None:
                    print("Completed API request - fetch_subcats(invalid category)")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/search_cats/?category=Resistor"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                print("Completed API request - search_cats")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/search_cats/?category=Resist"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json().get("components"), len(response.json().get("components")))
                if len(response.json().get("components")) == 0:
                    print("Completed API request - search_cats(invalid category)")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/get_components/?category=Resistor&subcategory=Active"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                print("Completed API request - get_components")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/get_components/?category=Resistor&subcategory=Resistor"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                if len(response.json().get("components")) == 0:
                    print("Completed API request - get_components (invalid subcategory)")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/component_by_serial/?serial=SERIAL_1"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                print("Completed API request - component_by_serial")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/component_by_serial/?serial=aaaaa"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                if len(json.loads(response.json()).get("components")) == 0:
                    print("Completed API request - component_by_serial (invalid serial)")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/search_item/?category=Resistor&subcategory=Passive&value=Value_0"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                print("Completed API request - search_item")    
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/search_item/?category=Resistor&subcategory=Passive&value=Value_1"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                if len(json.loads(response.json()).get("components")) == 0:
                    print("Completed API request - search_item (invalid value)")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

    url = "http://localhost:8000/api/request"
    json_package = {
        "serial": "SERIAL_5",
        "quantity": 1
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=json_package)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                print ("Completed API request - request")
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api())