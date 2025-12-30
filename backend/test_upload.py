import requests

print("Testing upload with sample_data.csv...")
try:
    with open('../sample_data.csv', 'rb') as f:
        files = {'file': ('sample_data.csv', f, 'text/csv')}
        response = requests.post(
            "http://127.0.0.1:8000/api/upload",
            files=files
        )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"File ID: {data['file_id']}")
        print(f"Columns: {data['columns']}")
        print(f"Preview (first 3 rows):")
        for i, row in enumerate(data['preview'][:3]):
            print(f"  Row {i+1}: {row}")
        print("SUCCESS!")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
