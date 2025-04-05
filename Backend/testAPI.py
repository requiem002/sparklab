import httpx

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
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)
    print("Completed API request - fetch_cats")

    url = "http://localhost:8000/api/fetch_subcats/?category=Resistor"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)
    print("Completed API request - fetch_subcats")

    url = "http://localhost:8000/api/search_cats/?category=Resistor"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)
    print("Completed API request - search_cats")

    url = "http://localhost:8000/api/get_components/?category=Resistor&subcategory=Active"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)
    print("Completed API request - get_components")

    url = "http://localhost:8000/api/component_by_serial/?serial=SERIAL_1"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)
    print("Completed API request - component_by_serial")

    url = "http://localhost:8000/api/search_item/?category=Resistor&subcategory=Passive&value=Value_0"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                # print("API request successful:", response.json())
                pass
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)
    print("Completed API request - search_item")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api())