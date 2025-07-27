#!/usr/bin/env python3
"""
Test script for System Monitor Admin Dashboard
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"  # Change this to your server URL

def test_submit_data():
    """Test submitting sample data"""
    print("🧪 Testing data submission...")
    
    sample_data = [
        {
            "test_device_type": "CPU",
            "cpu_brand": "Intel",
            "cpu_model": "i5-13600K",
            "gpu_brand": "NVIDIA",
            "gpu_model": "RTX 4070",
            "ram_gb": 32,
            "test_details": "Gaming performance test"
        },
        {
            "test_device_type": "GPU",
            "cpu_brand": "AMD",
            "cpu_model": "Ryzen 7 7700X",
            "gpu_brand": "AMD",
            "gpu_model": "RX 7800 XT",
            "ram_gb": 16,
            "test_details": "Video editing test"
        },
        {
            "test_device_type": "CPU",
            "cpu_brand": "Intel",
            "cpu_model": "i7-13700K",
            "gpu_brand": "NVIDIA",
            "gpu_model": "RTX 4080",
            "ram_gb": 64,
            "test_details": "3D rendering test"
        },
        {
            "test_device_type": "GPU",
            "cpu_brand": "AMD",
            "cpu_model": "Ryzen 9 7900X",
            "gpu_brand": "NVIDIA",
            "gpu_model": "RTX 4090",
            "ram_gb": 32,
            "test_details": "AI training test"
        },
        {
            "test_device_type": "CPU",
            "cpu_brand": "Intel",
            "cpu_model": "i5-13600K",
            "gpu_brand": "AMD",
            "gpu_model": "RX 6700 XT",
            "ram_gb": 16,
            "test_details": "Streaming test"
        }
    ]
    
    for i, data in enumerate(sample_data, 1):
        try:
            response = requests.post(f"{BASE_URL}/submit", json=data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test {i}: {result['message']} (ID: {result['document_id']})")
            else:
                print(f"❌ Test {i}: Failed - {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Test {i}: Error - {str(e)}")
        
        time.sleep(0.5)  # Small delay between requests

def test_list_data():
    """Test listing all data"""
    print("\n📋 Testing data listing...")
    
    try:
        response = requests.get(f"{BASE_URL}/list")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data)} records")
            for i, record in enumerate(data[:3], 1):  # Show first 3 records
                print(f"   Record {i}: {record['cpu_model']} + {record['gpu_model']} ({record['ram_gb']}GB)")
        else:
            print(f"❌ Failed - {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error - {str(e)}")

def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check: {result['message']}")
        else:
            print(f"❌ Health check failed - {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Health check error - {str(e)}")

def test_admin_dashboard():
    """Test admin dashboard access"""
    print("\n📊 Testing admin dashboard...")
    
    try:
        response = requests.get(f"{BASE_URL}/admin")
        if response.status_code == 200:
            print("✅ Admin dashboard accessible")
            print(f"   Content length: {len(response.text)} characters")
            if "System Monitor Admin Dashboard" in response.text:
                print("   ✅ Dashboard title found")
            if "plotly" in response.text.lower():
                print("   ✅ Plotly charts detected")
        else:
            print(f"❌ Admin dashboard failed - {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Admin dashboard error - {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting System Monitor Admin Dashboard Tests")
    print("=" * 50)
    
    # Test health first
    test_health_check()
    
    # Test data submission
    test_submit_data()
    
    # Test data listing
    test_list_data()
    
    # Test admin dashboard
    test_admin_dashboard()
    
    print("\n" + "=" * 50)
    print("🎉 Tests completed!")
    print(f"📊 Access admin dashboard at: {BASE_URL}/admin")
    print(f"📋 View raw data at: {BASE_URL}/list")

if __name__ == "__main__":
    main() 