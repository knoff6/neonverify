import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_login(username, password, description):
    print(f"Testing: {description}")
    try:
        response = requests.post(f"{BASE_URL}/login", data={'username': username, 'password': password}, allow_redirects=False)
        
        if response.status_code == 302 and '/dashboard' in response.headers.get('Location', ''):
            print(f"[SUCCESS] Login successful! Redirected to dashboard.")
            return True
        else:
            print(f"[FAILURE] Login failed. Status Code: {response.status_code}, Location: {response.headers.get('Location')}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect: {e}")
        return False

if __name__ == "__main__":
    # Test 1: Valid Credentials
    test_login('guest', 'guest', 'Valid Credentials (guest/guest)')

    # Test 2: SQL Injection
    test_login("' OR 1=1 --", 'anything', 'SQL Injection (\' OR 1=1 --)')
