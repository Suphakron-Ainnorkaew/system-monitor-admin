from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
from datetime import datetime, timezone
import os
import logging
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Atlas connection (use environment variable for security)
MONGODB_URI = os.environ.get('MONGODB_URI')

if not MONGODB_URI:
    logger.error("MONGODB_URI environment variable not set!")
    # For demo purposes, we'll use a fallback
    MONGODB_URI = "mongodb://localhost:27017"
    logger.warning("Using fallback MongoDB URI - this may not work in production")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
    db = client["system-monitor"]
    collection = db["process"]
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    # For demo purposes, we'll create a mock collection
    collection = None
    logger.warning("Using mock data storage for demo purposes")

# HTML template for admin dashboard
ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor Admin Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .chart-container {
            margin-bottom: 40px;
        }
        .chart-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            text-align: center;
        }
        .chart-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .chart {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .full-width {
            grid-column: 1 / -1;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-bottom: 20px;
        }
        .refresh-btn:hover {
            background: #45a049;
        }
        .demo-notice {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .error-notice {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 System Monitor Admin Dashboard</h1>
        
        {% if demo_mode %}
        <div class="demo-notice">
            🚀 <strong>Demo Mode:</strong> ใช้ข้อมูลจำลอง (Mock Data) สำหรับการทดสอบ
        </div>
        {% endif %}
        
        {% if error_message %}
        <div class="error-notice">
            ⚠️ <strong>Warning:</strong> {{ error_message }}
        </div>
        {% endif %}
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{{ total_tests }}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ unique_cpus }}</div>
                <div class="stat-label">Unique CPU Models</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ unique_gpus }}</div>
                <div class="stat-label">Unique GPU Models</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ avg_ram }} GB</div>
                <div class="stat-label">Average RAM</div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart">
                <div class="chart-title">📈 CPU Model Usage (Horizontal Bar)</div>
                <div id="cpuChart"></div>
            </div>
            <div class="chart">
                <div class="chart-title">🎮 GPU Model Usage (Horizontal Bar)</div>
                <div id="gpuChart"></div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart">
                <div class="chart-title">🍰 RAM Distribution (Pie Chart)</div>
                <div id="ramPieChart"></div>
            </div>
            <div class="chart">
                <div class="chart-title">📊 CPU vs GPU Brand Distribution</div>
                <div id="brandChart"></div>
            </div>
        </div>

        <div class="chart-container">
            <div class="chart full-width">
                <div class="chart-title">📈 Daily Test Activity (Line Chart)</div>
                <div id="dailyChart"></div>
            </div>
        </div>
    </div>

    <script>
        // CPU Chart
        var cpuData = {{ cpu_chart_data | safe }};
        Plotly.newPlot('cpuChart', cpuData.data, cpuData.layout);

        // GPU Chart
        var gpuData = {{ gpu_chart_data | safe }};
        Plotly.newPlot('gpuChart', gpuData.data, gpuData.layout);

        // RAM Pie Chart
        var ramData = {{ ram_pie_data | safe }};
        Plotly.newPlot('ramPieChart', ramData.data, ramData.layout);

        // Brand Chart
        var brandData = {{ brand_chart_data | safe }};
        Plotly.newPlot('brandChart', brandData.data, brandData.layout);

        // Daily Activity Chart
        var dailyData = {{ daily_chart_data | safe }};
        Plotly.newPlot('dailyChart', dailyData.data, dailyData.layout);
    </script>
</body>
</html>
'''

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400

        # Validate required fields
        required = ['test_device_type', 'cpu_brand', 'cpu_model', 'gpu_brand', 'gpu_model', 'ram_gb']
        for field in required:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing field: {field}'}), 400

        # Prepare document
        doc = {
            'test_device_type': data['test_device_type'], # ประเภทอุปกรณ์ที่ใช้ทดสอบ (CPU/GPU)
            'cpu_brand': data['cpu_brand'],           # ยี่ห้อ CPU
            'cpu_model': data['cpu_model'],           # รุ่น CPU
            'gpu_brand': data['gpu_brand'],           # ยี่ห้อ GPU
            'gpu_model': data['gpu_model'],           # รุ่น GPU
            'ram_gb': data['ram_gb'],                 # จำนวนแรม (GB)
            'test_details': data.get('test_details'), # ข้อมูลอื่นๆ (optional)
            'created_at': datetime.now(timezone.utc)  # เวลาบันทึก (timezone-aware)
        }

        # Insert to MongoDB if available
        if collection:
            result = collection.insert_one(doc)
            logger.info(f"Successfully inserted document with ID: {result.inserted_id}")
            return jsonify({
                'status': 'ok', 
                'message': 'Data saved successfully.',
                'document_id': str(result.inserted_id)
            })
        else:
            # Mock response for demo
            logger.warning("MongoDB not available, using mock response")
            return jsonify({
                'status': 'ok', 
                'message': 'Data saved successfully (Demo Mode).',
                'document_id': 'demo-' + str(hash(str(doc)))
            })
        
    except Exception as e:
        logger.error(f"Error in submit endpoint: {e}")
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500

@app.route('/list', methods=['GET'])
def list_data():
    try:
        if collection:
            # ดึงข้อมูลทั้งหมด
            results = list(collection.find({}, {'_id': 0}))
            logger.info(f"Retrieved {len(results)} documents")
            return jsonify(results)
        else:
            # Mock response for demo
            logger.warning("MongoDB not available, returning empty list")
            return jsonify([])
    except Exception as e:
        logger.error(f"Error in list endpoint: {e}")
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    try:
        # ดึงข้อมูลทั้งหมดจาก MongoDB
        if collection:
            data = list(collection.find({}))
        else:
            # Mock data for demo
            logger.warning("MongoDB not available, using mock data")
            data = []
        
        if not data:
            return render_template_string(ADMIN_TEMPLATE, 
                demo_mode=True,
                error_message="No data available or MongoDB connection failed",
                total_tests=0, unique_cpus=0, unique_gpus=0, avg_ram=0,
                cpu_chart_data=json.dumps({'data': [], 'layout': {}}),
                gpu_chart_data=json.dumps({'data': [], 'layout': {}}),
                ram_pie_data=json.dumps({'data': [], 'layout': {}}),
                brand_chart_data=json.dumps({'data': [], 'layout': {}}),
                daily_chart_data=json.dumps({'data': [], 'layout': {}})
            )
        
        # สร้าง DataFrame
        df = pd.DataFrame(data)
        
        # คำนวณสถิติพื้นฐาน
        total_tests = len(df)
        unique_cpus = df['cpu_model'].nunique()
        unique_gpus = df['gpu_model'].nunique()
        avg_ram = round(df['ram_gb'].mean(), 1)
        
        # 1. CPU Model Horizontal Bar Chart
        cpu_counts = df['cpu_model'].value_counts().head(10)
        cpu_chart_data = {
            'data': [{
                'x': cpu_counts.values.tolist(),
                'y': cpu_counts.index.tolist(),
                'type': 'bar',
                'orientation': 'h',
                'marker': {'color': '#667eea'}
            }],
            'layout': {
                'title': 'CPU Model Usage',
                'xaxis': {'title': 'Number of Tests'},
                'yaxis': {'title': 'CPU Model'},
                'height': 400
            }
        }
        
        # 2. GPU Model Horizontal Bar Chart
        gpu_counts = df['gpu_model'].value_counts().head(10)
        gpu_chart_data = {
            'data': [{
                'x': gpu_counts.values.tolist(),
                'y': gpu_counts.index.tolist(),
                'type': 'bar',
                'orientation': 'h',
                'marker': {'color': '#764ba2'}
            }],
            'layout': {
                'title': 'GPU Model Usage',
                'xaxis': {'title': 'Number of Tests'},
                'yaxis': {'title': 'GPU Model'},
                'height': 400
            }
        }
        
        # 3. RAM Distribution Pie Chart
        ram_counts = df['ram_gb'].value_counts()
        ram_pie_data = {
            'data': [{
                'labels': [f'{ram} GB' for ram in ram_counts.index],
                'values': ram_counts.values.tolist(),
                'type': 'pie',
                'hole': 0.4
            }],
            'layout': {
                'title': 'RAM Distribution',
                'height': 400
            }
        }
        
        # 4. CPU vs GPU Brand Distribution
        cpu_brand_counts = df['cpu_brand'].value_counts()
        gpu_brand_counts = df['gpu_brand'].value_counts()
        
        brand_chart_data = {
            'data': [
                {
                    'x': cpu_brand_counts.index.tolist(),
                    'y': cpu_brand_counts.values.tolist(),
                    'type': 'bar',
                    'name': 'CPU Brand',
                    'marker': {'color': '#667eea'}
                },
                {
                    'x': gpu_brand_counts.index.tolist(),
                    'y': gpu_brand_counts.values.tolist(),
                    'type': 'bar',
                    'name': 'GPU Brand',
                    'marker': {'color': '#764ba2'}
                }
            ],
            'layout': {
                'title': 'CPU vs GPU Brand Distribution',
                'xaxis': {'title': 'Brand'},
                'yaxis': {'title': 'Number of Tests'},
                'barmode': 'group',
                'height': 400
            }
        }
        
        # 5. Daily Test Activity Line Chart
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        daily_counts = df['date'].value_counts().sort_index()
        
        daily_chart_data = {
            'data': [{
                'x': [str(date) for date in daily_counts.index],
                'y': daily_counts.values.tolist(),
                'type': 'scatter',
                'mode': 'lines+markers',
                'line': {'color': '#4CAF50', 'width': 3},
                'marker': {'size': 8}
            }],
            'layout': {
                'title': 'Daily Test Activity',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Number of Tests'},
                'height': 400
            }
        }
        
        return render_template_string(ADMIN_TEMPLATE,
            demo_mode=False,
            error_message=None,
            total_tests=total_tests,
            unique_cpus=unique_cpus,
            unique_gpus=unique_gpus,
            avg_ram=avg_ram,
            cpu_chart_data=json.dumps(cpu_chart_data),
            gpu_chart_data=json.dumps(gpu_chart_data),
            ram_pie_data=json.dumps(ram_pie_data),
            brand_chart_data=json.dumps(brand_chart_data),
            daily_chart_data=json.dumps(daily_chart_data)
        )
        
    except Exception as e:
        logger.error(f"Error in admin dashboard: {e}")
        return render_template_string(ADMIN_TEMPLATE,
            demo_mode=True,
            error_message=f"Error loading dashboard: {str(e)}",
            total_tests=0, unique_cpus=0, unique_gpus=0, avg_ram=0,
            cpu_chart_data=json.dumps({'data': [], 'layout': {}}),
            gpu_chart_data=json.dumps({'data': [], 'layout': {}}),
            ram_pie_data=json.dumps({'data': [], 'layout': {}}),
            brand_chart_data=json.dumps({'data': [], 'layout': {}}),
            daily_chart_data=json.dumps({'data': [], 'layout': {}})
        )

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test MongoDB connection if available
        if collection:
            client.admin.command('ping')
            return jsonify({'status': 'ok', 'message': 'Service is healthy'})
        else:
            return jsonify({'status': 'ok', 'message': 'Service is healthy (Demo Mode)'})
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'error', 'message': f'Service unhealthy: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with basic info"""
    return jsonify({
        'status': 'ok',
        'message': 'System Monitor API',
        'endpoints': {
            'submit': '/submit (POST)',
            'list': '/list (GET)',
            'admin': '/admin (GET)',
            'health': '/health (GET)'
        },
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)