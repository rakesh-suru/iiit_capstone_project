# 📦 MODEL 2 – Demand-Based Dynamic Pricing (Humanized Full Version)
# Summer Analytics 2025 – Consulting & Analytics Club × Pathway

import pandas as pd
import numpy as np
import pathway as pw
from bokeh.plotting import figure, show, output_notebook
from bokeh.layouts import gridplot
from bokeh.io import push_notebook
import time

# Enable Bokeh for notebook output
output_notebook()

# 🧾 Load dataset
print("📥 Loading dataset...")
df = pd.read_csv('dataset.csv')

# 🔧 Pricing Constants
BASE_PRICE = 10.0
MAX_MULTIPLIER = 2.0
MIN_MULTIPLIER = 0.5

# 🧠 Demand Function Coefficients
ALPHA = 0.6      # Occupancy rate
BETA = 0.15      # Queue length
GAMMA = 0.2      # Traffic (negative)
DELTA = 0.3      # Special day
EPSILON = 0.1    # Vehicle type
LAMBDA = 0.8     # Demand-to-price sensitivity

# 🔤 Encoding helpers
def encode_traffic(traffic):
    return {'low': 0.2, 'average': 0.5, 'high': 0.8}.get(traffic.lower(), 0.5)

def encode_vehicle_type(vtype):
    return {'car': 1.0, 'truck': 1.5, 'bike': 0.7, 'cycle': 0.3}.get(vtype.lower(), 1.0)

# 🧮 Demand calculation
def compute_demand(occ, queue, traffic, special, vweight):
    return (ALPHA * occ + BETA * queue - GAMMA * traffic + DELTA * special + EPSILON * vweight)

# 🔃 Normalize demand to [-1, 1]
def normalize_demand(values):
    min_val, max_val = np.min(values), np.max(values)
    if max_val == min_val:
        return np.zeros_like(values)
    return 2 * (values - min_val) / (max_val - min_val) - 1

# 💰 Final price calculation
def calculate_price(demand):
    raw = BASE_PRICE * (1 + LAMBDA * demand)
    return max(BASE_PRICE * MIN_MULTIPLIER, min(BASE_PRICE * MAX_MULTIPLIER, raw))

# 🧪 Model 2 execution
def run_model2(df):
    df_sorted = df.sort_values(['SystemCodeNumber', 'LastUpdatedDate', 'LastUpdatedTime']).reset_index(drop=True)
    all_demands = []

    for _, row in df_sorted.iterrows():
        occ_rate = row['Occupancy'] / row['Capacity'] if row['Capacity'] > 0 else 0
        demand = compute_demand(
            occ_rate,
            row['QueueLength'],
            encode_traffic(row['TrafficConditionNearby']),
            row['IsSpecialDay'],
            encode_vehicle_type(row['VehicleType'])
        )
        all_demands.append(demand)

    normalized = normalize_demand(np.array(all_demands))

    results = []
    for idx, row in df_sorted.iterrows():
        occ_rate = row['Occupancy'] / row['Capacity'] if row['Capacity'] > 0 else 0
        price = calculate_price(normalized[idx])
        results.append({
            'ID': row['ID'],
            'SystemCodeNumber': row['SystemCodeNumber'],
            'DateTime': f"{row['LastUpdatedDate']} {row['LastUpdatedTime']}",
            'OccupancyRate': occ_rate,
            'QueueLength': row['QueueLength'],
            'TrafficCondition': row['TrafficConditionNearby'],
            'IsSpecialDay': row['IsSpecialDay'],
            'VehicleType': row['VehicleType'],
            'RawDemand': all_demands[idx],
            'NormalizedDemand': normalized[idx],
            'Price': price,
            'PriceMultiplier': price / BASE_PRICE
        })

        if idx % 100 == 0:
            print(f"🔄 Processed {idx} records...")

    return pd.DataFrame(results)

# ▶️ Run model
pricing_results = run_model2(df)
print("✅ Model 2 complete.")

# 📊 Visualization
def plot_model2_results():
    print("📊 Generating Bokeh visualizations...")
    plots = []
    spaces = pricing_results['SystemCodeNumber'].unique()[:4]

    for space in spaces:
        data = pricing_results[pricing_results['SystemCodeNumber'] == space].copy().reset_index(drop=True)
        data['TimeIndex'] = range(len(data))

        p = figure(title=f"Price Trend – {space}", x_axis_label='Time Step', y_axis_label='Price ($)', width=400, height=300)
        p.line(data['TimeIndex'], data['Price'], line_color='blue', line_width=2, legend_label='Price')
        p.line(data['TimeIndex'], (data['NormalizedDemand'] + 1) * 5 + 5, line_color='red', alpha=0.7, legend_label='Scaled Demand')
        p.line([0, len(data)], [BASE_PRICE, BASE_PRICE], line_dash='dashed', color='green', legend_label='Base Price')
        p.legend.location = 'top_left'
        plots.append(p)

    grid = gridplot([plots[i:i + 2] for i in range(0, len(plots), 2)])
    show(grid)

plot_model2_results()

# 🕒 Real-time simulation
def simulate_real_time():
    print("🕒 Starting real-time simulation...")
    space = pricing_results['SystemCodeNumber'].iloc[0]
    data = pricing_results[pricing_results['SystemCodeNumber'] == space].head(10)

    current_price = BASE_PRICE
    for _, row in data.iterrows():
        time.sleep(0.3)
        new_price = calculate_price(row['NormalizedDemand'])
        print(f"[{row['DateTime']}] Occupancy: {row['OccupancyRate']:.1%} | Queue: {row['QueueLength']} | "
              f"Traffic: {row['TrafficCondition']} | Vehicle: {row['VehicleType']} → 💲${new_price:.2f}")
        current_price = new_price

simulate_real_time()

# 📉 Comparison with Model 1
def compare_model1():
    print("📊 Comparing Model 2 vs Model 1...")
    baseline = []
    current_price = BASE_PRICE
    for _, row in pricing_results.iterrows():
        current_price += 5.0 * row['OccupancyRate']
        current_price = max(BASE_PRICE * MIN_MULTIPLIER, min(BASE_PRICE * MAX_MULTIPLIER, current_price))
        baseline.append(current_price)

    pricing_results['Model1_Price'] = baseline
    pricing_results['Price_Difference'] = pricing_results['Price'] - pricing_results['Model1_Price']
    avg_diff = pricing_results['Price_Difference'].mean()
    print(f"Average Price Difference (Model 2 - Model 1): ${avg_diff:.2f}")

compare_model1()

# 💾 Save results
pricing_results.to_csv("model2_pricing_results.csv", index=False)
print("💾 File saved: model2_pricing_results.csv")
