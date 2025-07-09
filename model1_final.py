#Model 1 – Baseline Linear Dynamic Pricing Model
#Capstone Project – Summer Analytics 2025 (Consulting & Analytics Club × Pathway)

#Importing Libraries
import pandas as pd
import numpy as np
import time
from bokeh.plotting import figure, show, output_notebook
from bokeh.layouts import gridplot
from bokeh.io import push_notebook

#Enable Bokeh in notebook
output_notebook()

#Load Dataset
df = pd.read_csv("dataset.csv")

#Configuration Parameters
BASE_PRICE = 10.0  # Base price in $
ALPHA = 5.0        # Sensitivity to occupancy rate
MAX_MULTIPLIER = 2.0
MIN_MULTIPLIER = 0.5

#Dataset Summary
print("Dataset Overview:")
print(f"Total Records: {len(df)}")
print(f"Unique Parking Spaces: {df['SystemCodeNumber'].nunique()}")
print(f"Date Range: {df['LastUpdatedDate'].min()} to {df['LastUpdatedDate'].max()}")
print(df.head())

#Utility Function: Calculate Occupancy Rate
def calculate_occupancy_rate(occupancy, capacity):
    return occupancy / capacity if capacity > 0 else 0

#Pricing Logic: Baseline Linear Model
def model1_pricing(previous_price, occupancy_rate, alpha=ALPHA):
    adjustment = alpha * occupancy_rate
    new_price = previous_price + adjustment
    return max(BASE_PRICE * MIN_MULTIPLIER, min(BASE_PRICE * MAX_MULTIPLIER, new_price))

#Core Function: Process Dynamic Pricing
def process_parking_data(df):
    df_sorted = df.sort_values(['SystemCodeNumber', 'LastUpdatedDate', 'LastUpdatedTime']).reset_index(drop=True)
    pricing_results = []
    current_prices = {space: BASE_PRICE for space in df_sorted['SystemCodeNumber'].unique()}

    for idx, row in df_sorted.iterrows():
        space_id = row['SystemCodeNumber']
        occ = row['Occupancy']
        cap = row['Capacity']
        rate = calculate_occupancy_rate(occ, cap)
        prev_price = current_prices[space_id]
        new_price = model1_pricing(prev_price, rate)
        current_prices[space_id] = new_price

        pricing_results.append({
            'ID': row['ID'],
            'SystemCodeNumber': space_id,
            'DateTime': f"{row['LastUpdatedDate']} {row['LastUpdatedTime']}",
            'Occupancy': occ,
            'Capacity': cap,
            'OccupancyRate': rate,
            'PreviousPrice': prev_price,
            'NewPrice': new_price,
            'PriceChange': new_price - prev_price,
            'VehicleType': row['VehicleType'],
            'TrafficCondition': row['TrafficConditionNearby'],
            'QueueLength': row['QueueLength']
        })

        if idx % 100 == 0:
            print(f"Processed {idx} records...")

    return pd.DataFrame(pricing_results)

#Run Pricing Model
results = process_parking_data(df)

#Summary
print("\n--- Pricing Summary ---")
print(f"Records Processed: {len(results)}")
print(f"Avg Price: ${results['NewPrice'].mean():.2f}")
print(f"Price Range: ${results['NewPrice'].min():.2f} to ${results['NewPrice'].max():.2f}")

#Visualize Results
def create_visualizations(pricing_df):
    print("\nCreating Bokeh visualizations...")
    unique_spaces = pricing_df['SystemCodeNumber'].unique()[:4]
    plots = []

    for space in unique_spaces:
        space_data = pricing_df[pricing_df['SystemCodeNumber'] == space].copy()
        space_data['TimeIndex'] = range(len(space_data))

        p = figure(title=f"Price Trend – {space}", x_axis_label="Time Step", y_axis_label="Price ($)", width=400, height=300)
        p.line(space_data['TimeIndex'], space_data['NewPrice'], color='blue', line_width=2, legend_label="Price")
        p.line(space_data['TimeIndex'], space_data['OccupancyRate'] * 20, color='red', line_width=1, alpha=0.7, legend_label="Occupancy ×20")
        p.line([0, len(space_data)], [BASE_PRICE, BASE_PRICE], color="green", line_dash="dashed", legend_label="Base Price")
        p.legend.location = "top_left"
        plots.append(p)

    grid = gridplot([plots[i:i+2] for i in range(0, len(plots), 2)])
    show(grid)

#Display the plots
create_visualizations(results)

#Simulate Real-Time Stream
def simulate_real_time(df):
    print("\n🔁 Real-Time Pricing Simulation")
    demo_space = df['SystemCodeNumber'].iloc[0]
    sample = df[df['SystemCodeNumber'] == demo_space].head(10)
    current_price = BASE_PRICE

    for idx, row in sample.iterrows():
        time.sleep(0.3)
        new_price = model1_pricing(current_price, row['OccupancyRate'])
        print(f"[{row['DateTime']}] Occupancy: {row['OccupancyRate']:.2%}, Price: ${current_price:.2f} → ${new_price:.2f}")
        current_price = new_price

simulate_real_time(results)

#Save output
results.to_csv("model1_pricing_results.csv", index=False)
print("\n✅ Model 1 Pricing Results Saved!")
