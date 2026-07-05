import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_data(num_sessions=100000):
    np.random.seed(42)
    random.seed(42)

    devices = ['Desktop', 'Mobile', 'Tablet']
    device_probs = [0.4, 0.5, 0.1]
    
    traffic_sources = ['Organic', 'Paid Ads', 'Social', 'Direct']
    source_probs = [0.4, 0.3, 0.2, 0.1]

    data = []
    
    start_date = datetime(2023, 1, 1)
    
    # Base transition probabilities
    # session_start -> product_view -> add_to_cart -> checkout_initiate -> purchase
    
    for i in range(num_sessions):
        session_id = f"sess_{i:06d}"
        user_id = f"user_{random.randint(10000, 90000)}"
        device = np.random.choice(devices, p=device_probs)
        source = np.random.choice(traffic_sources, p=source_probs)
        
        current_time = start_date + timedelta(days=random.uniform(0, 30), minutes=random.uniform(0, 1440))
        
        # Everyone starts a session
        data.append([session_id, user_id, current_time, 'session_start', device, source])
        
        # Product view: 80% proceed
        if random.random() < 0.8:
            current_time += timedelta(seconds=random.uniform(10, 60))
            data.append([session_id, user_id, current_time, 'product_view', device, source])
            
            # Add to cart: 40% of product viewers proceed
            if random.random() < 0.4:
                current_time += timedelta(seconds=random.uniform(30, 120))
                data.append([session_id, user_id, current_time, 'add_to_cart', device, source])
                
                # Checkout initiate: 50% of add to cart proceed
                if random.random() < 0.5:
                    current_time += timedelta(seconds=random.uniform(15, 60))
                    data.append([session_id, user_id, current_time, 'checkout_initiate', device, source])
                    
                    # Purchase
                    # Injecting the mobile drop-off bug here:
                    if device == 'Mobile':
                        purchase_prob = 0.15 # Massive drop-off
                    else:
                        purchase_prob = 0.60 # Normal conversion
                        
                    if random.random() < purchase_prob:
                        current_time += timedelta(seconds=random.uniform(30, 120))
                        data.append([session_id, user_id, current_time, 'purchase', device, source])
                        
    df = pd.DataFrame(data, columns=['session_id', 'user_id', 'timestamp', 'event_type', 'device_type', 'traffic_source'])
    df.to_csv('ecommerce_events.csv', index=False)
    print(f"Generated {len(df)} events for {num_sessions} sessions in 'ecommerce_events.csv'.")

if __name__ == '__main__':
    generate_data()
