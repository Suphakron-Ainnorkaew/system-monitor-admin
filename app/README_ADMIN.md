# 🚀 System Monitor Admin Dashboard

## 📊 ภาพรวม

หน้า Admin Dashboard ที่สร้างขึ้นมาเพื่อแสดงข้อมูลสถิติและกราฟต่างๆ จากข้อมูลการทดสอบระบบที่ถูกบันทึกผ่าน API

## 🎯 ฟีเจอร์หลัก

### 1. 📈 กราฟแท่งแนวนอน (Horizontal Bar Charts)
- **CPU Model Usage**: แสดง CPU Model ที่ใช้บ่อยที่สุด 10 อันดับแรก
- **GPU Model Usage**: แสดง GPU Model ที่ใช้บ่อยที่สุด 10 อันดับแรก
- แกน Y: ชื่อ Model
- แกน X: จำนวนการทดสอบ

### 2. 🍰 กราฟวงกลม (Pie Chart)
- **RAM Distribution**: แสดงการกระจายของ RAM ที่ใช้ในการทดสอบ
- ใช้ Donut Chart (มีรูตรงกลาง)
- แสดงเป็นเปอร์เซ็นต์ของแต่ละขนาด RAM

### 3. 📊 กราฟแท่งเปรียบเทียบ (Grouped Bar Chart)
- **CPU vs GPU Brand Distribution**: เปรียบเทียบยี่ห้อ CPU และ GPU
- แสดงเป็น Grouped Bar Chart
- สีน้ำเงินสำหรับ CPU, สีม่วงสำหรับ GPU

### 4. 📈 กราฟเส้น (Line Chart)
- **Daily Test Activity**: แสดงจำนวนการทดสอบในแต่ละวัน
- ใช้ Line Chart พร้อมจุดข้อมูล
- สีเขียว (#4CAF50)

### 5. 📊 สถิติพื้นฐาน
- **Total Tests**: จำนวนการทดสอบทั้งหมด
- **Unique CPU Models**: จำนวน CPU Model ที่ไม่ซ้ำ
- **Unique GPU Models**: จำนวน GPU Model ที่ไม่ซ้ำ
- **Average RAM**: RAM เฉลี่ยที่ใช้

## 🚀 การใช้งาน

### 1. รัน Demo Server
```bash
cd app
python app_demo.py
```

### 2. เข้าถึงหน้า Admin
เปิดเบราว์เซอร์ไปที่: `http://localhost:5000/admin`

### 3. เพิ่มข้อมูลตัวอย่าง
```bash
python add_sample_data.py
```

### 4. ทดสอบ API
```bash
python test_admin_simple.py
```

## 📋 API Endpoints

### POST /submit
ส่งข้อมูลการทดสอบระบบ
```json
{
    "test_device_type": "CPU",
    "cpu_brand": "Intel",
    "cpu_model": "i5-13600K",
    "gpu_brand": "NVIDIA",
    "gpu_model": "RTX 4070",
    "ram_gb": 32,
    "test_details": "Gaming performance test"
}
```

### GET /list
ดึงข้อมูลการทดสอบทั้งหมด

### GET /admin
เข้าถึงหน้า Admin Dashboard

### GET /health
ตรวจสอบสถานะของระบบ

## 🎨 การออกแบบ

### สีที่ใช้
- **CPU Charts**: น้ำเงิน (#667eea)
- **GPU Charts**: ม่วง (#764ba2)
- **Line Chart**: เขียว (#4CAF50)
- **Background**: สีเทาอ่อน (#f5f5f5)

### Layout
- **Responsive Design**: รองรับการแสดงผลบนอุปกรณ์ต่างๆ
- **Grid Layout**: ใช้ CSS Grid สำหรับจัดเรียงกราฟ
- **Card Design**: แต่ละกราฟอยู่ใน card ที่มี shadow

## 📱 Responsive Features

- **Desktop**: แสดงกราฟ 2 คอลัมน์
- **Tablet/Mobile**: แสดงกราฟ 1 คอลัมน์
- **Auto-resize**: กราฟปรับขนาดตามหน้าจอ

## 🔧 การปรับแต่ง

### 1. เปลี่ยนสีกราฟ
แก้ไขใน `app_demo.py` ในส่วนของ chart configuration:
```python
'marker': {'color': '#667eea'}  # เปลี่ยนสีตรงนี้
```

### 2. เปลี่ยนจำนวนข้อมูลที่แสดง
แก้ไขในส่วน `.head(10)` เพื่อเปลี่ยนจำนวนรายการที่แสดง

### 3. เพิ่มกราฟใหม่
เพิ่ม chart configuration ใหม่ในฟังก์ชัน `admin_dashboard()`

## 📊 ข้อมูลตัวอย่าง

ระบบมาพร้อมกับข้อมูลตัวอย่างที่หลากหลาย:
- **CPU Models**: i5-13600K, i7-13700K, i9-13900K, Ryzen 5/7/9 series
- **GPU Models**: RTX 4060/4070/4080/4090, RX 6700 XT/7800 XT
- **RAM Sizes**: 16GB, 32GB, 64GB
- **Brands**: Intel, AMD, NVIDIA

## 🎯 กราฟที่แสดงผล

### 1. CPU Model Usage
- แสดง CPU ที่ใช้บ่อยที่สุด
- i5-13600K จะมีความยาวมากที่สุด (4 ครั้ง)
- i7-13700K และ Ryzen 7 7700X (2 ครั้ง)

### 2. GPU Model Usage
- แสดง GPU ที่ใช้บ่อยที่สุด
- RTX 4070 และ RTX 4090 จะมีความยาวมากที่สุด
- RX 7800 XT (2 ครั้ง)

### 3. RAM Distribution
- 32GB: มากที่สุด
- 16GB: รองลงมา
- 64GB: น้อยที่สุด

### 4. Brand Distribution
- Intel CPU: มากกว่า AMD
- NVIDIA GPU: มากกว่า AMD

### 5. Daily Activity
- แสดงกิจกรรมการทดสอบในแต่ละวัน
- ข้อมูลจะอัพเดทตามเวลาจริง

## 🔄 การอัพเดทข้อมูล

- กดปุ่ม "🔄 Refresh Data" เพื่อโหลดข้อมูลใหม่
- ข้อมูลจะอัพเดทแบบ real-time เมื่อมีการเพิ่มข้อมูลใหม่

## 🎉 สรุป

หน้า Admin Dashboard นี้ให้มุมมองที่ครบถ้วนของข้อมูลการทดสอบระบบ:
- **สถิติพื้นฐาน** ที่เข้าใจง่าย
- **กราฟแท่งแนวนอน** สำหรับเปรียบเทียบ CPU/GPU
- **กราฟวงกลม** สำหรับดูการกระจาย RAM
- **กราฟเปรียบเทียบ** สำหรับดูยี่ห้อ
- **กราฟเส้น** สำหรับดูแนวโน้ม

ระบบพร้อมใช้งานและสามารถปรับแต่งได้ตามความต้องการ! 🚀 