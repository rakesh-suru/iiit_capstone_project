# 🚗 Dynamic Pricing for Urban Parking – Model 2

Capstone Project: **Summer Analytics 2025**  
Organized by: Consulting & Analytics Club × Pathway

---

## 📌 Objective

This project implements **Model 2** of the dynamic pricing engine using a multi-variable **demand function**. The goal is to adjust parking prices in real-time based on demand signals like occupancy rate, queue length, traffic congestion, special events, and vehicle type.

---

## 🧠 Demand Function

We use the following weighted function:

```
Demand = α·(Occupancy / Capacity) + β·QueueLength - γ·Traffic + δ·IsSpecialDay + ε·VehicleTypeWeight
```

### Coefficients:

- α (Occupancy Rate): `0.6`
- β (Queue Length): `0.15`
- γ (Traffic): `0.2` (reduces demand)
- δ (Special Day): `0.3`
- ε (Vehicle Type Weight): `0.1`
- λ (Demand Sensitivity to Price): `0.8`

### Final Price Formula:

```
Price = BasePrice * (1 + λ * NormalizedDemand)
```

Prices are bounded between `$5` and `$20`.

---

## 📈 Features

- Demand-based pricing using:
  - Occupancy Rate
  - Queue Length
  - Traffic Condition
  - Special Day Indicator
  - Vehicle Type
- Demand normalization to smooth price volatility
- Real-time simulation of parking data using `time.sleep()`
- Bokeh-based interactive visualizations
- Comparison with Model 1 (simple linear baseline)
- CSV export of all results

---

## 🛠️ How to Run

### 1. Upload `dataset.csv` to Colab or local project folder

### 2. Open the Notebook or Python file

File: `Model_2_Demand_Based_Pricing.ipynb` (or `model2_full_humanized.py`)

### 3. Run all cells

You will see:

- Print logs for demand normalization and pricing
- Interactive Bokeh plots
- Real-time simulated pricing updates
- A comparison summary with Model 1

---

## 📂 Folder Structure

```
📁 dynamic-parking-pricing/
├── dataset.csv
├── Model_2_Demand_Based_Pricing.ipynb
├── model2_pricing_results.csv
├── README.md
```

---

## 📊 Output

- `model2_pricing_results.csv`: Pricing history per time step and parking lot
- Real-time pricing updates printed
- Demand + Price trends visualized per parking lot

---

## 🔁 Coming Next

- ✅ Model 1 (Baseline) [completed]
- ✅ Model 2 (Demand-Based) [this repo]
- 🔜 Model 3 (Competitive Pricing with GPS proximity)

---

## 🧑‍💻 Author

Developed by **[Your Name]**  
Submitted for **Summer Analytics 2025**
