# 📈 Stock Analysis Project

A complete **end-to-end Stock Analysis application** built using **Python, Pandas, Streamlit, and Power BI**. This project focuses on collecting, cleaning, analyzing, and visualizing stock market data to derive meaningful insights for better decision-making.

---

## 🚀 Project Overview

The goal of this project is to:

* Process historical stock market data
* Perform data cleaning and transformation using **Pandas**
* Analyze stock performance (returns, volume, trends)
* Build an **interactive web dashboard** using **Streamlit**
* Create **advanced visual analytics** using **Power BI**

This project is suitable for **data analysis**, **finance analytics**, and **data visualization** learning use cases.

---

## 🛠️ Technologies Used

### 🔹 Programming & Libraries

* **Python 3.x**
* **Pandas** – Data manipulation and analysis
* **NumPy** – Numerical operations
* **Matplotlib / Seaborn** – Data visualization
* **PyYAML** – Reading YAML files

### 🔹 Visualization Tools

* **Streamlit** – Interactive web application
* **Power BI** – Business intelligence dashboards

### 🔹 Data Storage

* CSV files
* YAML files

---

## 📂 Project Structure

```
Stock-Analysis/
│
├── app.py                     # Streamlit application
├── final_output.csv           # Consolidated dataset
├── stockAnalysis.pbix     # Power BI dashboard file
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 📊 Key Features

### ✅ Data Processing (Pandas)

* Handle missing values
* Date parsing and formatting
* Sorting by ticker and date
* Aggregation and grouping

### ✅ Stock Analysis

* Daily & yearly returns
* Green vs Red stock count
* Average price & volume
* Trend analysis
* Correlation between stocks

### ✅ Streamlit Dashboard

* Interactive metrics cards
* Stock price visualizations
* Filters by ticker and date range
* DataFrame preview (index hidden)

### ✅ Power BI Dashboard

* KPI cards (returns, volume)
* Time-series charts
* Comparative stock analysis
* Slicers for dynamic filtering

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/csathishit89/dataDrivenStockAnalysis.git
cd stock-analysis
```

### 2️⃣ Create Virtual Environment (Optional)

```bash
python -m venv env
env\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

## 📈 Power BI Dashboard

1. Open **Power BI Desktop**
2. Load `final_output.csv`
3. Open `powerbi_dashboard.pbix`
4. Refresh data if required

---

## 📌 Sample Insights

* Identified top-performing stocks by yearly return
* Compared green vs red stocks over time
* Observed volume spikes during high volatility
* Correlation between stock price movements

---

## 🔮 Future Enhancements

* Live stock data integration (API)
* Technical indicators (RSI, MACD, Moving Averages)
* Predictive analysis using Machine Learning
* User authentication in Streamlit

---

## 🙌 Acknowledgements

* Yahoo Finance / NSE data sources
* Streamlit documentation
* Power BI community
