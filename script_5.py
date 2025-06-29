# 4. API Layer and Override Management (without Flask)
from datetime import datetime
import json

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
            'configuration': {
                'refresh_interval_hours': engine.config.refresh_interval_hours,
                'scoring_weights': {
                    'sales_velocity': engine.config.scoring_weights.sales_velocity,
                    'profit_margin': engine.config.scoring_weights.profit_margin,
                    'inventory_health': engine.config.scoring_weights.inventory_health,
                    'brand_tier': engine.config.scoring_weights.brand_tier,
                    'engagement_score': engine.config.scoring_weights.engagement_score
                }
            },
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
            'touchpoint': touchpoint.value,
            'timestamp': datetime.now().isoformat()
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
                'touchpoint': touchpoint.value,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'status': 'error',
                'message': f'No manual override found for {product_name}',
                'touchpoint': touchpoint.value,
                'timestamp': datetime.now().isoformat()
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
            'touchpoint': touchpoint.value,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_analytics_summary(self, touchpoint: TouchpointType) -> dict:
        """Get analytics summary for a touchpoint"""
        engine = self.engines[touchpoint]
        rankings = engine.generate_rankings(products)
        
        # Calculate analytics
        total_revenue = sum(p.revenue_last_month for p, _ in rankings)
        avg_score = sum(score for _, score in rankings) / len(rankings) if rankings else 0
        brand_tier_distribution = {}
        brand_distribution = {}
        
        for product, score in rankings:
            # Brand tier distribution
            if product.brand_tier not in brand_tier_distribution:
                brand_tier_distribution[product.brand_tier] = 0
            brand_tier_distribution[product.brand_tier] += 1
            
            # Brand distribution
            if product.brand not in brand_distribution:
                brand_distribution[product.brand] = 0
            brand_distribution[product.brand] += 1
        
        return {
            'touchpoint': touchpoint.value,
            'analytics': {
                'total_products': len(rankings),
                'total_revenue_last_month': round(total_revenue, 2),
                'average_merchandising_score': round(avg_score, 2),
                'brand_tier_distribution': brand_tier_distribution,
                'top_brands': dict(sorted(brand_distribution.items(), key=lambda x: x[1], reverse=True)[:5]),
                'manual_overrides_count': len(engine.manual_overrides),
                'blacklisted_products_count': len(engine.blacklisted_products)
            },
            'generated_at': datetime.now().isoformat()
        }

# Initialize API
api = MerchandisingAPI()

print("Testing Merchandising API:")
print("=" * 60)

# Get homepage rankings
homepage_data = api.get_rankings(TouchpointType.HOMEPAGE_CAROUSEL)
print(f"Homepage rankings generated at: {homepage_data['generated_at']}")
print(f"Total products: {homepage_data['total_products']}")
print(f"Current scoring weights: {homepage_data['configuration']['scoring_weights']}")

# Test manual override
print("\n1. Testing Manual Override:")
override_result = api.add_manual_override(
    TouchpointType.HOMEPAGE_CAROUSEL, 
    "Fresh Snail Mucin Cleanser", 
    1
)
print(f"   {override_result['message']}")

# Get updated rankings
updated_homepage_data = api.get_rankings(TouchpointType.HOMEPAGE_CAROUSEL, force_refresh=True)
print(f"   Top product after override: {updated_homepage_data['products'][0]['name']}")
print(f"   Is manual override: {updated_homepage_data['products'][0]['is_manual_override']}")

# Test blacklisting
print("\n2. Testing Product Blacklisting:")
blacklist_result = api.blacklist_product(
    TouchpointType.HOMEPAGE_CAROUSEL,
    "Calm Propolis Essence"
)
print(f"   {blacklist_result['message']}")

# Get analytics
print("\n3. Analytics Summary:")
analytics = api.get_analytics_summary(TouchpointType.HOMEPAGE_CAROUSEL)
print(f"   Total Revenue: ${analytics['analytics']['total_revenue_last_month']:,.2f}")
print(f"   Average Score: {analytics['analytics']['average_merchandising_score']:.1f}")
print(f"   Brand Tier Distribution: {analytics['analytics']['brand_tier_distribution']}")
print(f"   Top Brands: {list(analytics['analytics']['top_brands'].keys())}")