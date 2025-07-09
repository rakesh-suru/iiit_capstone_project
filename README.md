# 📍 Dynamic Pricing for Urban Parking – Model 3: Competitive Pricing

Capstone Project: **Summer Analytics 2025**  
Organized by: Consulting & Analytics Club × Pathway

---

## 📌 Objective

Model 3 introduces **competitive pricing** by incorporating geographic proximity into the pricing algorithm. This model dynamically adjusts parking rates based on the real-time prices of nearby parking lots, along with demand metrics such as occupancy, queue length, traffic, and special day indicators.

---

## 🧠 Logic Summary

### Step 1: Compute Demand
```
Demand = α·(Occupancy / Capacity) + β·QueueLength - γ·Traffic + δ·IsSpecialDay + ε·VehicleTypeWeight
```

### Step 2: Normalize Demand to [-1, 1]  
Then:
```
Price = BasePrice * (1 + λ * NormalizedDemand)
```

### Step 3: Adjust Price Based on Nearby Competitors
- If competitors nearby have **lower prices** and queue is long → **undercut by ₹0.5**
- If competitors are **costlier** and occupancy > 90% → **increase by ₹0.5**
- Else → keep price unchanged

---

## ⚙️ Constants Used

| Parameter         | Value  |
|------------------|--------|
| Base Price       | ₹10.0  |
| Min Multiplier   | 0.5    |
| Max Multiplier   | 2.0    |
| Nearby Radius    | 0.5 km |
| Demand Weights   | α = 0.6, β = 0.15, γ = 0.2, δ = 0.3, ε = 0.1 |
| Price Sensitivity (λ) | 0.8 |

---

## 📈 Features

- 📍 Haversine distance calculation to identify nearby competitors
- 🔁 Dynamic price adjustments based on competition and demand
- 📊 Real-time simulation of price updates
- 📈 Bokeh-based interactive price trend plots
- 📦 Export pricing results to `model3_pricing_results.csv`

---

## 🛠️ How to Run

### 1. Upload your `dataset.csv` to your runtime

Make sure it includes:  
`SystemCodeNumber`, `Occupancy`, `Capacity`, `QueueLength`, `Latitude`, `Longitude`, `TrafficConditionNearby`, `VehicleType`, `IsSpecialDay`, `LastUpdatedDate`, `LastUpdatedTime`

### 2. Open and run the notebook or script:

```bash
Model_3_Competitive_Pricing.ipynb
```

or

```bash
python model3_competitive_pricing.py
```

### 3. View outputs

- Logs of pricing decisions
- Interactive Bokeh plots
- Real-time simulation output
- Output file: `model3_pricing_results.csv`

---

## 📂 Folder Structure

```
📁 dynamic-parking-pricing/
├── dataset.csv
├── model3_competitive_pricing.py
├── Model_3_Competitive_Pricing.ipynb
├── model3_pricing_results.csv
├── README.md
```

---

## 📊 Sample Output Fields

- `SystemCodeNumber`
- `DateTime`
- `OccupancyRate`
- `QueueLength`
- `Price`
- `NearbyCompetitorCount`

---

## 🔁 Previous Models

- ✅ Model 1: Baseline Linear Pricing
- ✅ Model 2: Demand-Based Pricing
- ✅ Model 3: Competitive Pricing (this)

---

## 🧑‍💻 Author

Developed by **[Your Name]**  
Submitted for **Summer Analytics 2025**
