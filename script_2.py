# 2. Configuration Management System
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class TouchpointType(Enum):
    HOMEPAGE_CAROUSEL = "homepage_carousel"
    COLLECTION_PAGE = "collection_page"
    UPSELL_WIDGET = "upsell_widget"
    CHECKOUT_ADDON = "checkout_addon"

@dataclass
class ScoringWeights:
    sales_velocity: float = 0.30
    profit_margin: float = 0.25
    inventory_health: float = 0.20
    brand_tier: float = 0.15
    engagement_score: float = 0.10

@dataclass
class FilterCriteria:
    min_stock_units: int = 10
    max_days_inventory: int = 90
    min_profit_margin: float = 20.0
    exclude_out_of_stock: bool = True
    min_views_threshold: int = 100

@dataclass
class MerchandisingConfig:
    touchpoint_type: TouchpointType
    max_products: int
    scoring_weights: ScoringWeights
    filter_criteria: FilterCriteria
    refresh_interval_hours: int = 1
    allow_manual_overrides: bool = True
    seasonal_boost_enabled: bool = True

# Configuration for different touchpoints
TOUCHPOINT_CONFIGS = {
    TouchpointType.HOMEPAGE_CAROUSEL: MerchandisingConfig(
        touchpoint_type=TouchpointType.HOMEPAGE_CAROUSEL,
        max_products=20,
        scoring_weights=ScoringWeights(
            sales_velocity=0.35,
            profit_margin=0.25,
            inventory_health=0.15,
            brand_tier=0.15,
            engagement_score=0.10
        ),
        filter_criteria=FilterCriteria(
            min_stock_units=15,
            max_days_inventory=60,
            min_profit_margin=25.0,
            exclude_out_of_stock=True,
            min_views_threshold=500
        ),
        refresh_interval_hours=1
    ),
    TouchpointType.COLLECTION_PAGE: MerchandisingConfig(
        touchpoint_type=TouchpointType.COLLECTION_PAGE,
        max_products=48,
        scoring_weights=ScoringWeights(
            sales_velocity=0.25,
            profit_margin=0.20,
            inventory_health=0.25,
            brand_tier=0.20,
            engagement_score=0.10
        ),
        filter_criteria=FilterCriteria(
            min_stock_units=5,
            max_days_inventory=120,
            min_profit_margin=15.0,
            exclude_out_of_stock=True,
            min_views_threshold=100
        ),
        refresh_interval_hours=6
    )
}

print("Configuration system initialized")
print("Available touchpoint configurations:")
for touchpoint, config in TOUCHPOINT_CONFIGS.items():
    print(f"- {touchpoint.value}: Max products = {config.max_products}, Refresh = {config.refresh_interval_hours}h")