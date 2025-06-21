# 🛒 E-Commerce Customer Behavior Analytics Dashboard

This project presents an end-to-end analysis of e-commerce customer behavior using a **synthetic dataset generated via the Faker Python library**. It simulates a realistic e-commerce landscape for advanced data analysis, statistical modeling, and interactive visualization. The project culminates in a **multi-tab, dynamic dashboard built with Python and Dash**, empowering strategic business decision-making.

---

## 📊 Overview

The dataset captures a comprehensive view of e-commerce activity with features such as:

- Customer ID, Age, Gender  
- Purchase Date, Product Category, Product Price, Quantity  
- Payment Method, Returns, Churn Indicator

This provides a **granular and multi-dimensional view of customer behavior** and purchasing trends.

---

## ✨ Key Features

### ✅ End-to-End Data Processing
- Data cleaning and preprocessing
- Outlier detection using IQR method
- Feature normalization and transformation

### 📈 In-Depth Statistical Analysis
- Normality testing with **D'Agostino's K² test**
- Feature transformation using **Box-Cox**
- Dimensionality reduction using **Principal Component Analysis (PCA)**
- Correlation analysis with **Pearson matrices and heatmaps**

### 📊 Rich Data Visualization
- 20+ static plots: heatmaps, pair plots, regression plots, violin plots
- Custom visualizations to explore product trends, pricing, and demographics

### 🧭 Fully Interactive Dashboard (Built with Dash)
A multi-tab **Dash** application with real-time filtering and reporting:

- **Sales Overview**: Analyze trends across product categories and payment methods
- **Customer Insights**: Explore demographics and purchase patterns
- **Payment & Pricing Analysis**: Visualize histograms, bar charts, and distributions
- **Geographic Distribution**: Interactive map of customer data by age and metrics
- **Advanced Visualizations**: Scatter plots, violin plots, and customizable charts
- **Data Table & Export**: Filter and download custom CSVs
- **Custom Report Generator**: Embed visual elements into auto-generated summaries

> 💡 *Tip: Include screenshots of each tab here for better visibility.*

---

## 🧪 Technical Stack

| Category | Tools & Libraries |
|---------|------------------|
| **Data Processing** | `pandas`, `numpy` |
| **Statistical Modeling** | `scipy`, `statsmodels`, `scikit-learn` |
| **Visualization** | `matplotlib`, `seaborn`, `plotly` |
| **Dashboarding** | `dash`, `dash-bootstrap-components` |
| **Synthetic Data Generation** | `faker` |

---

## 🧮 Data Analysis Workflow

### 1. **Data Cleaning & Preprocessing**
- Imputed missing values using:
  - Median (numerical)
  - Mode (categorical)

### 2. **Outlier Removal**
- Applied **Interquartile Range (IQR)** filtering to numerical columns

### 3. **Normality Testing**
- Used **D'Agostino's K-squared test** on key features  
- Applied **Box-Cox transformation** to normalize skewed data (e.g., product price)

### 4. **Feature Analysis**
- Performed **PCA** to retain 95% variance while reducing dimensionality
- Visualized feature relationships with **correlation matrices** and **heatmaps**
