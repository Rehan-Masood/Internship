#!/usr/bin/env python
"""Test after fixes"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("="*60)
print("TESTING AFTER FIXES")
print("="*60)

# ============================================================
# TEST SWAGGER FIX
# ============================================================
print("\n[SWAGGER FIX VERIFICATION]")
print("-"*60)

# Check swagger.html URL
print("[TEST S1] Checking swagger.html configuration...")
try:
    r = requests.get(f"{BASE_URL}/api/docs", timeout=5)
    if "url:" in r.text:
        # Extract URL from JavaScript
        import re
        match = re.search(r'url:\s*["\']([^"\']+)["\']', r.text)
        if match:
            configured_url = match.group(1)
            print(f"  Configured URL: {configured_url}")
            if configured_url == "/apispec_1.json":
                print("  ✓ FIXED (now uses /apispec_1.json)")
                
                # Verify the endpoint exists
                r2 = requests.get(f"{BASE_URL}/apispec_1.json", timeout=5)
                print(f"\n[TEST S2] Swagger endpoint response: {r2.status_code}")
                if r2.status_code == 200:
                    print("  ✓ Endpoint exists and returns HTTP 200")
                    try:
                        data = r2.json()
                        if "swagger" in data or "openapi" in data:
                            print("  ✓ Valid Swagger/OpenAPI document")
                    except:
                        print("  ✗ Response is not valid JSON")
            else:
                print(f"  ✗ STILL WRONG (uses {configured_url})")
except Exception as e:
    print(f"  Error: {e}")

# ============================================================
# TEST LOGOUT
# ============================================================
print("\n\n[LOGOUT VERIFICATION]")
print("-"*60)

# Get list of existing users from the database
print("[TEST L1] Finding existing users...")

# Try admin user first
for email, password in [
    ("admin@taskflow.com", "admin123"),
    ("rehan@taskflow.com", "user123"),
    ("ali@taskflow.com", "user123"),
]:
    print(f"\n  Trying {email}...")
    try:
        login_data = {
            "email": email,
            "password": password
        }
        r = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=5)
        print(f"    Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            token = data.get('data', {}).get('access_token')
            if token:
                print(f"    ✓ Login successful!")
                print(f"    ✓ JWT received: {token[:30]}...")
                
                # Test protected endpoint
                print("\n  [TEST L2] Testing protected endpoint with JWT...")
                headers = {'Authorization': f'Bearer {token}'}
                r = requests.get(f"{BASE_URL}/api/auth/me", headers=headers, timeout=5)
                print(f"    Status: {r.status_code}")
                if r.status_code == 200:
                    print("    ✓ Protected endpoint works with valid JWT")
                    
                    # Verify logout URL works for frontend
                    print("\n  [TEST L3] Verifying logout frontend URL...")
                    r = requests.get(f"{BASE_URL}/", timeout=5)  # Get login page
                    if r.status_code == 200:
                        print("    ✓ Frontend loaded successfully")
                        # Check if app.logout method exists in JavaScript
                        if "async logout()" in r.text or "logout()" in r.text:
                            print("    ✓ Found logout method in JavaScript")
                    
                    break
                else:
                    print(f"    ✗ Protected endpoint failed: {r.status_code}")
            else:
                print("    ✗ No token in response")
        else:
            print(f"    ✗ Login failed: {r.status_code}")
    except Exception as e:
        print(f"    Error: {e}")

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
