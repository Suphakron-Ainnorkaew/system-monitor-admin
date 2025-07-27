# 🚀 Deployment Guide - System Monitor on Render.com

## 📋 ข้อกำหนดเบื้องต้น

### 1. MongoDB Atlas Setup
- สร้าง MongoDB Atlas cluster
- ตั้งค่า Network Access (IP Whitelist หรือ 0.0.0.0/0)
- สร้าง Database User
- รับ Connection String

### 2. Render.com Account
- สร้างบัญชี Render.com
- เชื่อมต่อ GitHub repository

## 🔧 การเตรียมไฟล์

### 1. ไฟล์ที่จำเป็น
```
app/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── render.yaml         # Render configuration
└── README.md          # Project documentation
```

### 2. ตรวจสอบ requirements.txt
```txt
flask==3.0.0
pymongo==4.6.1
dnspython==2.4.2
requests==2.32.3
plotly==5.18.0
pandas==2.1.4
gunicorn==21.2.0
```

### 3. ตรวจสอบ render.yaml
```yaml
services:
  - type: web
    name: system-monitor-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: MONGODB_URI
        sync: false
      - key: PORT
        value: 5000
    healthCheckPath: /health
```

## 🚀 ขั้นตอนการ Deploy

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. สร้าง Service บน Render.com

1. **เข้าไปที่ Render Dashboard**
   - ไปที่ https://dashboard.render.com
   - คลิก "New +" → "Web Service"

2. **เชื่อมต่อ Repository**
   - เลือก GitHub repository
   - เลือก branch (main)

3. **ตั้งค่า Service**
   - **Name**: system-monitor-api
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **ตั้งค่า Environment Variables**
   - **MONGODB_URI**: `mongodb+srv://username:password@cluster.mongodb.net/system-monitor?retryWrites=true&w=majority`
   - **PORT**: `5000` (Render จะตั้งให้อัตโนมัติ)

### 3. Deploy
- คลิก "Create Web Service"
- รอการ build และ deploy (ประมาณ 2-5 นาที)

## 🔍 การตรวจสอบ

### 1. Health Check
```
https://your-app-name.onrender.com/health
```
ควรได้ response:
```json
{
  "status": "ok",
  "message": "Service is healthy"
}
```

### 2. Admin Dashboard
```
https://your-app-name.onrender.com/admin
```

### 3. API Endpoints
```
https://your-app-name.onrender.com/          # Root info
https://your-app-name.onrender.com/submit    # POST data
https://your-app-name.onrender.com/list      # GET data
https://your-app-name.onrender.com/admin     # Dashboard
https://your-app-name.onrender.com/health    # Health check
```

## 🛠️ การแก้ไขปัญหา

### 1. Build Failed
**ปัญหา**: Build ไม่สำเร็จ
**แก้ไข**:
- ตรวจสอบ requirements.txt
- ตรวจสอบ Python version compatibility
- ดู build logs ใน Render dashboard

### 2. MongoDB Connection Failed
**ปัญหา**: ไม่สามารถเชื่อมต่อ MongoDB ได้
**แก้ไข**:
- ตรวจสอบ MONGODB_URI
- ตรวจสอบ Network Access ใน MongoDB Atlas
- ตรวจสอบ Database User permissions

### 3. App Crashes
**ปัญหา**: App ทำงานแล้วหยุด
**แก้ไข**:
- ตรวจสอบ logs ใน Render dashboard
- ตรวจสอบ start command
- ตรวจสอบ port configuration

### 4. 404 Errors
**ปัญหา**: ไม่พบหน้าเว็บ
**แก้ไข**:
- ตรวจสอบ route definitions
- ตรวจสอบ static file paths
- ตรวจสอบ render.yaml configuration

## 📊 การ Monitor

### 1. Render Dashboard
- **Logs**: ดู application logs
- **Metrics**: CPU, Memory usage
- **Deployments**: ประวัติการ deploy

### 2. MongoDB Atlas
- **Database**: ดูข้อมูลที่บันทึก
- **Performance**: ตรวจสอบ query performance
- **Connections**: ตรวจสอบการเชื่อมต่อ

## 🔒 Security

### 1. Environment Variables
- อย่า commit MONGODB_URI ใน code
- ใช้ Render environment variables
- ตรวจสอบ .gitignore

### 2. MongoDB Security
- ใช้ strong password
- ตั้งค่า IP whitelist
- ใช้ SSL connection

### 3. API Security
- ตรวจสอบ input validation
- ใช้ HTTPS (Render จัดให้อัตโนมัติ)
- ตั้งค่า CORS ถ้าจำเป็น

## 📈 การ Scale

### 1. Auto-scaling
- Render รองรับ auto-scaling
- ตั้งค่าใน service configuration

### 2. Database Scaling
- MongoDB Atlas รองรับ scaling
- เปลี่ยน plan ตามความต้องการ

## 🎯 การทดสอบหลัง Deploy

### 1. ทดสอบ API
```bash
curl -X POST https://your-app-name.onrender.com/submit \
  -H "Content-Type: application/json" \
  -d '{
    "test_device_type": "CPU",
    "cpu_brand": "Intel",
    "cpu_model": "i5-13600K",
    "gpu_brand": "NVIDIA",
    "gpu_model": "RTX 4070",
    "ram_gb": 32,
    "test_details": "Test deployment"
  }'
```

### 2. ทดสอบ Dashboard
- เปิด https://your-app-name.onrender.com/admin
- ตรวจสอบกราฟแสดงผล
- ทดสอบ refresh data

## 🎉 สรุป

หลังจาก deploy สำเร็จ คุณจะได้:
- ✅ Web service ที่ทำงานบน Render.com
- ✅ MongoDB Atlas database
- ✅ Admin dashboard พร้อมกราฟ
- ✅ API endpoints สำหรับรับส่งข้อมูล
- ✅ Health check และ monitoring

**URL ที่ได้**: `https://your-app-name.onrender.com`

ระบบพร้อมใช้งานใน production! 🚀 