# 4. API Layer and Override Management
from flask import Flask, jsonify, request
from datetime import datetime
import uuid

class MerchandisingAPI:
    def __init__(self):
        self.engines = {}
        self.cache = {}
        self.cache_expiry = {}
        
        # Initialize engines for each touchpoint
        for touchpoint_type, config in TOUCHPOINT_CONFIGS.items():
            self.engines[touchpoint_type] = MerchandisingEngine(config)
    
    def get_rankings(self, touchpoint: TouchpointType, force_refresh: bool = False) -> dict:
        """Get rankings for a specific touchpoint with caching"""
        cache_key = f"{touchpoint.value}_rankings"
        
        # Check cache validity
        if not force_refresh and cache_key in self.cache:
            if datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
                return self.cache[cache_key]
        
        # Generate fresh rankings
        engine = self.engines[touchpoint]
        rankings = engine.generate_rankings(products)
        
        # Prepare response
        response = {
            'touchpoint': touchpoint.value,
            'generated_at': datetime.now().isoformat(),
            'total_products': len(rankings),
            'max_products': engine.config.max_products,
            'products': []
        }
        
        for i, (product, score) in enumerate(rankings):
            product_data = product.to_dict()
            product_data.update({
                'position': i + 1,
                'merchandising_score': round(score, 2),
                'is_manual_override': product.name in engine.manual_overrides
            })
            response['products'].append(product_data)
        
        # Cache the response
        cache_duration = timedelta(hours=engine.config.refresh_interval_hours)
        self.cache[cache_key] = response
        self.cache_expiry[cache_key] = datetime.now() + cache_duration
        
        return response
    
    def add_manual_override(self, touchpoint: TouchpointType, product_name: str, position: int) -> dict:
        """Add manual override for product positioning"""
        engine = self.engines[touchpoint]
        engine.manual_overrides[product_name] = position - 1  # Convert to 0-based index
        
        # Clear cache to force refresh
        cache_key = f"{touchpoint.value}_rankings"
        if cache_key in self.cache:
            del self.cache[cache_key]
        
        return {
            'status': 'success',
            'message': f'Manual override added: {product_name} at position {position}',
            'touchpoint': touchpoint.value
        }
    
    def remove_manual_override(self, touchpoint: TouchpointType, product_name: str) -> dict:
        """Remove manual override for product"""
        engine = self.engines[touchpoint]
        if product_name in engine.manual_overrides:
            del engine.manual_overrides[product_name]
            
            # Clear cache to force refresh
            cache_key = f"{touchpoint.value}_rankings"
            if cache_key in self.cache:
                del self.cache[cache_key]
            
            return {
                'status': 'success',
                'message': f'Manual override removed for {product_name}',
                'touchpoint': touchpoint.value
            }
        else:
            return {
                'status': 'error',
                'message': f'No manual override found for {product_name}',
                'touchpoint': touchpoint.value
            }
    
    def blacklist_product(self, touchpoint: TouchpointType, product_name: str) -> dict:
        """Blacklist a product from appearing in rankings"""
        engine = self.engines[touchpoint]
        engine.blacklisted_products.add(product_name)
        
        # Clear cache to force refresh
        cache_key = f"{touchpoint.value}_rankings"
        if cache_key in self.cache:
            del self.cache[cache_key]
        
        return {
            'status': 'success',
            'message': f'Product blacklisted: {product_name}',
            'touchpoint': touchpoint.value
        }
    
    def update_scoring_weights(self, touchpoint: TouchpointType, weights: dict) -> dict:
        """Update scoring weights for a touchpoint"""
        engine = self.engines[touchpoint]
        
        # Validate weights sum to 1.0
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            return {
                'status': 'error',
                'message': f'Weights must sum to 1.0, got {total_weight}'
            }
        
        # Update weights
        for key, value in weights.items():
            if hasattr(engine.config.scoring_weights, key):
                setattr(engine.config.scoring_weights, key, value)
        
        # Clear cache to force refresh
        cache_key = f"{touchpoint.value}_rankings"
        if cache_key in self.cache:
            del self.cache[cache_key]
        
        return {
            'status': 'success',
            'message': 'Scoring weights updated',
            'touchpoint': touchpoint.value,
            'new_weights': weights
        }

# Initialize API
api = MerchandisingAPI()

# Test API functionality
print("Testing Merchandising API:")
print("=" * 50)

# Get homepage rankings
homepage_data = api.get_rankings(TouchpointType.HOMEPAGE_CAROUSEL)
print(f"Homepage rankings generated at: {homepage_data['generated_at']}")
print(f"Total products: {homepage_data['total_products']}")

# Test manual override
override_result = api.add_manual_override(
    TouchpointType.HOMEPAGE_CAROUSEL, 
    "Fresh Snail Mucin Cleanser", 
    1
)
print(f"Override result: {override_result['message']}")

# Get updated rankings
updated_homepage_data = api.get_rankings(TouchpointType.HOMEPAGE_CAROUSEL, force_refresh=True)
print(f"Top product after override: {updated_homepage_data['products'][0]['name']}")
print(f"Is manual override: {updated_homepage_data['products'][0]['is_manual_override']}")

# Test weight update
weight_update_result = api.update_scoring_weights(
    TouchpointType.HOMEPAGE_CAROUSEL,
    {
        'sales_velocity': 0.40,
        'profit_margin': 0.20,
        'inventory_health': 0.15,
        'brand_tier': 0.15,
        'engagement_score': 0.10
    }
)
print(f"Weight update result: {weight_update_result['status']}")