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
    
    url = "http://localhost:8000/api/fetch_subcats?category=Resistor"
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

    url = "http://localhost:8000/api/search_cats?category=Resistor"
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

    url = "http://localhost:8000/api/search_subcats/?category=Resistor&subcategory=Active"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                print("API request successful:", response.json())
            else:
                print("API request failed:", response.status_code, response.text)
    except Exception as e:
        print("Error during API request:", e)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api())