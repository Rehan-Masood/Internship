#!/usr/bin/env python
"""Test the two problems in the running application"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("="*60)
print("TESTING THE TWO PROBLEMS")
print("="*60)

# ============================================================
# PROBLEM 2: SWAGGER ENDPOINT
# ============================================================
print("\n[SWAGGER TEST]")
print("-"*60)

# Test 1: Check /api-docs.json
print("[TEST S1] Checking /api-docs.json...")
try:
    r = requests.get(f"{BASE_URL}/api-docs.json", timeout=5)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        print("  ✓ Endpoint exists")
        try:
            data = r.json()
            print(f"  ✓ Valid JSON")
            if "swagger" in data or "openapi" in data:
                print("  ✓ Valid Swagger/OpenAPI document")
            else:
                print("  ✗ NOT a Swagger/OpenAPI document")
        except:
            print("  ✗ Invalid JSON")
    else:
        print(f"  ✗ Not found (404)")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Check /apispec_1.json (Flasgger default)
print("\n[TEST S2] Checking /apispec_1.json (Flasgger default)...")
try:
    r = requests.get(f"{BASE_URL}/apispec_1.json", timeout=5)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        print("  ✓ Endpoint exists")
        try:
            data = r.json()
            print(f"  ✓ Valid JSON")
            if "swagger" in data or "openapi" in data:
                print("  ✓ Valid Swagger/OpenAPI document")
                print(f"  ✓ CORRECT ENDPOINT: /apispec_1.json")
            else:
                print("  ✗ NOT a Swagger/OpenAPI document")
        except:
            print("  ✗ Invalid JSON")
    else:
        print(f"  ✗ Not found")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 3: Check swagger.html URL
print("\n[TEST S3] Checking swagger.html configuration...")
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
                print("  ✓ CORRECT (matches Flasgger endpoint)")
            else:
                print(f"  ✗ WRONG (should be /apispec_1.json)")
except Exception as e:
    print(f"  Error: {e}")

# ============================================================
# PROBLEM 1: LOGOUT - Check if backend supports logout
# ============================================================
print("\n\n[LOGOUT TEST]")
print("-"*60)

# Test login first
print("[TEST L1] Testing login...")
try:
    login_data = {
        "email": "rehan@taskflow.com",
        "password": "user123"
    }
    r = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=5)
    print(f"  Login status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        token = data.get('data', {}).get('access_token')
        if token:
            print(f"  ✓ JWT received: {token[:30]}...")
            
            # Test protected endpoint
            print("\n[TEST L2] Testing protected endpoint with JWT...")
            headers = {'Authorization': f'Bearer {token}'}
            r = requests.get(f"{BASE_URL}/api/auth/me", headers=headers, timeout=5)
            print(f"  Status: {r.status_code}")
            if r.status_code == 200:
                print("  ✓ Protected endpoint works with valid JWT")
            else:
                print(f"  ✗ Protected endpoint failed: {r.status_code}")
            
            # Test without JWT
            print("\n[TEST L3] Testing protected endpoint without JWT...")
            r = requests.get(f"{BASE_URL}/api/auth/me", timeout=5)
            print(f"  Status: {r.status_code}")
            if r.status_code == 401:
                print("  ✓ Correctly rejects request without JWT")
            else:
                print(f"  ✗ Should reject without JWT")
        else:
            print("  ✗ No token in response")
    else:
        print(f"  ✗ Login failed: {r.status_code}")
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "="*60)
print("TESTS COMPLETE")
print("="*60)
