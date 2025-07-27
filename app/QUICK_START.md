# 🚀 Quick Start Guide - System Monitor Admin Dashboard

## ⚡ การเริ่มต้นใช้งานอย่างรวดเร็ว

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. รัน Demo Server
```bash
python app_demo.py
```

### 3. เพิ่มข้อมูลตัวอย่าง
```bash
python add_sample_data.py
```

### 4. เข้าถึงหน้า Admin
เปิดเบราว์เซอร์ไปที่: **http://localhost:5000/admin**

## 📊 กราฟที่คุณจะเห็น

### 🎯 กราฟแท่งแนวนอน (ตามที่ต้องการ)
- **CPU Model Usage**: แสดง i5-13600K (4 ครั้ง), i7-13700K (2 ครั้ง), etc.
- **GPU Model Usage**: แสดง RTX 4070, RTX 4090, RX 7800 XT, etc.

### 🍰 กราฟวงกลม (ตามที่อนุญาต)
- **RAM Distribution**: แสดงการกระจายของ 16GB, 32GB, 64GB

### 📈 กราฟเส้น (ตามที่อนุญาต)
- **Daily Test Activity**: แสดงกิจกรรมการทดสอบรายวัน

### 📊 กราฟเปรียบเทียบ (ตามที่อนุญาต)
- **CPU vs GPU Brand**: เปรียบเทียบ Intel vs AMD, NVIDIA vs AMD

## 🎯 ข้อมูลตัวอย่างที่ใช้

### CPU Models (แสดงในกราฟแท่งแนวนอน)
- i5-13600K: 4 ครั้ง (ความยาวมากที่สุด)
- i7-13700K: 2 ครั้ง
- i9-13900K: 1 ครั้ง
- Ryzen 7 7700X: 2 ครั้ง
- Ryzen 9 7900X: 2 ครั้ง
- Ryzen 5 7600X: 1 ครั้ง

### GPU Models (แสดงในกราฟแท่งแนวนอน)
- RTX 4070: 3 ครั้ง
- RTX 4090: 3 ครั้ง
- RTX 4080: 2 ครั้ง
- RX 7800 XT: 2 ครั้ง
- RTX 4060: 1 ครั้ง
- RX 6700 XT: 1 ครั้ง

### RAM Distribution (แสดงในกราฟวงกลม)
- 32GB: 6 ครั้ง (มากที่สุด)
- 16GB: 4 ครั้ง
- 64GB: 3 ครั้ง

## 🔧 การทดสอบ

### ทดสอบ API
```bash
python test_admin_simple.py
```

### ทดสอบการเพิ่มข้อมูล
```bash
python add_sample_data.py
```

## 📱 การใช้งาน

1. **ดูสถิติพื้นฐาน**: ดูที่ส่วนบนของหน้า
2. **ดูกราฟแท่งแนวนอน**: CPU และ GPU usage
3. **ดูกราฟวงกลม**: RAM distribution
4. **ดูกราฟเปรียบเทียบ**: Brand comparison
5. **ดูกราฟเส้น**: Daily activity
6. **Refresh**: กดปุ่ม "🔄 Refresh Data" เพื่ออัพเดท

## 🎨 สีที่ใช้

- **CPU Charts**: น้ำเงิน (#667eea)
- **GPU Charts**: ม่วง (#764ba2)
- **Line Chart**: เขียว (#4CAF50)
- **Background**: เทาอ่อน (#f5f5f5)

## 📋 API Endpoints

- **POST /submit**: ส่งข้อมูลการทดสอบ
- **GET /list**: ดึงข้อมูลทั้งหมด
- **GET /admin**: หน้า Admin Dashboard
- **GET /health**: ตรวจสอบสถานะ

## 🎉 สรุป

ระบบพร้อมใช้งานแล้ว! คุณจะเห็น:
- ✅ กราฟแท่งแนวนอนสำหรับ CPU/GPU (ตามที่ต้องการ)
- ✅ กราฟวงกลมสำหรับ RAM (ตามที่อนุญาต)
- ✅ กราฟเส้นสำหรับกิจกรรมรายวัน (ตามที่อนุญาต)
- ✅ กราฟเปรียบเทียบยี่ห้อ (ตามที่อนุญาต)
- ✅ สถิติพื้นฐานที่เข้าใจง่าย

**เริ่มต้นใช้งานได้เลยที่: http://localhost:5000/admin** 🚀 