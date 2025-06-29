# 9. Create HTML Dashboard for Merchandising Management

dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkinSeoul AI Merchandising Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .stat-label {
            color: #666;
            font-size: 1rem;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }
        
        .rankings-panel {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .control-panel {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .section-title {
            font-size: 1.5rem;
            color: #667eea;
            margin-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }
        
        .product-list {
            list-style: none;
        }
        
        .product-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9ff;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .product-item:hover {
            background: #e8ecff;
            transform: translateX(5px);
        }
        
        .product-info {
            flex: 1;
        }
        
        .product-name {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .product-details {
            font-size: 0.9rem;
            color: #666;
        }
        
        .product-score {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .control-section {
            margin-bottom: 30px;
        }
        
        .control-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        .form-label {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .form-input,
        .form-select {
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .form-input:focus,
        .form-select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .btn:hover {
            background: #5a67d8;
        }
        
        .btn-secondary {
            background: #764ba2;
        }
        
        .btn-secondary:hover {
            background: #6b46c1;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-warning {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .touchpoint-tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .tab {
            padding: 12px 24px;
            background: none;
            border: none;
            font-size: 1rem;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
            font-weight: bold;
        }
        
        .tab:hover {
            background: #f8f9ff;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧴 SkinSeoul AI Merchandising Dashboard</h1>
            <p>Intelligent Product Ranking & Automated Merchandising System</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="totalProducts">20</div>
                <div class="stat-label">Active Products</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalRevenue">$258,301</div>
                <div class="stat-label">Monthly Revenue</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avgScore">88.4</div>
                <div class="stat-label">Avg Merchandising Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="lastUpdate">2 min ago</div>
                <div class="stat-label">Last Update</div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="rankings-panel">
                <div class="touchpoint-tabs">
                    <button class="tab active" onclick="switchTouchpoint('homepage_carousel')">Homepage Carousel</button>
                    <button class="tab" onclick="switchTouchpoint('collection_page')">Collection Page</button>
                </div>
                
                <h2 class="section-title">🏆 Current Rankings</h2>
                <div id="alertContainer"></div>
                
                <ul class="product-list" id="productList">
                    <!-- Dynamic content will be loaded here -->
                </ul>
            </div>
            
            <div class="control-panel">
                <div class="control-section">
                    <h3 class="section-title">⚡ Manual Override</h3>
                    <form class="control-form" id="overrideForm">
                        <div class="form-group">
                            <label class="form-label">Product Name</label>
                            <select class="form-select" id="overrideProduct">
                                <option value="">Select a product...</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Target Position</label>
                            <input type="number" class="form-input" id="overridePosition" min="1" max="20" placeholder="1">
                        </div>
                        <button type="submit" class="btn">Apply Override</button>
                    </form>
                </div>
                
                <div class="control-section">
                    <h3 class="section-title">🚫 Product Management</h3>
                    <form class="control-form" id="blacklistForm">
                        <div class="form-group">
                            <label class="form-label">Blacklist Product</label>
                            <select class="form-select" id="blacklistProduct">
                                <option value="">Select a product...</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-secondary">Blacklist Product</button>
                    </form>
                </div>
                
                <div class="control-section">
                    <h3 class="section-title">🔄 System Actions</h3>
                    <button class="btn" onclick="refreshRankings()" style="width: 100%; margin-bottom: 10px;">
                        Refresh Rankings
                    </button>
                    <button class="btn btn-secondary" onclick="exportData()" style="width: 100%;">
                        Export Data
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Sample data - in real implementation, this would come from the API
        const sampleRankings = {
            homepage_carousel: [
                { name: "Fresh Snail Mucin Cleanser", brand: "Skinfood", brand_tier: "A", price: 76.55, merchandising_score: 95.2, is_manual_override: true },
                { name: "Hydra Ginseng Serum", brand: "Sulwhasoo", brand_tier: "A", price: 66.15, merchandising_score: 93.0, is_manual_override: false },
                { name: "Radiant Collagen Lotion", brand: "Missha", brand_tier: "A", price: 53.63, merchandising_score: 91.6, is_manual_override: false },
                { name: "Soothing Mugwort Emulsion", brand: "Benton", brand_tier: "A", price: 12.41, merchandising_score: 91.0, is_manual_override: false },
                { name: "Soothing Niacinamide Emulsion", brand: "Dr. Jart+", brand_tier: "A", price: 56.38, merchandising_score: 90.8, is_manual_override: false }
            ],
            collection_page: [
                { name: "Glow Vitamin C Ampoule", brand: "Laneige", brand_tier: "B", price: 52.08, merchandising_score: 87.5, is_manual_override: false },
                { name: "Fresh Green Tea Essence", brand: "Mamonde", brand_tier: "B", price: 77.87, merchandising_score: 86.2, is_manual_override: false },
                { name: "Pure Collagen Toner", brand: "Neogen", brand_tier: "A", price: 24.86, merchandising_score: 85.8, is_manual_override: false }
            ]
        };
        
        let currentTouchpoint = 'homepage_carousel';
        
        function switchTouchpoint(touchpoint) {
            currentTouchpoint = touchpoint;
            
            // Update tab styles
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
            
            // Load rankings for the selected touchpoint
            loadRankings();
        }
        
        function loadRankings() {
            const rankings = sampleRankings[currentTouchpoint] || [];
            const productList = document.getElementById('productList');
            
            productList.innerHTML = '';
            
            rankings.forEach((product, index) => {
                const listItem = document.createElement('li');
                listItem.className = 'product-item';
                listItem.innerHTML = `
                    <div class="product-info">
                        <div class="product-name">${index + 1}. ${product.name}</div>
                        <div class="product-details">
                            ${product.brand} • ${product.brand_tier}-tier • $${product.price.toFixed(2)}
                            ${product.is_manual_override ? ' • <strong>Manual Override</strong>' : ''}
                        </div>
                    </div>
                    <div class="product-score">${product.merchandising_score.toFixed(1)}</div>
                `;
                productList.appendChild(listItem);
            });
            
            // Update product dropdowns
            updateProductDropdowns(rankings);
        }
        
        function updateProductDropdowns(rankings) {
            const overrideSelect = document.getElementById('overrideProduct');
            const blacklistSelect = document.getElementById('blacklistProduct');
            
            // Clear existing options
            overrideSelect.innerHTML = '<option value="">Select a product...</option>';
            blacklistSelect.innerHTML = '<option value="">Select a product...</option>';
            
            // Add product options
            rankings.forEach(product => {
                const option1 = document.createElement('option');
                option1.value = product.name;
                option1.textContent = product.name;
                overrideSelect.appendChild(option1);
                
                const option2 = document.createElement('option');
                option2.value = product.name;
                option2.textContent = product.name;
                blacklistSelect.appendChild(option2);
            });
        }
        
        function showAlert(message, type = 'success') {
            const alertContainer = document.getElementById('alertContainer');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            
            alertContainer.innerHTML = '';
            alertContainer.appendChild(alert);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }
        
        function refreshRankings() {
            showAlert('Rankings refreshed successfully!');
            loadRankings();
            
            // Update last update time
            document.getElementById('lastUpdate').textContent = 'Just now';
        }
        
        function exportData() {
            // In real implementation, this would trigger a download
            const data = JSON.stringify(sampleRankings[currentTouchpoint], null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${currentTouchpoint}_rankings.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showAlert('Data exported successfully!');
        }
        
        // Form handlers
        document.getElementById('overrideForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const product = document.getElementById('overrideProduct').value;
            const position = document.getElementById('overridePosition').value;
            
            if (product && position) {
                showAlert(`Manual override applied: ${product} moved to position ${position}`);
                this.reset();
            } else {
                showAlert('Please select a product and position', 'warning');
            }
        });
        
        document.getElementById('blacklistForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const product = document.getElementById('blacklistProduct').value;
            
            if (product) {
                showAlert(`Product blacklisted: ${product}`, 'warning');
                this.reset();
            } else {
                showAlert('Please select a product to blacklist', 'warning');
            }
        });
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            loadRankings();
        });
    </script>
</body>
</html>"""

# Save dashboard HTML
with open('merchandising_dashboard.html', 'w') as f:
    f.write(dashboard_html)

print("✅ Merchandising Dashboard created: merchandising_dashboard.html")
print(f"   HTML file size: {len(dashboard_html)} characters")
print("   Features: Rankings display, manual overrides, product management, real-time updates")

# 10. Create deployment configuration files

# Docker configuration
dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
"""

# Requirements file
requirements_content = """fastapi==0.104.1
uvicorn==0.24.0
gunicorn==21.2.0
pandas==2.1.3
numpy==1.24.3
redis==5.0.1
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
python-multipart==0.0.6
aioredis==2.0.1
celery==5.3.4
schedule==1.2.0
python-dotenv==1.0.0
prometheus-client==0.19.0
structlog==23.2.0
"""

# Environment configuration
env_config = """# SkinSeoul AI Merchandising System Configuration

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/skinseoul_merchandising
REDIS_URL=redis://localhost:6379/0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
DEBUG=False

# Cache Configuration
CACHE_TTL_HOURS=1
CACHE_MAX_SIZE=1000

# Merchandising Configuration
DEFAULT_MAX_PRODUCTS=20
DEFAULT_REFRESH_INTERVAL=1
ENABLE_SEASONAL_BOOST=true
ENABLE_MANUAL_OVERRIDES=true

# Monitoring Configuration
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO
HEALTH_CHECK_INTERVAL=30

# Security Configuration
API_KEY_REQUIRED=true
CORS_ORIGINS=["https://skin-seoul.com", "https://admin.skin-seoul.com"]
RATE_LIMIT_PER_MINUTE=100

# Business Rules
MIN_STOCK_UNITS=10
MAX_INVENTORY_DAYS=90
MIN_PROFIT_MARGIN=20.0
MIN_VIEWS_THRESHOLD=100

# Notification Configuration
SLACK_WEBHOOK_URL=
EMAIL_ALERTS_ENABLED=false
ALERT_THRESHOLD_SCORE_DROP=10
"""

# Docker Compose file
docker_compose_content = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/skinseoul
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=skinseoul
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  scheduler:
    build: .
    command: python scheduler.py
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/skinseoul
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
"""

# Save all configuration files
with open('Dockerfile', 'w') as f:
    f.write(dockerfile_content)

with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

with open('.env.example', 'w') as f:
    f.write(env_config)

with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose_content)

print("\n✅ Deployment Configuration Files created:")
print("   - Dockerfile (containerization)")
print("   - requirements.txt (Python dependencies)")
print("   - .env.example (environment configuration)")
print("   - docker-compose.yml (multi-service deployment)")
print("   - merchandising_dashboard.html (management interface)")

print(f"\n📁 Complete codebase files generated:")
files_created = [
    "process_flow_documentation.md",
    "merchandising_dashboard.html", 
    "Dockerfile",
    "requirements.txt",
    ".env.example",
    "docker-compose.yml"
]

for file in files_created:
    print(f"   ✓ {file}")

print(f"\n🎯 System Overview:")
print(f"   - Core Engine: Product scoring, filtering, ranking algorithms")
print(f"   - API Layer: RESTful endpoints with caching and override management")
print(f"   - Automation: Scheduled refreshes and performance monitoring")
print(f"   - Dashboard: Web interface for business users")
print(f"   - Deployment: Docker containerization with multi-service architecture")
print(f"   - Documentation: Complete process flow and technical specifications")