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
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            position: relative;
        }
        
        /* Animated background elements */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><radialGradient id="g"><stop offset="20%" stop-color="%23ffffff" stop-opacity="0.1"/><stop offset="50%" stop-color="%23ffffff" stop-opacity="0.05"/><stop offset="100%" stop-color="%23ffffff" stop-opacity="0"/></radialGradient></defs><circle cx="20" cy="20" r="10" fill="url(%23g)"/><circle cx="80" cy="80" r="15" fill="url(%23g)"/></svg>') repeat;
            animation: float 20s ease-in-out infinite;
            pointer-events: none;
            z-index: -1;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            padding: 40px;
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
            background-size: 300% 300%;
            animation: gradientShift 3s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            position: relative;
        }
        
        .header .subtitle {
            color: #6b7280;
            font-size: 1.1rem;
            font-weight: 500;
        }
        
        .refresh-btn {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 16px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .refresh-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        
        .refresh-btn:hover::before {
            left: 100%;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px -5px rgba(16, 185, 129, 0.4);
        }
        
        .refresh-btn i {
            margin-right: 8px;
            transition: transform 0.3s ease;
        }
        
        .refresh-btn:hover i {
            transform: rotate(180deg);
        }
        
        .demo-notice, .error-notice {
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 600;
            position: relative;
            overflow: hidden;
        }
        
        .demo-notice {
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            color: #92400e;
            border: 2px solid #f59e0b;
        }
        
        .error-notice {
            background: linear-gradient(135deg, #fee2e2, #fecaca);
            color: #991b1b;
            border: 2px solid #ef4444;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 32px;
            border-radius: 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            transform: rotate(0deg);
            transition: transform 0.6s ease;
        }
        
        .stat-card:hover::before {
            transform: rotate(180deg);
        }
        
        .stat-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 50px -12px rgba(102, 126, 234, 0.4);
        }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 16px;
            opacity: 0.9;
        }
        
        .stat-number {
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }
        
        .stat-label {
            font-size: 1rem;
            opacity: 0.9;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }
        
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 32px;
            margin-bottom: 40px;
        }
        
        .chart {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .chart::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 20px 20px 0 0;
        }
        
        .chart:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.15);
        }
        
        .chart-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 24px;
            text-align: center;
            position: relative;
            padding-bottom: 12px;
        }
        
        .chart-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 2px;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
            color: #6b7280;
        }
        
        .loading i {
            font-size: 2rem;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Responsive Design */
        @media (max-width: 1200px) {
            .chart-grid {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .container {
                padding: 20px;
                border-radius: 16px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 16px;
            }
            
            .stat-card {
                padding: 24px;
            }
            
            .chart {
                padding: 20px;
            }
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(243, 244, 246, 0.5);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a67d8, #6b46c1);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> System Monitor</h1>
            <p class="subtitle">Real-time Hardware Analytics Dashboard</p>
        </div>
        
        {% if demo_mode %}
        <div class="demo-notice">
            <i class="fas fa-rocket"></i> <strong>Demo Mode:</strong> ใช้ข้อมูลจำลอง (Mock Data) สำหรับการทดสอบ
        </div>
        {% endif %}
        
        {% if error_message %}
        <div class="error-notice">
            <i class="fas fa-exclamation-triangle"></i> <strong>Warning:</strong> {{ error_message }}
        </div>
        {% endif %}
        
        <button class="refresh-btn" onclick="location.reload()">
            <i class="fas fa-sync-alt"></i> Refresh Data
        </button>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-vial"></i></div>
                <div class="stat-number">{{ total_tests }}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-microchip"></i></div>
                <div class="stat-number">{{ unique_cpus }}</div>
                <div class="stat-label">Unique CPU Models</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-desktop"></i></div>
                <div class="stat-number">{{ unique_gpus }}</div>
                <div class="stat-label">Unique GPU Models</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-memory"></i></div>
                <div class="stat-number">{{ avg_ram }} GB</div>
                <div class="stat-label">Average RAM</div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-calendar-week"></i></div>
                <div class="stat-number">{{ tests_last_7d }}</div>
                <div class="stat-label">Tests (Last 7 Days)</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-chart-line"></i></div>
                <div class="stat-number">{{ growth_7d_pct }}%</div>
                <div class="stat-label">7-Day Growth</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-star"></i></div>
                <div class="stat-number">{{ avg_score_overall }}</div>
                <div class="stat-label">Avg Score (Overall)</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-tags"></i></div>
                <div class="stat-number">{{ top_combo_label }}</div>
                <div class="stat-label">Top CPU+GPU Combo</div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart">
                <div class="chart-title"><i class="fas fa-chart-bar"></i> CPU Model Usage</div>
                <div id="cpuChart"></div>
            </div>
            <div class="chart">
                <div class="chart-title"><i class="fas fa-gamepad"></i> GPU Model Usage</div>
                <div id="gpuChart"></div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart">
                <div class="chart-title"><i class="fas fa-chart-pie"></i> RAM Distribution</div>
                <div id="ramPieChart"></div>
            </div>
            <div class="chart">
                <div class="chart-title"><i class="fas fa-tags"></i> CPU vs GPU Brand Distribution</div>
                <div id="brandChart"></div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart">
                <div class="chart-title"><i class="fas fa-cogs"></i> Test Mode Distribution</div>
                <div id="modeChart"></div>
            </div>
            <div class="chart">
                <div class="chart-title"><i class="fas fa-trophy"></i> Average Scores by Mode</div>
                <div id="scoresChart"></div>
            </div>
        </div>

        <div class="chart-container">
            <div class="chart full-width">
                <div class="chart-title"><i class="fas fa-chart-line"></i> Daily Test Activity</div>
                <div id="dailyChart"></div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart">
                <div class="chart-title"><i class="fas fa-bullseye"></i> Device Type Mix</div>
                <div id="deviceTypeChart"></div>
            </div>
            <div class="chart">
                <div class="chart-title"><i class="fas fa-layer-group"></i> RAM Tier Distribution</div>
                <div id="ramTierChart"></div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart">
                <div class="chart-title"><i class="fas fa-project-diagram"></i> CPU vs GPU Brand Heatmap</div>
                <div id="brandHeatmap"></div>
            </div>
            <div class="chart">
                <div class="chart-title"><i class="fas fa-list-ol"></i> Top CPU+GPU Combos</div>
                <div id="comboChart"></div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart full-width">
                <div class="chart-title"><i class="fas fa-microchip"></i> Top 10 CPUs by Avg Score</div>
                <div id="topCpuChart"></div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart full-width">
                <div class="chart-title"><i class="fas fa-sliders-h"></i> Score Distribution</div>
                <div id="scoreHist"></div>
            </div>
        </div>
    </div>

    <script>
        // Enhanced chart configurations with modern styling
        const chartConfig = {
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false,
            responsive: true
        };

        // Modern color palette
        const colors = {
            primary: '#667eea',
            secondary: '#764ba2',
            accent: '#f093fb',
            success: '#10b981',
            warning: '#f59e0b',
            error: '#ef4444'
        };

        function updateChartLayout(layout) {
            return {
                ...layout,
                font: { family: 'Inter, sans-serif', size: 12 },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                margin: { t: 20, r: 20, b: 40, l: 60 }
            };
        }

        // CPU Chart
        var cpuData = {{ cpu_chart_data | safe }};
        if (cpuData.data.length > 0) {
            cpuData.data[0].marker.color = colors.primary;
            cpuData.layout = updateChartLayout(cpuData.layout);
        }
        Plotly.newPlot('cpuChart', cpuData.data, cpuData.layout, chartConfig);

        // GPU Chart
        var gpuData = {{ gpu_chart_data | safe }};
        if (gpuData.data.length > 0) {
            gpuData.data[0].marker.color = colors.secondary;
            gpuData.layout = updateChartLayout(gpuData.layout);
        }
        Plotly.newPlot('gpuChart', gpuData.data, gpuData.layout, chartConfig);

        // RAM Pie Chart
        var ramData = {{ ram_pie_data | safe }};
        if (ramData.data.length > 0) {
            ramData.data[0].marker = {
                colors: [colors.primary, colors.secondary, colors.accent, colors.success, colors.warning]
            };
            ramData.layout = updateChartLayout(ramData.layout);
        }
        Plotly.newPlot('ramPieChart', ramData.data, ramData.layout, chartConfig);

        // Brand Chart
        var brandData = {{ brand_chart_data | safe }};
        if (brandData.data.length > 0) {
            brandData.data.forEach((trace, index) => {
                trace.marker.color = index === 0 ? colors.primary : colors.secondary;
            });
            brandData.layout = updateChartLayout(brandData.layout);
        }
        Plotly.newPlot('brandChart', brandData.data, brandData.layout, chartConfig);

        // Mode Chart
        var modeData = {{ mode_chart_data | safe }};
        if (modeData.data.length > 0) {
            modeData.data[0].marker = {
                colors: [colors.success, colors.warning, colors.error, colors.accent]
            };
            modeData.layout = updateChartLayout(modeData.layout);
        }
        Plotly.newPlot('modeChart', modeData.data, modeData.layout, chartConfig);

        // Scores Chart
        var scoresData = {{ scores_chart_data | safe }};
        if (scoresData.data.length > 0) {
            scoresData.data[0].marker.color = colors.accent;
            scoresData.layout = updateChartLayout(scoresData.layout);
        }
        Plotly.newPlot('scoresChart', scoresData.data, scoresData.layout, chartConfig);

        // Daily Activity Chart
        var dailyData = {{ daily_chart_data | safe }};
        if (dailyData.data.length > 0) {
            dailyData.data[0].line.color = colors.success;
            dailyData.data[0].marker.color = colors.success;
            dailyData.layout = updateChartLayout(dailyData.layout);
        }
        Plotly.newPlot('dailyChart', dailyData.data, dailyData.layout, chartConfig);

        // Device Type Mix
        var deviceTypeData = {{ device_type_chart_data | safe }};
        if (deviceTypeData.data.length > 0) {
            deviceTypeData.data[0].marker = { colors: [colors.primary, colors.secondary, colors.accent] };
            deviceTypeData.layout = updateChartLayout(deviceTypeData.layout);
        }
        Plotly.newPlot('deviceTypeChart', deviceTypeData.data, deviceTypeData.layout, chartConfig);

        // RAM Tier Distribution
        var ramTierData = {{ ram_tier_pie_data | safe }};
        if (ramTierData.data.length > 0) {
            ramTierData.data[0].marker = { colors: [colors.warning, colors.primary, colors.secondary, colors.accent, colors.success] };
            ramTierData.layout = updateChartLayout(ramTierData.layout);
        }
        Plotly.newPlot('ramTierChart', ramTierData.data, ramTierData.layout, chartConfig);

        // Brand Heatmap
        var brandHeatmapData = {{ brand_heatmap_data | safe }};
        brandHeatmapData.layout = updateChartLayout(brandHeatmapData.layout);
        Plotly.newPlot('brandHeatmap', brandHeatmapData.data, brandHeatmapData.layout, chartConfig);

        // Top Combos
        var comboBarData = {{ combo_bar_data | safe }};
        comboBarData.layout = updateChartLayout(comboBarData.layout);
        Plotly.newPlot('comboChart', comboBarData.data, comboBarData.layout, chartConfig);

        // Top 10 CPUs by Avg Score
        var topCpuData = {{ top_cpu_chart_data | safe }};
        topCpuData.layout = updateChartLayout(topCpuData.layout);
        Plotly.newPlot('topCpuChart', topCpuData.data, topCpuData.layout, chartConfig);

        // Score Histogram
        var scoreHistData = {{ score_hist_data | safe }};
        scoreHistData.layout = updateChartLayout(scoreHistData.layout);
        Plotly.newPlot('scoreHist', scoreHistData.data, scoreHistData.layout, chartConfig);

        // Add smooth loading animation
        document.addEventListener('DOMContentLoaded', function() {
            const charts = document.querySelectorAll('.chart');
            charts.forEach((chart, index) => {
                chart.style.opacity = '0';
                chart.style.transform = 'translateY(30px)';
                setTimeout(() => {
                    chart.style.transition = 'all 0.6s ease';
                    chart.style.opacity = '1';
                    chart.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
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
        if collection is not None:
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
        if collection is not None:
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
        if collection is not None:
            data = list(collection.find({}))
        else:
            # Mock data for demo
            logger.warning("MongoDB not available, using mock data")
            data = [
                {
                    'test_device_type': 'CPU',
                    'cpu_brand': 'Intel',
                    'cpu_model': 'i5-13600K',
                    'gpu_brand': 'NVIDIA',
                    'gpu_model': 'RTX 4070',
                    'ram_gb': 32,
                    'test_details': 'AI Model Training Test',
                    'created_at': datetime.now(timezone.utc)
                },
                {
                    'test_device_type': 'GPU',
                    'cpu_brand': 'AMD',
                    'cpu_model': 'Ryzen 7 5800X',
                    'gpu_brand': 'NVIDIA',
                    'gpu_model': 'RTX 4080',
                    'ram_gb': 64,
                    'test_details': 'Deep Learning Inference',
                    'created_at': datetime.now(timezone.utc)
                }
            ]
        
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
        
        # แปลง created_at เป็น datetime ถ้าเป็น string
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
        
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
        df['date'] = df['created_at'].dt.date
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
        
        # 6. Test Mode Distribution (ถ้ามีข้อมูล)
        if 'test_details' in df.columns and len(df) > 0:
            # ดึง mode จาก test_details
            modes = []
            for _, row in df.iterrows():
                if isinstance(row['test_details'], dict) and 'mode' in row['test_details']:
                    modes.append(row['test_details']['mode'])
                else:
                    modes.append('unknown')
            
            mode_counts = pd.Series(modes).value_counts()
            mode_chart_data = {
                'data': [{
                    'labels': mode_counts.index.tolist(),
                    'values': mode_counts.values.tolist(),
                    'type': 'pie',
                    'hole': 0.4
                }],
                'layout': {
                    'title': 'Test Mode Distribution',
                    'height': 400
                }
            }
        else:
            mode_chart_data = {
                'data': [{
                    'labels': ['No mode data'],
                    'values': [1],
                    'type': 'pie',
                    'hole': 0.4
                }],
                'layout': {
                    'title': 'Test Mode Distribution',
                    'height': 400
                }
            }
        
        # 7. Average Scores by Mode (ถ้ามีข้อมูล)
        if 'test_details' in df.columns and len(df) > 0:
            scores_data = []
            for _, row in df.iterrows():
                if isinstance(row['test_details'], dict) and 'avg_score' in row['test_details']:
                    mode = row['test_details'].get('mode', 'unknown')
                    score = row['test_details']['avg_score']
                    scores_data.append({'mode': mode, 'score': score})
            
            if scores_data:
                scores_df = pd.DataFrame(scores_data)
                avg_scores = scores_df.groupby('mode')['score'].mean()
                
                scores_chart_data = {
                    'data': [{
                        'x': avg_scores.index.tolist(),
                        'y': avg_scores.values.tolist(),
                        'type': 'bar',
                        'marker': {'color': '#FF6B6B'}
                    }],
                    'layout': {
                        'title': 'Average Scores by Test Mode',
                        'xaxis': {'title': 'Test Mode'},
                        'yaxis': {'title': 'Average Score'},
                        'height': 400
                    }
                }
            else:
                scores_chart_data = {
                    'data': [{
                        'x': ['No data'],
                        'y': [0],
                        'type': 'bar',
                        'marker': {'color': '#FF6B6B'}
                    }],
                    'layout': {
                        'title': 'Average Scores by Test Mode',
                        'xaxis': {'title': 'Test Mode'},
                        'yaxis': {'title': 'Average Score'},
                        'height': 400
                    }
                }
        else:
            scores_chart_data = {
                'data': [{
                    'x': ['No data'],
                    'y': [0],
                    'type': 'bar',
                    'marker': {'color': '#FF6B6B'}
                }],
                'layout': {
                    'title': 'Average Scores by Test Mode',
                    'xaxis': {'title': 'Test Mode'},
                    'yaxis': {'title': 'Average Score'},
                    'height': 400
                }
            }

        # 8. Marketing/Business insights
        # Time window based on data timeline to avoid tz issues
        now_ts = pd.to_datetime(df['created_at']).max()
        last_7_start = now_ts - pd.Timedelta(days=7) if pd.notna(now_ts) else None
        prev_7_start = now_ts - pd.Timedelta(days=14) if pd.notna(now_ts) else None
        if last_7_start is not None:
            last_7_df = df[df['created_at'] > last_7_start]
            prev_7_df = df[(df['created_at'] > prev_7_start) & (df['created_at'] <= last_7_start)] if prev_7_start is not None else df.iloc[0:0]
            tests_last_7d = int(len(last_7_df))
            prev_cnt = int(len(prev_7_df))
            growth_7d_pct = round(((tests_last_7d - prev_cnt) / (prev_cnt if prev_cnt > 0 else 1)) * 100.0, 1)
        else:
            tests_last_7d = 0
            growth_7d_pct = 0.0

        # Avg score overall
        overall_scores = []
        if 'test_details' in df.columns and len(df) > 0:
            for _, row in df.iterrows():
                if isinstance(row['test_details'], dict) and 'avg_score' in row['test_details']:
                    try:
                        overall_scores.append(float(row['test_details']['avg_score']))
                    except Exception:
                        pass
        avg_score_overall = round(sum(overall_scores) / len(overall_scores), 1) if overall_scores else 0

        # Top CPU+GPU combo
        combo_series = (df['cpu_model'].fillna('Unknown CPU') + ' + ' + df['gpu_model'].fillna('Unknown GPU'))
        combo_counts = combo_series.value_counts()
        if not combo_counts.empty:
            top_combo_label = f"{combo_counts.index[0]}"
        else:
            top_combo_label = 'N/A'

        # Device type mix (pie)
        device_counts = df['test_device_type'].fillna('unknown').value_counts()
        device_type_chart_data = {
            'data': [{
                'labels': device_counts.index.tolist(),
                'values': device_counts.values.tolist(),
                'type': 'pie',
                'hole': 0.35
            }],
            'layout': {
                'title': 'Device Type Mix',
                'height': 400
            }
        }

        # RAM Tiers
        try:
            ram_tiers = pd.cut(df['ram_gb'].astype(float),
                               bins=[0, 8, 16, 32, 64, float('inf')],
                               labels=['<=8 GB', '9-16 GB', '17-32 GB', '33-64 GB', '65+ GB'],
                               include_lowest=True)
            ram_tier_counts = ram_tiers.value_counts().reindex(['<=8 GB', '9-16 GB', '17-32 GB', '33-64 GB', '65+ GB']).fillna(0)
        except Exception:
            ram_tier_counts = pd.Series([], dtype=int)
        ram_tier_pie_data = {
            'data': [{
                'labels': ram_tier_counts.index.astype(str).tolist(),
                'values': ram_tier_counts.values.tolist(),
                'type': 'pie',
                'hole': 0.35
            }],
            'layout': {
                'title': 'RAM Tier Distribution',
                'height': 400
            }
        }

        # CPU vs GPU Brand Heatmap
        brand_matrix = df.pivot_table(index='cpu_brand', columns='gpu_brand', values='test_device_type', aggfunc='count', fill_value=0)
        heatmap_data = {
            'data': [{
                'z': brand_matrix.values.tolist(),
                'x': brand_matrix.columns.astype(str).tolist(),
                'y': brand_matrix.index.astype(str).tolist(),
                'type': 'heatmap',
                'colorscale': 'Blues'
            }],
            'layout': {
                'title': 'CPU vs GPU Brand Heatmap',
                'height': 400
            }
        }

        # Top CPU+GPU combos (bar)
        top_combos = combo_counts.head(10)
        combo_bar_data = {
            'data': [{
                'x': top_combos.values.tolist(),
                'y': top_combos.index.tolist(),
                'type': 'bar',
                'orientation': 'h',
                'marker': {'color': '#546de5'}
            }],
            'layout': {
                'title': 'Top CPU+GPU Combos',
                'xaxis': {'title': 'Count'},
                'yaxis': {'title': 'CPU + GPU'},
                'height': 400
            }
        }

        # Top 10 CPUs by average score (marketing insight: stronger CPU -> better AI performance)
        cpu_scores = []
        if 'test_details' in df.columns and len(df) > 0:
            for _, row in df.iterrows():
                if isinstance(row['test_details'], dict) and 'avg_score' in row['test_details']:
                    try:
                        cpu_scores.append({'cpu_model': row.get('cpu_model', 'Unknown'),
                                           'avg_score': float(row['test_details']['avg_score'])})
                    except Exception:
                        pass
        if cpu_scores:
            cpu_scores_df = pd.DataFrame(cpu_scores)
            top_cpu = cpu_scores_df.groupby('cpu_model')['avg_score'].mean().sort_values(ascending=False).head(10)
        else:
            top_cpu = pd.Series([], dtype=float)
        top_cpu_chart_data = {
            'data': [{
                'x': top_cpu.values.tolist()[::-1],
                'y': top_cpu.index.tolist()[::-1],
                'type': 'bar',
                'orientation': 'h',
                'marker': {'color': '#10b981'}
            }],
            'layout': {
                'title': 'Top 10 CPUs by Avg Score',
                'xaxis': {'title': 'Average Score'},
                'yaxis': {'title': 'CPU Model'},
                'height': 450
            }
        }

        # Score histogram
        score_values = overall_scores
        score_hist_data = {
            'data': [{
                'x': score_values,
                'type': 'histogram',
                'marker': {'color': '#f093fb'}
            }],
            'layout': {
                'title': 'Score Distribution',
                'xaxis': {'title': 'Avg Score'},
                'yaxis': {'title': 'Frequency'},
                'height': 400
            }
        }
        
        return render_template_string(ADMIN_TEMPLATE,
            demo_mode=(collection is None),
            error_message=None,
            total_tests=total_tests,
            unique_cpus=unique_cpus,
            unique_gpus=unique_gpus,
            avg_ram=avg_ram,
            tests_last_7d=tests_last_7d,
            growth_7d_pct=growth_7d_pct,
            avg_score_overall=avg_score_overall,
            top_combo_label=top_combo_label,
            cpu_chart_data=json.dumps(cpu_chart_data),
            gpu_chart_data=json.dumps(gpu_chart_data),
            ram_pie_data=json.dumps(ram_pie_data),
            brand_chart_data=json.dumps(brand_chart_data),
            daily_chart_data=json.dumps(daily_chart_data),
            mode_chart_data=json.dumps(mode_chart_data),
            scores_chart_data=json.dumps(scores_chart_data),
            device_type_chart_data=json.dumps(device_type_chart_data),
            ram_tier_pie_data=json.dumps(ram_tier_pie_data),
            brand_heatmap_data=json.dumps(heatmap_data),
            combo_bar_data=json.dumps(combo_bar_data),
            top_cpu_chart_data=json.dumps(top_cpu_chart_data),
            score_hist_data=json.dumps(score_hist_data)
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
        if collection is not None:
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