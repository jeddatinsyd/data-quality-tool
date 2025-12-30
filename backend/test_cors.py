import requests

# Test OPTIONS preflight
print("Testing CORS preflight...")
response = requests.options(
    "http://127.0.0.1:8000/api/upload",
    headers={
        "Origin": "http://127.0.0.1:3000",
        "Access-Control-Request-Method": "POST"
    }
)
print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print()

# Test actual POST
print("Testing POST request...")
try:
    files = {'file': ('test.csv', 'id,name\n1,test', 'text/csv')}
    response = requests.post(
        "http://127.0.0.1:8000/api/upload",
        files=files,
        headers={"Origin": "http://127.0.0.1:3000"}
    )
    print(f"Status: {response.status_code}")
    print(f"CORS Header: {response.headers.get('Access-Control-Allow-Origin')}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
