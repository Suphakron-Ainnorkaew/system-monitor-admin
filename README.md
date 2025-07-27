# 🚀 System Monitor Admin Dashboard

## 📊 ภาพรวม

System Monitor Admin Dashboard เป็นระบบที่สร้างขึ้นเพื่อแสดงข้อมูลสถิติและกราฟต่างๆ จากข้อมูลการทดสอบระบบที่ถูกบันทึกผ่าน API

## 🎯 ฟีเจอร์หลัก

### 📈 กราฟที่แสดง
- **กราฟแท่งแนวนอน**: แสดงการใช้ CPU Model และ GPU Model
- **กราฟวงกลม**: แสดงการกระจายของ RAM
- **กราฟเส้น**: แสดงกิจกรรมการทดสอบรายวัน
- **กราฟเปรียบเทียบ**: แสดงการเปรียบเทียบยี่ห้อ CPU vs GPU

### 📊 สถิติพื้นฐาน
- จำนวนการทดสอบทั้งหมด
- จำนวน CPU/GPU Model ที่ไม่ซ้ำ
- RAM เฉลี่ยที่ใช้

## 🚀 การใช้งาน

### 1. เข้าถึง Admin Dashboard
```
https://your-app-name.onrender.com/admin
```

### 2. API Endpoints
- `GET /` - ข้อมูลพื้นฐาน
- `POST /submit` - ส่งข้อมูลการทดสอบ
- `GET /list` - ดึงข้อมูลทั้งหมด
- `GET /admin` - Admin Dashboard
- `GET /health` - ตรวจสอบสถานะ

## 🔧 การ Deploy

### 1. บน Render.com
- ดูคู่มือใน `app/DEPLOYMENT_GUIDE.md`
- ใช้ `app/render.yaml` สำหรับ configuration

### 2. Local Development
```bash
cd app
pip install -r requirements.txt
python app.py
```

## 📁 โครงสร้างไฟล์

```
app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render configuration
├── DEPLOYMENT_GUIDE.md   # คู่มือการ deploy
├── README_ADMIN.md       # คู่มือ admin dashboard
├── QUICK_START.md        # คู่มือเริ่มต้นอย่างรวดเร็ว
└── RENDER_DEPLOYMENT_CHECKLIST.md # Checklist สำหรับ deploy
```

## 🎨 การออกแบบ

- **Responsive Design**: รองรับทุกอุปกรณ์
- **Modern UI**: ใช้ CSS Grid และ Card Design
- **Interactive Charts**: ใช้ Plotly.js
- **Color Scheme**: สีที่สวยงามและแยกแยะได้ชัดเจน

## 🔒 ความปลอดภัย

- Environment Variables สำหรับ sensitive data
- Input validation
- Error handling
- HTTPS (Render จัดให้อัตโนมัติ)

## 📱 การรองรับ

- Desktop: แสดงกราฟ 2 คอลัมน์
- Tablet/Mobile: แสดงกราฟ 1 คอลัมน์
- Auto-resize: กราฟปรับขนาดตามหน้าจอ

## 🎉 สรุป

ระบบพร้อมใช้งานใน production พร้อม:
- ✅ Admin dashboard ที่ครบถ้วน
- ✅ API endpoints ที่ทำงานได้
- ✅ MongoDB integration
- ✅ Production-ready configuration
- ✅ Complete documentation

**เริ่มต้นใช้งานได้เลย!** 🚀

---

📖 **ดูคู่มือเพิ่มเติม**:
- [คู่มือการ Deploy](app/DEPLOYMENT_GUIDE.md)
- [คู่มือ Admin Dashboard](app/README_ADMIN.md)
- [Quick Start Guide](app/QUICK_START.md)
