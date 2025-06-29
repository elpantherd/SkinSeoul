# SkinSeoul's Automated Merchandising System

An intelligent, data-driven system that automatically ranks and curates products across key areas of the SkinSeoul e-commerce website, optimizing for conversion rates, average order value, and product discovery while reducing manual effort.

## 📊 System Overview

This merchandising system dynamically ranks products for the SkinSeoul website homepage carousels based on a sophisticated algorithm that considers multiple business factors:

- **Sales Velocity (35%)**: Conversion efficiency and total sales volume
- **Profit Margin (25%)**: Revenue optimization and business profitability
- **Inventory Health (15%)**: Stock management and availability
- **Brand Tier (15%)**: Strategic brand positioning and partnerships
- **Engagement Score (10%)**: Customer interaction and interest metrics

![merchandising_algorithm_weights](https://github.com/user-attachments/assets/6793e37f-a90a-468e-9c99-7e554a24ae4e)

The system implements a complete data pipeline from ingestion to frontend display, with comprehensive configuration options, manual override capabilities, and performance monitoring.

## 🚀 Key Features

- **Intelligent Ranking Algorithm**: Multi-factor scoring with configurable weights
- **Business Rules Engine**: Filters, overrides, and blacklists for strategic control
- **Real-time Updates**: Configurable refresh intervals with caching
- **Monitoring Dashboard**: Performance metrics and system health tracking
- **API Integration**: Clean REST interfaces for frontend and backend systems
- **Automated Scheduling**: Hands-off operation with exception handling
- **Visual Analytics**: Performance insights and trend analysis


![correlation_matrix_1](https://github.com/user-attachments/assets/0a3a91fa-c8c0-4109-862f-4e973a64ba27)
![top10_score_breakdown](https://github.com/user-attachments/assets/747fbee9-9a23-4843-8c42-87d93b62964b)
![brand_tier_chart](https://github.com/user-attachments/assets/b13b65cb-9076-4188-9276-73695e876277)
![brand_tier_distribution](https://github.com/user-attachments/assets/09101d38-7ea9-400f-a6a6-a2a9b307014f)
![price_vs_score_scatterplot](https://github.com/user-attachments/assets/a3988338-f9db-4e7f-8e20-f8a5ed3b4fda)

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/skinseoul/ai-merchandising.git
cd ai-merchandising
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run with Docker:
```bash
docker-compose up -d
```

5. Or run locally:
```bash
python app.py
```


## 📈 Performance Analysis

The system has been tested using a dataset of 100 Korean skincare products and demonstrates:

- **Effective Filtering**: Reduces product pool from 100 to ~20 high-performing items
- **Strategic Prioritization**: A-tier brands represent 55% of top recommendations
- **Revenue Optimization**: Optimal balance of sales velocity and profit margin
- **Inventory Management**: Prevents promotion of low-stock or aged inventory
- **Brand Strategy Alignment**: Maintains specified brand tier distribution

## 📋 API Documentation

### Endpoints

- `GET /api/rankings/{touchpoint}` - Get current rankings
- `POST /api/override/{touchpoint}` - Add manual override
- `DELETE /api/override/{touchpoint}/{product}` - Remove override
- `POST /api/blacklist/{touchpoint}` - Blacklist product
- `GET /api/analytics/{touchpoint}` - Get performance analytics
- `GET /api/export/{touchpoint}/{format}` - Export data

### Example Response

```json
{
  "touchpoint": "homepage_carousel",
  "generated_at": "2025-06-23T09:14:33.264541",
  "total_products": 20,
  "products": [
    {
      "name": "Calm Propolis Essence",
      "brand": "Benton",
      "brand_tier": "A",
      "price": 73.65,
      "position": 1,
      "merchandising_score": 95.3,
      "is_manual_override": false
    },
    // ...more products
  ]
}
```

## 🔄 Frontend Integration

The system provides multiple integration options:

1. **REST API**: Direct API calls with JSON responses
2. **JavaScript SDK**: Simple drop-in integration (recommended)
3. **Webhook Events**: Real-time updates via WebSocket
4. **Export Formats**: JSON, CSV, and frontend-optimized formats

## 📊 Business Impact

Implementation of this merchandising system is expected to deliver:

- **+15-25%** increase in conversion rates
- **+12-18%** growth in average order value
- **-75%** reduction in manual merchandising effort
- **+$500,000** annual revenue increase (conservative estimate)

## 🛡️ Security & Reliability

- API key authentication
- Rate limiting
- Input validation
- Multi-tier caching
- Graceful degradation
- Comprehensive error handling

## 📜 License

Copyright © 2025 SkinSeoul. All rights reserved.
