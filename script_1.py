# Create the main merchandising system architecture

# 1. Data Models and Core Classes
class Product:
    def __init__(self, product_data):
        self.name = product_data['Product Name']
        self.brand = product_data['Brand']
        self.brand_tier = product_data['Brand Tier']
        self.price = float(product_data['Price (USD)'])
        self.cogs = float(product_data['COGS (USD)'])
        self.days_inventory = int(product_data['Days of Inventory'])
        self.units_stock = int(product_data['Units in Stock'])
        self.views_last_month = int(product_data['Views Last Month'])
        self.volume_sold_last_month = int(product_data['Volume Sold Last Month'])
        
        # Calculated metrics
        self.profit_margin = ((self.price - self.cogs) / self.price) * 100 if self.price > 0 else 0
        self.conversion_rate = (self.volume_sold_last_month / self.views_last_month * 100) if self.views_last_month > 0 else 0
        self.revenue_last_month = self.volume_sold_last_month * self.price
        self.sell_through_rate = (self.volume_sold_last_month / (self.units_stock + self.volume_sold_last_month) * 100) if (self.units_stock + self.volume_sold_last_month) > 0 else 0
        
    def to_dict(self):
        return {
            'name': self.name,
            'brand': self.brand,
            'brand_tier': self.brand_tier,
            'price': self.price,
            'cogs': self.cogs,
            'profit_margin': self.profit_margin,
            'conversion_rate': self.conversion_rate,
            'revenue_last_month': self.revenue_last_month,
            'sell_through_rate': self.sell_through_rate,
            'days_inventory': self.days_inventory,
            'units_stock': self.units_stock,
            'views_last_month': self.views_last_month,
            'volume_sold_last_month': self.volume_sold_last_month
        }

# Initialize products from dataset
products = []
for _, row in df.iterrows():
    products.append(Product(row))

print(f"Loaded {len(products)} products")
print("Sample product metrics:")
sample_product = products[0]
print(f"Product: {sample_product.name}")
print(f"Profit Margin: {sample_product.profit_margin:.2f}%")
print(f"Conversion Rate: {sample_product.conversion_rate:.2f}%")
print(f"Revenue Last Month: ${sample_product.revenue_last_month:.2f}")
print(f"Sell-through Rate: {sample_product.sell_through_rate:.2f}%")