# System Monitor Admin Dashboard

## 📊 ภาพรวม

หน้า Admin Dashboard ถูกออกแบบมาเพื่อแสดงข้อมูลสถิติและกราฟต่างๆ จากข้อมูลการทดสอบระบบที่ถูกบันทึกผ่าน API

## 🚀 การใช้งาน

### 1. เข้าถึงหน้า Admin
```
http://your-server:port/admin
```

### 2. หน้าจอหลัก
หน้า Admin จะแสดง:
- **สถิติพื้นฐาน**: จำนวนการทดสอบทั้งหมด, CPU/GPU ที่ไม่ซ้ำ, RAM เฉลี่ย
- **กราฟแท่งแนวนอน**: แสดงการใช้ CPU Model และ GPU Model
- **กราฟวงกลม**: แสดงการกระจายของ RAM
- **กราฟแท่งเปรียบเทียบ**: แสดงการเปรียบเทียบยี่ห้อ CPU vs GPU
- **กราฟเส้น**: แสดงกิจกรรมการทดสอบรายวัน

## 📈 กราฟที่แสดง

### 1. CPU Model Usage (Horizontal Bar Chart)
- แสดง CPU Model ที่ใช้บ่อยที่สุด 10 อันดับแรก
- แกน Y: ชื่อ CPU Model
- แกน X: จำนวนการทดสอบ
- สี: น้ำเงิน (#667eea)

### 2. GPU Model Usage (Horizontal Bar Chart)
- แสดง GPU Model ที่ใช้บ่อยที่สุด 10 อันดับแรก
- แกน Y: ชื่อ GPU Model
- แกน X: จำนวนการทดสอบ
- สี: ม่วง (#764ba2)

### 3. RAM Distribution (Pie Chart)
- แสดงการกระจายของ RAM ที่ใช้ในการทดสอบ
- แสดงเป็นเปอร์เซ็นต์ของแต่ละขนาด RAM
- ใช้ Donut Chart (มีรูตรงกลาง)

### 4. CPU vs GPU Brand Distribution
- เปรียบเทียบยี่ห้อ CPU และ GPU
- แสดงเป็น Grouped Bar Chart
- สีน้ำเงินสำหรับ CPU, สีม่วงสำหรับ GPU

### 5. Daily Test Activity (Line Chart)
- แสดงจำนวนการทดสอบในแต่ละวัน
- ใช้ Line Chart พร้อมจุดข้อมูล
- สีเขียว (#4CAF50)

## 🔧 การติดตั้ง

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. ตั้งค่า Environment Variables
```bash
export MONGODB_URI="your-mongodb-connection-string"
```

### 3. รัน Server
```bash
python app.py
```

## 🧪 การทดสอบ

### 1. ทดสอบ API
```bash
python test_api.py
```

### 2. ทดสอบ Admin Dashboard
```bash
python test_admin.py
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

## 🎨 การปรับแต่ง

### 1. เปลี่ยนสีกราฟ
แก้ไขใน `app.py` ในส่วนของ chart configuration:
```python
'marker': {'color': '#667eea'}  # เปลี่ยนสีตรงนี้
```

### 2. เปลี่ยนจำนวนข้อมูลที่แสดง
แก้ไขในส่วน `.head(10)` เพื่อเปลี่ยนจำนวนรายการที่แสดง

### 3. เพิ่มกราฟใหม่
เพิ่ม chart configuration ใหม่ในฟังก์ชัน `admin_dashboard()`

## 🔒 ความปลอดภัย

- หน้า Admin ไม่มีระบบ Authentication (ควรเพิ่มในอนาคต)
- ใช้ HTTPS ใน production
- ตั้งค่า CORS ตามความเหมาะสม

## 📱 Responsive Design

หน้า Admin รองรับการแสดงผลบนอุปกรณ์ต่างๆ:
- Desktop: แสดงกราฟ 2 คอลัมน์
- Tablet/Mobile: แสดงกราฟ 1 คอลัมน์

## 🐛 การแก้ไขปัญหา

### 1. กราฟไม่แสดง
- ตรวจสอบการเชื่อมต่อ MongoDB
- ตรวจสอบว่ามีข้อมูลในฐานข้อมูล
- ดู Console ใน Browser สำหรับ JavaScript errors

### 2. ข้อมูลไม่อัพเดท
- กดปุ่ม "Refresh Data" เพื่อโหลดข้อมูลใหม่
- ตรวจสอบว่า API `/submit` ทำงานปกติ

### 3. MongoDB Connection Error
- ตรวจสอบ MONGODB_URI environment variable
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ตรวจสอบ IP Whitelist ใน MongoDB Atlas

## 📞 การสนับสนุน

หากมีปัญหาหรือต้องการความช่วยเหลือ:
1. ตรวจสอบ log files
2. ทดสอบ API endpoints
3. ตรวจสอบการเชื่อมต่อฐานข้อมูล 