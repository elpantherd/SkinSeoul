# 3. Core Merchandising Engine
import math
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

class MerchandisingEngine:
    def __init__(self, config: MerchandisingConfig):
        self.config = config
        self.manual_overrides = {}  # product_name -> position
        self.blacklisted_products = set()
        self.seasonal_boosts = {}  # product_name -> boost_multiplier
        
    def calculate_sales_velocity_score(self, product: Product) -> float:
        """Calculate sales velocity score (0-100)"""
        if product.views_last_month == 0:
            return 0
        
        # Base conversion rate score
        conversion_score = min(product.conversion_rate * 10, 100)
        
        # Volume sold relative to category average
        volume_score = min((product.volume_sold_last_month / 200) * 100, 100)
        
        # Combine both metrics
        return (conversion_score * 0.6 + volume_score * 0.4)
    
    def calculate_profit_margin_score(self, product: Product) -> float:
        """Calculate profit margin score (0-100)"""
        # Normalize profit margin to 0-100 scale
        # Assuming 50%+ margin gets full score
        return min(product.profit_margin * 2, 100)
    
    def calculate_inventory_health_score(self, product: Product) -> float:
        """Calculate inventory health score (0-100)"""
        days_inventory = product.days_inventory
        
        # Optimal range: 30-90 days
        if 30 <= days_inventory <= 90:
            return 100
        elif days_inventory < 30:
            # Penalize low inventory
            return max(0, (days_inventory / 30) * 100)
        else:
            # Penalize excess inventory
            return max(0, 100 - ((days_inventory - 90) / 100) * 50)
    
    def calculate_brand_tier_score(self, product: Product) -> float:
        """Calculate brand tier score (0-100)"""
        tier_scores = {
            'A': 100,  # Premium brands
            'B': 75,   # Mainstream brands  
            'C': 50    # Value brands
        }
        return tier_scores.get(product.brand_tier, 50)
    
    def calculate_engagement_score(self, product: Product) -> float:
        """Calculate engagement score (0-100)"""
        # Normalize views to 0-100 scale
        # Assuming 5000+ views gets full score
        return min((product.views_last_month / 5000) * 100, 100)
    
    def calculate_composite_score(self, product: Product) -> float:
        """Calculate final composite merchandising score"""
        weights = self.config.scoring_weights
        
        # Calculate individual scores
        velocity_score = self.calculate_sales_velocity_score(product)
        profit_score = self.calculate_profit_margin_score(product)
        inventory_score = self.calculate_inventory_health_score(product)
        brand_score = self.calculate_brand_tier_score(product)
        engagement_score = self.calculate_engagement_score(product)
        
        # Calculate weighted composite score
        composite_score = (
            velocity_score * weights.sales_velocity +
            profit_score * weights.profit_margin +
            inventory_score * weights.inventory_health +
            brand_score * weights.brand_tier +
            engagement_score * weights.engagement_score
        )
        
        # Apply seasonal boost if enabled
        if self.config.seasonal_boost_enabled and product.name in self.seasonal_boosts:
            composite_score *= self.seasonal_boosts[product.name]
        
        return min(composite_score, 100)  # Cap at 100
    
    def apply_filters(self, products: List[Product]) -> List[Product]:
        """Apply filtering criteria to products"""
        filtered_products = []
        criteria = self.config.filter_criteria
        
        for product in products:
            # Skip blacklisted products
            if product.name in self.blacklisted_products:
                continue
                
            # Apply stock filter
            if criteria.exclude_out_of_stock and product.units_stock < criteria.min_stock_units:
                continue
                
            # Apply inventory days filter
            if product.days_inventory > criteria.max_days_inventory:
                continue
                
            # Apply profit margin filter
            if product.profit_margin < criteria.min_profit_margin:
                continue
                
            # Apply views threshold filter
            if product.views_last_month < criteria.min_views_threshold:
                continue
                
            filtered_products.append(product)
        
        return filtered_products
    
    def generate_rankings(self, products: List[Product]) -> List[Tuple[Product, float]]:
        """Generate ranked product list with scores"""
        # Apply filters
        filtered_products = self.apply_filters(products)
        
        # Calculate scores for all products
        scored_products = []
        for product in filtered_products:
            score = self.calculate_composite_score(product)
            scored_products.append((product, score))
        
        # Sort by score (descending)
        scored_products.sort(key=lambda x: x[1], reverse=True)
        
        # Apply manual overrides
        final_rankings = []
        override_positions = {}
        
        # First, place manually overridden products
        for product_name, position in self.manual_overrides.items():
            for product, score in scored_products:
                if product.name == product_name:
                    override_positions[position] = (product, score)
                    break
        
        # Then fill remaining positions with algorithmic rankings
        position = 0
        for product, score in scored_products:
            if product.name not in self.manual_overrides:
                while position in override_positions:
                    final_rankings.append(override_positions[position])
                    position += 1
                final_rankings.append((product, score))
                position += 1
            
            if len(final_rankings) >= self.config.max_products:
                break
        
        # Add any remaining override products
        for pos in sorted(override_positions.keys()):
            if pos >= len(final_rankings):
                final_rankings.append(override_positions[pos])
        
        return final_rankings[:self.config.max_products]

# Test the merchandising engine
engine = MerchandisingEngine(TOUCHPOINT_CONFIGS[TouchpointType.HOMEPAGE_CAROUSEL])

# Generate rankings for homepage carousel
homepage_rankings = engine.generate_rankings(products)

print("Homepage Carousel Rankings (Top 10):")
print("-" * 80)
for i, (product, score) in enumerate(homepage_rankings[:10]):
    print(f"{i+1:2d}. {product.name:<35} | Score: {score:5.1f} | Brand: {product.brand:<12} | Tier: {product.brand_tier} | Margin: {product.profit_margin:5.1f}%")

print(f"\nTotal qualified products: {len(homepage_rankings)}")
print(f"Products filtered out: {len(products) - len(homepage_rankings)}")