# 📦 MODEL 3 – Competitive Pricing Based on Location
# Summer Analytics 2025 – Consulting & Analytics Club × Pathway

import pandas as pd
import numpy as np
import pathway as pw
from bokeh.plotting import figure, show, output_notebook
from bokeh.layouts import gridplot
import time
import math

# Activate Bokeh for Colab/Notebook
output_notebook()

# Load dataset
print("📥 Loading dataset...")
df = pd.read_csv("dataset.csv")

# Constants
BASE_PRICE = 10.0
MAX_MULTIPLIER = 2.0
MIN_MULTIPLIER = 0.5
ALPHA = 0.6
BETA = 0.15
GAMMA = 0.2
DELTA = 0.3
EPSILON = 0.1
LAMBDA = 0.8
DISTANCE_THRESHOLD = 0.5  # km

# --- Helper Functions ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def encode_traffic(level):
    return {'low': 0.2, 'average': 0.5, 'high': 0.8}.get(level.lower(), 0.5)

def encode_vehicle(vtype):
    return {'car': 1.0, 'truck': 1.5, 'bike': 0.7, 'cycle': 0.3}.get(vtype.lower(), 1.0)

def compute_demand(occ, queue, traffic, special, vtype_weight):
    return (ALPHA * occ + BETA * queue - GAMMA * traffic + DELTA * special + EPSILON * vtype_weight)

def normalize(values):
    min_v, max_v = np.min(values), np.max(values)
    if max_v == min_v:
        return np.zeros_like(values)
    return 2 * (values - min_v) / (max_v - min_v) - 1

def compute_price(norm_demand):
    price = BASE_PRICE * (1 + LAMBDA * norm_demand)
    return np.clip(price, BASE_PRICE * MIN_MULTIPLIER, BASE_PRICE * MAX_MULTIPLIER)

# --- Model 3 Logic ---
def run_model3(df):
    df_sorted = df.sort_values(['LastUpdatedDate', 'LastUpdatedTime']).reset_index(drop=True)
    all_demands = []

    # Step 1: Compute demand
    for _, row in df_sorted.iterrows():
        occ = row['Occupancy'] / row['Capacity'] if row['Capacity'] > 0 else 0
        demand = compute_demand(occ, row['QueueLength'], encode_traffic(row['TrafficConditionNearby']),
                                row['IsSpecialDay'], encode_vehicle(row['VehicleType']))
        all_demands.append(demand)

    norm_demand = normalize(np.array(all_demands))

    results = []
    for idx, row in df_sorted.iterrows():
        occ = row['Occupancy'] / row['Capacity'] if row['Capacity'] > 0 else 0
        base_price = compute_price(norm_demand[idx])

        lat, lon = row['Latitude'], row['Longitude']
        this_id = row['SystemCodeNumber']

        # Nearby competitors
        nearby_prices = []
        for _, comp in df_sorted.iterrows():
            if comp['SystemCodeNumber'] == this_id:
                continue
            dist = haversine(lat, lon, comp['Latitude'], comp['Longitude'])
            if dist <= DISTANCE_THRESHOLD:
                comp_occ = comp['Occupancy'] / comp['Capacity'] if comp['Capacity'] > 0 else 0
                comp_demand = compute_demand(comp_occ, comp['QueueLength'], encode_traffic(comp['TrafficConditionNearby']),
                                             comp['IsSpecialDay'], encode_vehicle(comp['VehicleType']))
                comp_price = compute_price(normalize(np.array([comp_demand]))[0])
                nearby_prices.append(comp_price)

        # Adjust based on competition
        if nearby_prices:
            avg_nearby = np.mean(nearby_prices)
            if avg_nearby < base_price and row['QueueLength'] > 3:
                final_price = avg_nearby - 0.5  # undercut
            elif avg_nearby > base_price and occ > 0.9:
                final_price = base_price + 0.5  # increase slightly
            else:
                final_price = base_price
        else:
            final_price = base_price

        final_price = np.clip(final_price, BASE_PRICE * MIN_MULTIPLIER, BASE_PRICE * MAX_MULTIPLIER)

        results.append({
            'ID': row['ID'],
            'SystemCodeNumber': this_id,
            'DateTime': f"{row['LastUpdatedDate']} {row['LastUpdatedTime']}",
            'OccupancyRate': occ,
            'QueueLength': row['QueueLength'],
            'RawDemand': all_demands[idx],
            'NormalizedDemand': norm_demand[idx],
            'Latitude': lat,
            'Longitude': lon,
            'Price': final_price,
            'NearbyCompetitorCount': len(nearby_prices)
        })

        if idx % 100 == 0:
            print(f"📍 Processed {idx} rows...")

    return pd.DataFrame(results)

# Run the model
model3_df = run_model3(df)
print("✅ Model 3 complete.")

# --- Visualization ---
def plot_model3_results():
    print("📊 Creating Bokeh visualizations...")
    plots = []
    for lot in model3_df['SystemCodeNumber'].unique()[:3]:
        data = model3_df[model3_df['SystemCodeNumber'] == lot].copy()
        data['TimeIndex'] = range(len(data))

        p = figure(title=f"Pricing Trend – {lot}", width=400, height=300,
                   x_axis_label="Time Step", y_axis_label="Price ($)")
        p.line(data['TimeIndex'], data['Price'], line_color='blue', legend_label='Price', line_width=2)
        p.line(data['TimeIndex'], data['OccupancyRate'] * 20, line_color='orange',
               legend_label='Occupancy ×20', alpha=0.6)
        p.legend.location = 'top_left'
        plots.append(p)

    show(gridplot([plots]))

plot_model3_results()

# --- Real-Time Simulation ---
def simulate_real_time_model3():
    print("🕒 Starting real-time simulation for Model 3...")
    lot_id = model3_df['SystemCodeNumber'].iloc[0]
    data = model3_df[model3_df['SystemCodeNumber'] == lot_id].head(10)

    for _, row in data.iterrows():
        time.sleep(0.3)
        print(f"[{row['DateTime']}] Occ: {row['OccupancyRate']:.1%}, Queue: {row['QueueLength']}, "
              f"💲 Price: ${row['Price']:.2f}, 🧭 Nearby: {row['NearbyCompetitorCount']}")

simulate_real_time_model3()

# --- Save results ---
model3_df.to_csv("model3_pricing_results.csv", index=False)
print("💾 Saved as 'model3_pricing_results.csv'")
