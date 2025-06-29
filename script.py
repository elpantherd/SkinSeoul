# 11. Create visualizations to analyze the merchandising system performance

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Create visualization directory
import os
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

# Load and process the dataset
df = pd.read_excel('Mock_Skincare_Dataset.xlsx')

# Calculate key metrics for visualization
df['Profit Margin'] = ((df['Price (USD)'] - df['COGS (USD)']) / df['Price (USD)']) * 100
df['Conversion Rate'] = (df['Volume Sold Last Month'] / df['Views Last Month']) * 100
df['Revenue'] = df['Price (USD)'] * df['Volume Sold Last Month']

# Create a MerchandisingEngine instance to get scores
engine = MerchandisingEngine(TOUCHPOINT_CONFIGS[TouchpointType.HOMEPAGE_CAROUSEL])

# Calculate scores for all products
product_scores = []
for _, row in df.iterrows():
    product = Product(row)
    score = engine.calculate_composite_score(product)
    
    # Calculate individual component scores
    sales_velocity_score = engine.calculate_sales_velocity_score(product)
    profit_margin_score = engine.calculate_profit_margin_score(product)
    inventory_health_score = engine.calculate_inventory_health_score(product)
    brand_tier_score = engine.calculate_brand_tier_score(product)
    engagement_score = engine.calculate_engagement_score(product)
    
    product_scores.append({
        'Product Name': product.name,
        'Brand': product.brand,
        'Brand Tier': product.brand_tier,
        'Price': product.price,
        'Profit Margin': product.profit_margin,
        'Days Inventory': product.days_inventory,
        'Units Stock': product.units_stock,
        'Views': product.views_last_month,
        'Volume Sold': product.volume_sold_last_month,
        'Composite Score': score,
        'Sales Velocity Score': sales_velocity_score,
        'Profit Margin Score': profit_margin_score,
        'Inventory Health Score': inventory_health_score,
        'Brand Tier Score': brand_tier_score,
        'Engagement Score': engagement_score
    })

scores_df = pd.DataFrame(product_scores)

# Apply the same filters as the engine
filtered_df = scores_df.copy()
filter_criteria = engine.config.filter_criteria

filtered_df = filtered_df[
    (filtered_df['Units Stock'] >= filter_criteria.min_stock_units) &
    (filtered_df['Days Inventory'] <= filter_criteria.max_days_inventory) &
    (filtered_df['Profit Margin'] >= filter_criteria.min_profit_margin) &
    (filtered_df['Views'] >= filter_criteria.min_views_threshold)
]

# Sort by composite score
filtered_df = filtered_df.sort_values(by='Composite Score', ascending=False)

# Get the top 20 products (maximum for homepage carousel)
top_products = filtered_df.head(20)

# Convert to CSV file
top_products.to_csv('visualizations/top_merchandised_products.csv', index=False)

# Export the data for charts later
filtered_df.to_csv('visualizations/all_scored_products.csv', index=False)

# Create visualization 1: Brand Tier Distribution in Top Products
plt.figure(figsize=(10, 6))
tier_counts = top_products['Brand Tier'].value_counts().sort_index()
tier_palette = {'A': '#4CAF50', 'B': '#2196F3', 'C': '#FF9800'}

plt.bar(tier_counts.index, tier_counts.values, color=[tier_palette.get(tier, '#999') for tier in tier_counts.index])
plt.title('Brand Tier Distribution in Top 20 Products', fontsize=16)
plt.xlabel('Brand Tier', fontsize=14)
plt.ylabel('Number of Products', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('visualizations/brand_tier_distribution.png', dpi=300, bbox_inches='tight')

# Create visualization 2: Correlation Matrix
correlation_metrics = [
    'Price', 'Profit Margin', 'Days Inventory', 
    'Units Stock', 'Views', 'Volume Sold', 'Composite Score'
]
corr_matrix = filtered_df[correlation_metrics].corr()

plt.figure(figsize=(12, 10))
heatmap = sns.heatmap(
    corr_matrix, 
    annot=True, 
    cmap='coolwarm', 
    fmt='.2f', 
    linewidths=0.5, 
    vmin=-1, 
    vmax=1
)
plt.title('Correlation Matrix of Product Metrics', fontsize=16)
plt.tight_layout()
plt.savefig('visualizations/correlation_matrix.png', dpi=300, bbox_inches='tight')

# Create visualization 3: Top 10 Products and Their Scores
top10 = top_products.head(10)
top10_scores = top10[[
    'Product Name', 'Composite Score', 'Sales Velocity Score',
    'Profit Margin Score', 'Inventory Health Score', 'Brand Tier Score', 'Engagement Score'
]]

plt.figure(figsize=(14, 8))
top10_scores.set_index('Product Name').sort_values('Composite Score').iloc[::-1].plot(
    kind='barh', 
    stacked=True,
    colormap='viridis',
    figsize=(14, 8)
)
plt.title('Score Breakdown for Top 10 Products', fontsize=16)
plt.xlabel('Score Contribution', fontsize=14)
plt.legend(title='Score Components', loc='lower right', frameon=True)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('visualizations/top10_score_breakdown.png', dpi=300, bbox_inches='tight')

# Create visualization 4: Price vs. Score Scatterplot by Brand Tier
plt.figure(figsize=(12, 8))
colors = {'A': '#1b9e77', 'B': '#7570b3', 'C': '#d95f02'}
for tier, group in filtered_df.groupby('Brand Tier'):
    plt.scatter(
        group['Price'], 
        group['Composite Score'], 
        label=f'Tier {tier}',
        color=colors[tier],
        alpha=0.7,
        s=100
    )

plt.title('Price vs. Merchandising Score by Brand Tier', fontsize=16)
plt.xlabel('Price (USD)', fontsize=14)
plt.ylabel('Composite Merchandising Score', fontsize=14)
plt.grid(linestyle='--', alpha=0.7)
plt.legend(title='Brand Tier')
plt.tight_layout()
plt.savefig('visualizations/price_vs_score.png', dpi=300, bbox_inches='tight')

# Create a summary of the visualizations created
print("\n✅ Data Visualizations Created:")
print("   1. Brand Tier Distribution in Top 20 Products (brand_tier_distribution.png)")
print("   2. Correlation Matrix of Product Metrics (correlation_matrix.png)")
print("   3. Score Breakdown for Top 10 Products (top10_score_breakdown.png)")
print("   4. Price vs. Merchandising Score by Brand Tier (price_vs_score.png)")
print("\n✅ Data Files Created:")
print("   1. Top Merchandised Products (top_merchandised_products.csv)")
print("   2. All Scored Products (all_scored_products.csv)")

# Create final results summary
print("\n🔍 Final Analysis Summary:")
print(f"   Total products analyzed: {len(df)}")
print(f"   Products qualifying for homepage carousel: {len(filtered_df)}")
print(f"   Average merchandising score: {filtered_df['Composite Score'].mean():.2f}")
print(f"   Top brand in results: {top_products['Brand'].value_counts().index[0]}")
print(f"   Average price of top 20 products: ${top_products['Price'].mean():.2f}")
print(f"   Percentage of A-tier brands in top 20: {len(top_products[top_products['Brand Tier'] == 'A']) / len(top_products) * 100:.1f}%")
print(f"   Highest scoring product: {top_products.iloc[0]['Product Name']} (Score: {top_products.iloc[0]['Composite Score']:.2f})")
print(f"   Most important score component: {engine.config.scoring_weights.sales_velocity * 100:.0f}% Sales Velocity")