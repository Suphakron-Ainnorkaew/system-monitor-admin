#!/usr/bin/env python3
"""
Add sample data for testing admin dashboard
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"

# Sample data for testing
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
    },
    {
        "test_device_type": "CPU",
        "cpu_brand": "Intel",
        "cpu_model": "i9-13900K",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 4090",
        "ram_gb": 64,
        "test_details": "Professional workstation"
    },
    {
        "test_device_type": "GPU",
        "cpu_brand": "AMD",
        "cpu_model": "Ryzen 5 7600X",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 4060",
        "ram_gb": 16,
        "test_details": "Budget gaming build"
    },
    {
        "test_device_type": "CPU",
        "cpu_brand": "Intel",
        "cpu_model": "i5-13600K",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 4070",
        "ram_gb": 32,
        "test_details": "Another gaming test"
    },
    {
        "test_device_type": "GPU",
        "cpu_brand": "AMD",
        "cpu_model": "Ryzen 7 7700X",
        "gpu_brand": "AMD",
        "gpu_model": "RX 7800 XT",
        "ram_gb": 32,
        "test_details": "AMD build test"
    },
    {
        "test_device_type": "CPU",
        "cpu_brand": "Intel",
        "cpu_model": "i7-13700K",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 4080",
        "ram_gb": 32,
        "test_details": "High-end gaming"
    },
    {
        "test_device_type": "GPU",
        "cpu_brand": "AMD",
        "cpu_model": "Ryzen 9 7900X",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 4090",
        "ram_gb": 64,
        "test_details": "Ultimate build"
    },
    {
        "test_device_type": "CPU",
        "cpu_brand": "Intel",
        "cpu_model": "i5-13600K",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 4070",
        "ram_gb": 16,
        "test_details": "Budget build"
    }
]

def add_sample_data():
    """Add sample data to the system"""
    print("📤 Adding sample data for admin dashboard testing...")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for i, data in enumerate(sample_data, 1):
        try:
            print(f"📝 Adding record {i}/{len(sample_data)}: {data['cpu_model']} + {data['gpu_model']}")
            
            response = requests.post(f"{BASE_URL}/submit", json=data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result['message']}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            error_count += 1
        
        # Small delay between requests
        time.sleep(0.3)
    
    print("\n" + "=" * 60)
    print(f"🎉 Data addition completed!")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {error_count}")
    print(f"📊 Total records: {success_count + error_count}")
    
    if success_count > 0:
        print(f"\n🌐 Access admin dashboard at: {BASE_URL}/admin")
        print(f"📋 View raw data at: {BASE_URL}/list")

def check_current_data():
    """Check current data in the system"""
    print("📋 Checking current data...")
    
    try:
        response = requests.get(f"{BASE_URL}/list", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Current records: {len(data)}")
            
            if data:
                print("📝 Sample records:")
                for i, record in enumerate(data[:3], 1):
                    print(f"   {i}. {record['cpu_model']} + {record['gpu_model']} ({record['ram_gb']}GB)")
        else:
            print(f"❌ Failed to get data: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking data: {str(e)}")

def main():
    """Main function"""
    print("🚀 System Monitor - Sample Data Generator")
    print("=" * 60)
    
    # Check current data first
    check_current_data()
    
    print("\n" + "=" * 60)
    
    # Add sample data
    add_sample_data()

if __name__ == "__main__":
    main() 