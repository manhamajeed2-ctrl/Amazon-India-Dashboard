# Amazon India Sales Dashboard

A simple, easy-to-understand management dashboard built with **Streamlit** for Amazon India sales performance.

Designed for non-technical stakeholders (e.g., managers) to quickly understand:

- Overall Sales & Profit Performance  
- Category & Product Performance  
- Order Status & Revenue Loss  
- Payment, Fulfillment & Geographic Performance  

## Features

- **KPI Cards**: Total Sales, Profit, Orders, Units Sold, Average Order Value, Profit Margin %
- **Trend Charts**: Monthly Sales & Profit over time
- **Category Analysis**: Sales, Profit & Units by Category
- **Top Products**: Top 10 products by sales
- **Order Health**: Delivered / Shipped / Returned / Cancelled with rates
- **Payment & Fulfillment**: Contribution by method
- **Geographic Performance**: State-wise Sales, Profit & Orders
- Clean, professional UI with Amazon-inspired color accents

## Data

- **Source**: `Amazon Sales Data India.xlsx` (10,000 orders)
- **Period**: January 2024 – August 2026
- **Categories**: Apparel & Fashion, Beauty & Personal Care, Electronics & Mobiles, Home & Kitchen, Pantry & Groceries

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/amazon-india-dashboard.git
cd amazon-india-dashboard
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

## Project Structure

```
amazon-india-dashboard/
├── app.py                      # Main Streamlit application
├── Amazon Sales Data India.xlsx # Source data
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml             # Optional Streamlit theme config
```

## How to Deploy

### Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select this repository
4. Set main file path to `app.py`
5. Deploy!

### Local / Other platforms

Works on any platform that supports Python + Streamlit (Heroku, Railway, AWS, etc.).

## Business Questions Answered

| Section | Key Question |
|---------|--------------|
| Overall Performance | How is the business performing overall? |
| Category & Product | Which products and categories are driving the business? |
| Order Status | How many orders are successfully completed and how many are being lost? |
| Payment / Fulfillment / Geo | Which payment methods, fulfillment methods and states are generating business? |

## Tech Stack

- **Frontend / App**: Streamlit
- **Charts**: Plotly Express & Graph Objects
- **Data**: Pandas + OpenPyXL
- **Language**: Python 3.9+

## License

This project is for educational / demonstration purposes.

---

Built for **Sapphire IQ** – Amazon India Dashboard project.
