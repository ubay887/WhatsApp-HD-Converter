import requests
import sys


def test_health():
    """Test health endpoint"""
    try:
        print("Testing health endpoint...")
        response = requests.get("http://127.0.0.1:5000/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_root():
    """Test root endpoint"""
    try:
        print("\nTesting root endpoint...")
        response = requests.get("http://127.0.0.1:5000/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("WhatsApp HD Converter - API Test")
    print("=" * 50)
    print("\nMake sure the server is running first!")
    print("Run: python app.py")
    print("\n" + "=" * 50 + "\n")

    health_ok = test_health()
    root_ok = test_root()

    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Health endpoint: {'✓ PASS' if health_ok else '✗ FAIL'}")
    print(f"Root endpoint: {'✓ PASS' if root_ok else '✗ FAIL'}")
    print("=" * 50)

    sys.exit(0 if (health_ok and root_ok) else 1)
