
# SkinSeoul AI-Powered Automated Merchandising System
## Process Flow Documentation

### System Architecture Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Core Engine     │───▶│   Output APIs   │
│   - Product DB  │    │  - Scoring       │    │   - Rankings    │
│   - Analytics   │    │  - Filtering     │    │   - JSON/CSV    │
│   - Inventory   │    │  - Caching       │    │   - Frontend    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Management Layer│
                    │  - Overrides     │
                    │  - Scheduling    │
                    │  - Monitoring    │
                    └──────────────────┘
```

### Data Flow Process

#### 1. Data Ingestion
- **Source**: Mock_Skincare_Dataset.xlsx (100 Korean skincare products)
- **Fields**: Product Name, Brand, Brand Tier, Price, COGS, Inventory, Views, Sales
- **Processing**: Data validation, type conversion, calculated metrics generation
- **Output**: Product objects with enhanced analytics

#### 2. Filtering Stage
- **Stock Filter**: Exclude products with < 10 units (configurable)
- **Inventory Filter**: Exclude products with > 90 days inventory
- **Profit Filter**: Exclude products with < 20% margin (configurable)
- **Engagement Filter**: Exclude products with < 100 views (configurable)
- **Blacklist Filter**: Exclude manually blacklisted products

#### 3. Scoring Algorithm
**Weighted Composite Score (0-100):**
- Sales Velocity (35%): Conversion rate + Volume sold relative to category
- Profit Margin (25%): Gross margin percentage normalized to 100
- Inventory Health (15%): Optimal range 30-90 days, penalties outside
- Brand Tier (15%): A-tier=100, B-tier=75, C-tier=50 points
- Engagement Score (10%): Page views normalized to 100 scale

#### 4. Ranking Generation
- Sort products by composite score (descending)
- Apply manual overrides (specific position assignments)
- Enforce maximum product limits per touchpoint
- Generate final ranked list with metadata

#### 5. Output Generation
- **API Response**: JSON with product details, scores, positions
- **Frontend Config**: Optimized format for web integration
- **CSV Export**: Analytics-friendly format for reporting
- **Cache Storage**: Temporary storage with TTL for performance

#### 6. Automation Layer
- **Scheduled Refresh**: Automatic updates per touchpoint configuration
- **Inventory Monitoring**: Alerts for low stock and excess inventory
- **Performance Tracking**: Historical metrics and trend analysis
- **Override Management**: Business rules and manual interventions

### Touchpoint Configurations

#### Homepage Carousel
- **Purpose**: High-conversion product showcase
- **Max Products**: 20
- **Refresh**: Every 1 hour
- **Scoring Weights**: Sales Velocity 35%, Profit 25%, Inventory 15%, Brand 15%, Engagement 10%
- **Filters**: Min 15 units stock, Max 60 days inventory, Min 25% margin, Min 500 views

#### Collection Page
- **Purpose**: Category-specific product discovery
- **Max Products**: 48
- **Refresh**: Every 6 hours
- **Scoring Weights**: Balanced across all factors
- **Filters**: More lenient for broader product variety

### Business Rules Engine

#### Manual Overrides
- Emergency promotions (immediate positioning)
- Brand campaign support (temporary algorithmic adjustments)
- Seasonal adjustments (holiday/event-based modifications)
- Strategic partnerships (preferred brand positioning)

#### Automated Responses
- Out-of-stock removal (immediate)
- Low inventory alerts (< 20 units)
- High inventory flags (> 90 days)
- Performance anomaly detection (score variance > 10%)

### Performance Monitoring

#### Key Metrics
- Total Revenue Impact
- Average Merchandising Score
- Brand Tier Distribution
- Conversion Rate Changes
- Manual Override Usage

#### Alerts and Notifications
- System health monitoring
- Data quality validation
- Performance degradation detection
- Inventory level warnings

### API Endpoints Summary
- `GET /rankings/{touchpoint}` - Get current rankings
- `POST /override/{touchpoint}` - Add manual override
- `DELETE /override/{touchpoint}/{product}` - Remove override
- `POST /blacklist/{touchpoint}` - Blacklist product
- `GET /analytics/{touchpoint}` - Get performance analytics
- `GET /export/{touchpoint}/{format}` - Export data

### Integration Points

#### Frontend Integration
- JavaScript SDK for dynamic content loading
- Real-time updates via WebSocket connections
- Fallback mechanisms for system downtime
- A/B testing framework support

#### Backend Integration
- RESTful API architecture
- Database synchronization
- Cache invalidation strategies
- Event-driven updates

### Security and Reliability

#### Data Protection
- API rate limiting
- Input validation and sanitization
- Secure configuration management
- Audit logging for all changes

#### System Reliability
- Multi-tier caching strategy
- Graceful degradation mechanisms
- Automated failover procedures
- Comprehensive error handling

### Deployment Architecture

#### Development Environment
- Local development server
- Mock data for testing
- Configuration management
- Unit and integration testing

#### Production Environment
- Load-balanced API servers
- Redis cache cluster
- PostgreSQL database
- Monitoring and alerting stack

This documentation provides a comprehensive overview of the AI-powered automated merchandising system, covering all aspects from data ingestion to production deployment.
