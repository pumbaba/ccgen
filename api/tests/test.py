import requests
import json
import time
import os

# Get API URL from environment or use default
API_URL = os.environ.get("API_URL", "http://localhost:5000/generate")
HEALTH_URL = os.environ.get("HEALTH_URL", "http://localhost:5000/health")

# Test cases with different types of diffs
test_cases = [
    {
        "name": "Simple feature addition",
        "diff": """
diff --git a/app.py b/app.py
index 123456..789012 100644
--- a/app.py
+++ b/app.py
@@ -10,6 +10,10 @@ def existing_function():
     pass

+def new_feature():
+    \"\"\"Adds a new cool feature\"\"\"
+    return {"status": "success"}
+
 if __name__ == '__main__':
     app.run()
"""
    },
    {
        "name": "Bug fix",
        "diff": """
diff --git a/app.py b/app.py
index 123456..789012 100644
--- a/app.py
+++ b/app.py
@@ -15,7 +15,7 @@ def calculate_total(items):
     total = 0
     for item in items:
-        total += item.price
+        total += item.price if hasattr(item, 'price') else 0
     return total
"""
    },
    {
        "name": "Documentation update",
        "diff": """
diff --git a/README.md b/README.md
index 123456..789012 100644
--- a/README.md
+++ b/README.md
@@ -10,6 +10,10 @@ Getting Started

 Run `pip install -r requirements.txt` to install dependencies.

+## Configuration
+
+Make sure to set the `OPENAI_API_KEY` environment variable before running the application.
+
 ## Usage

 Execute `python app.py` to start the server.
"""
    },
    {
        "name": "Multiple changes (feature and fix)",
        "diff": """
diff --git a/app.py b/app.py
index 123456..789012 100644
--- a/app.py
+++ b/app.py
@@ -10,6 +10,10 @@ def existing_function():
     pass

+def new_feature():
+    \"\"\"Adds a new cool feature\"\"\"
+    return {"status": "success"}
+
 if __name__ == '__main__':
     app.run()
diff --git a/utils.py b/utils.py
index abcdef..012345 100644
--- a/utils.py
+++ b/utils.py
@@ -15,7 +15,7 @@ def parse_config(config_file):
     with open(config_file, 'r') as file:
         try:
-            return json.loads(file)
+            return json.loads(file.read())
         except json.JSONDecodeError:
            return {}
"""
    },
    {
        "name": "Breaking change",
        "diff": """
diff --git a/api.py b/api.py
index 123456..789012 100644
--- a/api.py
+++ b/api.py
@@ -10,9 +10,10 @@ class UserAPI:

-    def get_user(self, user_id):
+    def get_user(self, user_id, include_details=False):
         \"\"\"Get user information
+        Now requires a second parameter to specify if details should be included
         \"\"\"
-        return self.db.find_user(user_id)
+        return self.db.find_user(user_id, fetch_details=include_details)
"""
    }
]

def test_health():
    """Check if the API is healthy"""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"API Health: {data}")
            return True
        else:
            print(f"API Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return False

def test_commit_generation():
    """Test the commit message generation API with various test cases"""
    # First check API health
    if not test_health():
        print("API is not healthy, skipping tests.")
        return

    # Run each test case
    for idx, test_case in enumerate(test_cases):
        print(f"\n----- Test Case {idx+1}: {test_case['name']} -----")
        
        try:
            response = requests.post(
                API_URL,
                json={"diff": test_case["diff"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("Response:")
                print(json.dumps(result, indent=2))
                
                if "commits" in result:
                    print(f"\nSuccessfully generated {len(result['commits'])} commit messages:")
                    for i, commit in enumerate(result['commits']):
                        print(f"  {i+1}. {commit}")
                else:
                    print("ERROR: Response does not contain 'commits' field")
                
                # Check for warnings
                if "warning" in result:
                    print(f"\nWarnings: {result['warning']}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error during test: {e}")
            
        # Add a slight delay between tests
        time.sleep(1)

if __name__ == "__main__":
    print("Testing Commit Message Generation API...")
    test_commit_generation()
    print("\nAll tests completed.")