#!/usr/bin/env python3
"""
Simple test script for Admin Dashboard (without MongoDB)
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"

def test_endpoints():
    """Test all endpoints"""
    print("🧪 Testing Admin Dashboard Endpoints")
    print("=" * 50)
    
    endpoints = [
        ("/health", "Health Check"),
        ("/list", "List Data"),
        ("/admin", "Admin Dashboard")
    ]
    
    for endpoint, name in endpoints:
        try:
            print(f"\n📋 Testing {name} ({endpoint})...")
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {name}: Success (Status: {response.status_code})")
                
                if endpoint == "/admin":
                    content = response.text
                    if "System Monitor Admin Dashboard" in content:
                        print("   ✅ Dashboard title found")
                    if "plotly" in content.lower():
                        print("   ✅ Plotly charts detected")
                    if "cpuChart" in content:
                        print("   ✅ CPU chart container found")
                    if "gpuChart" in content:
                        print("   ✅ GPU chart container found")
                    print(f"   📄 Content length: {len(content)} characters")
                
                elif endpoint == "/list":
                    try:
                        data = response.json()
                        print(f"   📊 Retrieved {len(data)} records")
                    except:
                        print("   ⚠️  Response is not JSON")
                
                elif endpoint == "/health":
                    try:
                        data = response.json()
                        print(f"   💚 Health status: {data.get('message', 'Unknown')}")
                    except:
                        print("   ⚠️  Response is not JSON")
                        
            else:
                print(f"❌ {name}: Failed (Status: {response.status_code})")
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Connection refused (Server not running)")
        except requests.exceptions.Timeout:
            print(f"❌ {name}: Timeout")
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")

def test_sample_data_submission():
    """Test submitting sample data"""
    print("\n📤 Testing Data Submission...")
    
    sample_data = {
        "test_device_type": "CPU",
        "cpu_brand": "Intel",
        "cpu_model": "i5-13600K",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 4070",
        "ram_gb": 32,
        "test_details": "Test submission"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/submit", json=sample_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Data submission: {result.get('message', 'Success')}")
            print(f"   📝 Document ID: {result.get('document_id', 'N/A')}")
        else:
            print(f"❌ Data submission failed (Status: {response.status_code})")
            print(f"   Response: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Data submission: Connection refused (Server not running)")
    except requests.exceptions.Timeout:
        print("❌ Data submission: Timeout")
    except Exception as e:
        print(f"❌ Data submission: Error - {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting Simple Admin Dashboard Tests")
    print("=" * 50)
    
    # Test all endpoints
    test_endpoints()
    
    # Test data submission
    test_sample_data_submission()
    
    print("\n" + "=" * 50)
    print("🎉 Tests completed!")
    print(f"📊 Access admin dashboard at: {BASE_URL}/admin")
    print(f"📋 View raw data at: {BASE_URL}/list")
    print(f"🏥 Health check at: {BASE_URL}/health")

if __name__ == "__main__":
    main() 