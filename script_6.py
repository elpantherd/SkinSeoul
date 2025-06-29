# 5. Automation and Scheduling System
import threading
import time
from datetime import datetime, timedelta
from typing import Callable, List
import logging

class AutomationScheduler:
    def __init__(self, api: MerchandisingAPI):
        self.api = api
        self.scheduled_tasks = {}
        self.running = False
        self.thread = None
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('MerchandisingAutomation')
    
    def schedule_touchpoint_refresh(self, touchpoint: TouchpointType):
        """Schedule automatic refresh for a touchpoint"""
        config = self.api.engines[touchpoint].config
        refresh_interval = config.refresh_interval_hours
        
        def refresh_task():
            try:
                self.logger.info(f"Auto-refreshing rankings for {touchpoint.value}")
                rankings = self.api.get_rankings(touchpoint, force_refresh=True)
                self.logger.info(f"Successfully refreshed {rankings['total_products']} products for {touchpoint.value}")
                
                # Check for inventory alerts
                self._check_inventory_alerts(touchpoint, rankings)
                
            except Exception as e:
                self.logger.error(f"Failed to refresh {touchpoint.value}: {str(e)}")
        
        self.scheduled_tasks[touchpoint] = {
            'task': refresh_task,
            'interval_hours': refresh_interval,
            'last_run': datetime.min,
            'next_run': datetime.now()
        }
    
    def _check_inventory_alerts(self, touchpoint: TouchpointType, rankings: dict):
        """Check for inventory alerts and log warnings"""
        low_stock_threshold = 20
        high_inventory_threshold = 90
        
        alerts = []
        
        for product_data in rankings['products']:
            if product_data['units_stock'] < low_stock_threshold:
                alerts.append(f"LOW STOCK: {product_data['name']} - {product_data['units_stock']} units")
            
            if product_data['days_inventory'] > high_inventory_threshold:
                alerts.append(f"HIGH INVENTORY: {product_data['name']} - {product_data['days_inventory']} days")
        
        if alerts:
            self.logger.warning(f"Inventory alerts for {touchpoint.value}:")
            for alert in alerts[:5]:  # Show top 5 alerts
                self.logger.warning(f"  {alert}")
    
    def start(self):
        """Start the automation scheduler"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        self.logger.info("Automation scheduler started")
    
    def stop(self):
        """Stop the automation scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.logger.info("Automation scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            current_time = datetime.now()
            
            for touchpoint, task_info in self.scheduled_tasks.items():
                if current_time >= task_info['next_run']:
                    # Run the task
                    task_info['task']()
                    
                    # Schedule next run
                    task_info['last_run'] = current_time
                    task_info['next_run'] = current_time + timedelta(hours=task_info['interval_hours'])
            
            # Sleep for 1 minute before next check
            time.sleep(60)

# 6. Export and Integration System
class ExportManager:
    def __init__(self, api: MerchandisingAPI):
        self.api = api
    
    def export_rankings_json(self, touchpoint: TouchpointType, limit: int = None) -> str:
        """Export rankings as JSON for API integration"""
        rankings = self.api.get_rankings(touchpoint)
        
        if limit:
            rankings['products'] = rankings['products'][:limit]
        
        return json.dumps(rankings, indent=2)
    
    def export_rankings_csv(self, touchpoint: TouchpointType) -> str:
        """Export rankings as CSV for analysis"""
        rankings = self.api.get_rankings(touchpoint)
        
        csv_data = "position,name,brand,brand_tier,price,profit_margin,merchandising_score,units_stock,days_inventory,views_last_month,volume_sold_last_month,is_manual_override\n"
        
        for product in rankings['products']:
            csv_data += f"{product['position']},{product['name']},{product['brand']},{product['brand_tier']},{product['price']},{product['profit_margin']:.2f},{product['merchandising_score']},{product['units_stock']},{product['days_inventory']},{product['views_last_month']},{product['volume_sold_last_month']},{product['is_manual_override']}\n"
        
        return csv_data
    
    def export_frontend_config(self, touchpoint: TouchpointType) -> str:
        """Export configuration for frontend integration"""
        rankings = self.api.get_rankings(touchpoint)
        
        # Create frontend-friendly format
        frontend_config = {
            'touchpoint_id': touchpoint.value,
            'last_updated': rankings['generated_at'],
            'products': []
        }
        
        for product in rankings['products']:
            frontend_config['products'].append({
                'id': f"product_{product['position']}",
                'name': product['name'],
                'brand': product['brand'],
                'price': product['price'],
                'image_url': f"/images/products/{product['name'].lower().replace(' ', '_')}.jpg",
                'product_url': f"/products/{product['name'].lower().replace(' ', '-')}",
                'priority': product['merchandising_score'],
                'is_promoted': product['is_manual_override']
            })
        
        return json.dumps(frontend_config, indent=2)

# 7. Monitoring and Performance Tracking
class PerformanceMonitor:
    def __init__(self, api: MerchandisingAPI):
        self.api = api
        self.metrics_history = {}
        
    def record_performance_metrics(self, touchpoint: TouchpointType):
        """Record performance metrics for analysis"""
        rankings = self.api.get_rankings(touchpoint)
        analytics = self.api.get_analytics_summary(touchpoint)
        
        timestamp = datetime.now().isoformat()
        
        if touchpoint not in self.metrics_history:
            self.metrics_history[touchpoint] = []
        
        metrics = {
            'timestamp': timestamp,
            'total_products': analytics['analytics']['total_products'],
            'total_revenue': analytics['analytics']['total_revenue_last_month'],
            'average_score': analytics['analytics']['average_merchandising_score'],
            'brand_tier_a_count': analytics['analytics']['brand_tier_distribution'].get('A', 0),
            'brand_tier_b_count': analytics['analytics']['brand_tier_distribution'].get('B', 0),
            'brand_tier_c_count': analytics['analytics']['brand_tier_distribution'].get('C', 0),
            'manual_overrides': analytics['analytics']['manual_overrides_count']
        }
        
        self.metrics_history[touchpoint].append(metrics)
        
        # Keep only last 100 records
        if len(self.metrics_history[touchpoint]) > 100:
            self.metrics_history[touchpoint] = self.metrics_history[touchpoint][-100:]
        
        return metrics
    
    def get_performance_report(self, touchpoint: TouchpointType) -> dict:
        """Generate performance report"""
        if touchpoint not in self.metrics_history or not self.metrics_history[touchpoint]:
            return {'error': 'No performance data available'}
        
        history = self.metrics_history[touchpoint]
        latest = history[-1]
        
        # Calculate trends if we have at least 2 data points
        trends = {}
        if len(history) >= 2:
            previous = history[-2]
            trends = {
                'revenue_change': ((latest['total_revenue'] - previous['total_revenue']) / previous['total_revenue'] * 100) if previous['total_revenue'] > 0 else 0,
                'score_change': latest['average_score'] - previous['average_score'],
                'product_count_change': latest['total_products'] - previous['total_products']
            }
        
        return {
            'touchpoint': touchpoint.value,
            'current_metrics': latest,
            'trends': trends,
            'data_points': len(history),
            'generated_at': datetime.now().isoformat()
        }

# Initialize systems
scheduler = AutomationScheduler(api)
export_manager = ExportManager(api)
performance_monitor = PerformanceMonitor(api)

# Test automation system
print("Testing Automation and Export Systems:")
print("=" * 60)

# Schedule automated refreshes
scheduler.schedule_touchpoint_refresh(TouchpointType.HOMEPAGE_CAROUSEL)
scheduler.schedule_touchpoint_refresh(TouchpointType.COLLECTION_PAGE)

print("1. Automation Scheduler:")
print(f"   Scheduled tasks: {len(scheduler.scheduled_tasks)}")
for touchpoint, task_info in scheduler.scheduled_tasks.items():
    print(f"   - {touchpoint.value}: refresh every {task_info['interval_hours']} hours")

# Test exports
print("\n2. Export Manager:")
json_export = export_manager.export_rankings_json(TouchpointType.HOMEPAGE_CAROUSEL, limit=5)
print(f"   JSON export sample (first 200 chars): {json_export[:200]}...")

csv_export = export_manager.export_rankings_csv(TouchpointType.HOMEPAGE_CAROUSEL)
print(f"   CSV export lines: {len(csv_export.split(chr(10)))}")

# Test performance monitoring
print("\n3. Performance Monitor:")
metrics = performance_monitor.record_performance_metrics(TouchpointType.HOMEPAGE_CAROUSEL)
print(f"   Recorded metrics: Revenue=${metrics['total_revenue']:,.2f}, Avg Score={metrics['average_score']:.1f}")

report = performance_monitor.get_performance_report(TouchpointType.HOMEPAGE_CAROUSEL)
print(f"   Performance report generated at: {report['generated_at']}")

print("\n4. System Status:")
print(f"   API cache entries: {len(api.cache)}")
print(f"   Total products loaded: {len(products)}")
print(f"   Active touchpoints: {len(TOUCHPOINT_CONFIGS)}")
print("   System ready for production deployment!")