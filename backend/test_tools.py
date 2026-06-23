import requests
import json

BASE_URL = "http://localhost:8002"

print("Testing Enterprise AI Assistant Tools\n")
print("="*60)

def test_tool(name, question):
    print(f"\n{name}")
    print("-" * 60)
    print(f"Question: {question}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/ask",
            json={"question": question},
            timeout=30
        )
        result = response.json()
        print(f"Status: {response.status_code}")
        if result.get("success"):
            print(f"Answer:\n{result.get('answer')}")
        else:
            print(f"Error: {result.get('error')}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

print("\n1. GET EMPLOYEE INFO TOOL")
test_tool("Test 1a", "Who is John Smith and what is his position?")

print("\n\n2. LIST EMPLOYEES TOOL")
test_tool("Test 2a", "List all employees in the Engineering department")

print("\n\n3. CREATE TICKET TOOL")
test_tool("Test 3a", "Create a high priority ticket about the server being down and assign it to Michael Chen")

print("\n\n4. GET TICKET STATUS TOOL")
test_tool("Test 4a", "What tickets are currently open?")

print("\n\n5. GENERATE REPORT TOOL")
test_tool("Test 5a", "Generate an employee summary report")

print("\n\n6. CONVERSATION MEMORY TEST")
test_tool("Test 6a", "Who is Sarah Johnson?")
test_tool("Test 6b", "What department does she work in?")

print("\n\n" + "="*60)
print("All tests completed!")
print("="*60)
