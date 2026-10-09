"""
Amazon India Sales Dashboard
Simple, easy-to-understand management dashboard for non-technical stakeholders.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Amazon India Dashboard | Sapphire IQ",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS for clean, professional look
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main header */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #232F3E;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #565959;
        margin-bottom: 1.5rem;
    }
    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F7F8FA 100%);
        border: 1px solid #E3E6E8;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
        height: 100%;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #565959;
        font-weight: 500;
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.55rem;
        font-weight: 700;
        color: #232F3E;
    }
    .kpi-delta {
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
    /* Section headers */
    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        color: #232F3E;
        border-left: 5px solid #FF9900;
        padding-left: 12px;
        margin: 1.8rem 0 1rem 0;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #232F3E;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #FFFFFF !important;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Data Loading (cached)
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    path = Path(__file__).parent / "Amazon Sales Data India.xlsx"
    df = pd.read_excel(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["MonthName"] = df["Order_Date"].dt.strftime("%b %Y")
    # Ensure numeric
    for col in ["Quantity", "Unit_Price_INR", "Discount_Pct", "Total_Sales_INR", "Profit_INR"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


df = load_data()

# ─────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────
st.sidebar.markdown("## 📦 Amazon India")
st.sidebar.markdown("### Filters")

# Date range
min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()
date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Category filter
categories = sorted(df["Category"].unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
)

# Order Status filter
statuses = sorted(df["Order_Status"].unique())
selected_statuses = st.sidebar.multiselect(
    "Order Status",
    options=statuses,
    default=statuses,
)

# State filter
states = sorted(df["Ship_State"].unique())
selected_states = st.sidebar.multiselect(
    "Ship State",
    options=states,
    default=states,
)

# Apply filters
mask = (
    (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
    & (df["Category"].isin(selected_categories))
    & (df["Order_Status"].isin(selected_statuses))
    & (df["Ship_State"].isin(selected_states))
)
filtered = df.loc[mask].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Records shown:** {len(filtered):,}")
st.sidebar.markdown("Built for Sapphire IQ")


# ─────────────────────────────────────────────
# Helper formatters
# ─────────────────────────────────────────────
def fmt_inr(val):
    """Format large INR values nicely."""
    if abs(val) >= 1e7:
        return f"₹{val/1e7:.2f} Cr"
    if abs(val) >= 1e5:
        return f"₹{val/1e5:.2f} L"
    if abs(val) >= 1e3:
        return f"₹{val/1e3:.1f} K"
    return f"₹{val:,.0f}"


def fmt_num(val):
    return f"{val:,.0f}"


def fmt_pct(val):
    return f"{val:.1f}%"


# Color palette (Amazon-inspired)
COLORS = {
    "orange": "#FF9900",
    "dark": "#232F3E",
    "blue": "#146EB4",
    "green": "#067D62",
    "red": "#B12704",
    "light_orange": "#FFB84D",
    "gray": "#565959",
}
CATEGORY_COLORS = px.colors.qualitative.Set2


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<p class="main-header">📦 Amazon India Sales Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Clear overview of Sales, Profit, Products, Orders, Payment, Fulfilment & Geographic Performance</p>',
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust the filters.")
    st.stop()


# ─────────────────────────────────────────────
# 1) OVERALL SALES & PROFIT PERFORMANCE
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">1) Overall Sales & Profit Performance</p>', unsafe_allow_html=True)

total_sales = filtered["Total_Sales_INR"].sum()
total_profit = filtered["Profit_INR"].sum()
total_orders = filtered["Order_ID"].nunique()
total_units = filtered["Quantity"].sum()
aov = total_sales / total_orders if total_orders > 0 else 0
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

# KPI Row
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">{fmt_inr(total_sales)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Profit</div>
            <div class="kpi-value">{fmt_inr(total_profit)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{fmt_num(total_orders)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with kpi4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Units Sold</div>
            <div class="kpi-value">{fmt_num(total_units)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with kpi5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">{fmt_inr(aov)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with kpi6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Profit Margin %</div>
            <div class="kpi-value">{fmt_pct(profit_margin)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Monthly Trend
monthly = (
    filtered.groupby("YearMonth", as_index=False)
    .agg(
        Sales=("Total_Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Orders=("Order_ID", "nunique"),
    )
    .sort_values("YearMonth")
)

fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

fig_trend.add_trace(
    go.Bar(
        x=monthly["YearMonth"],
        y=monthly["Sales"],
        name="Sales",
        marker_color=COLORS["orange"],
        opacity=0.85,
    ),
    secondary_y=False,
)
fig_trend.add_trace(
    go.Scatter(
        x=monthly["YearMonth"],
        y=monthly["Profit"],
        name="Profit",
        mode="lines+markers",
        line=dict(color=COLORS["blue"], width=3),
        marker=dict(size=6),
    ),
    secondary_y=True,
)

fig_trend.update_layout(
    title="Monthly Sales & Profit Trend",
    height=420,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=60, b=40),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Month",
    hovermode="x unified",
)
fig_trend.update_yaxes(title_text="Sales (₹)", secondary_y=False, gridcolor="#EAEDED")
fig_trend.update_yaxes(title_text="Profit (₹)", secondary_y=True, gridcolor="#EAEDED")
fig_trend.update_xaxes(tickangle=-45, gridcolor="#EAEDED")

st.plotly_chart(fig_trend, use_container_width=True)


# ─────────────────────────────────────────────
# 2) CATEGORY & PRODUCT PERFORMANCE
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">2) Category & Product Performance</p>', unsafe_allow_html=True)

cat_perf = (
    filtered.groupby("Category", as_index=False)
    .agg(
        Sales=("Total_Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Units=("Quantity", "sum"),
        Orders=("Order_ID", "nunique"),
    )
    .sort_values("Sales", ascending=False)
)

col_a, col_b = st.columns(2)

with col_a:
    fig_cat_sales = px.bar(
        cat_perf,
        x="Category",
        y="Sales",
        color="Category",
        color_discrete_sequence=CATEGORY_COLORS,
        title="Category-wise Sales",
        labels={"Sales": "Sales (₹)"},
        text_auto=".2s",
    )
    fig_cat_sales.update_layout(
        height=380,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    fig_cat_sales.update_xaxes(tickangle=-20)
    st.plotly_chart(fig_cat_sales, use_container_width=True)

with col_b:
    fig_cat_profit = px.bar(
        cat_perf,
        x="Category",
        y="Profit",
        color="Category",
        color_discrete_sequence=CATEGORY_COLORS,
        title="Category-wise Profit",
        labels={"Profit": "Profit (₹)"},
        text_auto=".2s",
    )
    fig_cat_profit.update_layout(
        height=380,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    fig_cat_profit.update_xaxes(tickangle=-20)
    st.plotly_chart(fig_cat_profit, use_container_width=True)

# Units + Top Products
col_c, col_d = st.columns(2)

with col_c:
    fig_units = px.pie(
        cat_perf,
        names="Category",
        values="Units",
        title="Category-wise Units Sold",
        color_discrete_sequence=CATEGORY_COLORS,
        hole=0.45,
    )
    fig_units.update_traces(textposition="inside", textinfo="percent+label")
    fig_units.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
    st.plotly_chart(fig_units, use_container_width=True)

with col_d:
    top_products = (
        filtered.groupby("Product", as_index=False)
        .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"), Units=("Quantity", "sum"))
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig_top = px.bar(
        top_products,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Sales",
        color="Sales",
        color_continuous_scale=["#FFE0B2", "#FF9900"],
        labels={"Sales": "Sales (₹)"},
        text_auto=".2s",
    )
    fig_top.update_layout(
        height=380,
        yaxis={"categoryorder": "total ascending"},
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_top, use_container_width=True)


# ─────────────────────────────────────────────
# 3) ORDER STATUS & REVENUE LOSS
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">3) Order Status & Revenue Loss</p>', unsafe_allow_html=True)

status_counts = filtered["Order_Status"].value_counts().reset_index()
status_counts.columns = ["Order_Status", "Count"]

total_for_rate = len(filtered)
delivered = status_counts.loc[status_counts["Order_Status"] == "Delivered", "Count"].sum()
shipped = status_counts.loc[status_counts["Order_Status"] == "Shipped", "Count"].sum()
returned = status_counts.loc[status_counts["Order_Status"] == "Returned", "Count"].sum()
cancelled = status_counts.loc[status_counts["Order_Status"] == "Cancelled", "Count"].sum()

return_rate = (returned / total_for_rate * 100) if total_for_rate > 0 else 0
cancel_rate = (cancelled / total_for_rate * 100) if total_for_rate > 0 else 0

# Status KPIs
s1, s2, s3, s4, s5, s6 = st.columns(6)
with s1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Delivered</div>
            <div class="kpi-value" style="color:#067D62">{fmt_num(delivered)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Shipped</div>
            <div class="kpi-value" style="color:#146EB4">{fmt_num(shipped)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Returned</div>
            <div class="kpi-value" style="color:#B12704">{fmt_num(returned)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Cancelled</div>
            <div class="kpi-value" style="color:#B12704">{fmt_num(cancelled)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Return Rate %</div>
            <div class="kpi-value">{fmt_pct(return_rate)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with s6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Cancellation Rate %</div>
            <div class="kpi-value">{fmt_pct(cancel_rate)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    status_colors = {
        "Delivered": COLORS["green"],
        "Shipped": COLORS["blue"],
        "Returned": COLORS["red"],
        "Cancelled": "#D9782D",
    }
    fig_status = px.pie(
        status_counts,
        names="Order_Status",
        values="Count",
        title="Order Status Distribution",
        color="Order_Status",
        color_discrete_map=status_colors,
        hole=0.4,
    )
    fig_status.update_traces(textposition="inside", textinfo="percent+label")
    fig_status.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_status, use_container_width=True)

with col_f:
    # Category-wise Returns & Cancellations
    loss_df = filtered[filtered["Order_Status"].isin(["Returned", "Cancelled"])]
    if not loss_df.empty:
        cat_loss = (
            loss_df.groupby(["Category", "Order_Status"], as_index=False)
            .size()
            .rename(columns={"size": "Count"})
        )
        fig_loss = px.bar(
            cat_loss,
            x="Category",
            y="Count",
            color="Order_Status",
            barmode="group",
            title="Category-wise Returns & Cancellations",
            color_discrete_map={"Returned": COLORS["red"], "Cancelled": "#D9782D"},
            labels={"Count": "Number of Orders"},
        )
        fig_loss.update_layout(
            height=380,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        fig_loss.update_xaxes(tickangle=-20)
        st.plotly_chart(fig_loss, use_container_width=True)
    else:
        st.info("No returned or cancelled orders in the current filter selection.")


# ─────────────────────────────────────────────
# 4) PAYMENT, FULFILLMENT & GEOGRAPHIC PERFORMANCE
# ─────────────────────────────────────────────
st.markdown(
    '<p class="section-title">4) Payment, Fulfillment & Geographic Performance</p>',
    unsafe_allow_html=True,
)

# Payment Method
pay_perf = (
    filtered.groupby("Payment_Method", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"), Orders=("Order_ID", "nunique"))
    .sort_values("Sales", ascending=False)
)

# Fulfillment
ful_perf = (
    filtered.groupby("Fulfillment", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"), Orders=("Order_ID", "nunique"))
    .sort_values("Sales", ascending=False)
)

col_g, col_h = st.columns(2)

with col_g:
    fig_pay = px.bar(
        pay_perf,
        x="Payment_Method",
        y=["Sales", "Profit"],
        barmode="group",
        title="Sales & Profit by Payment Method",
        color_discrete_map={"Sales": COLORS["orange"], "Profit": COLORS["blue"]},
        labels={"value": "Amount (₹)", "variable": "Metric"},
    )
    fig_pay.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis_title="",
    )
    fig_pay.update_xaxes(tickangle=-25)
    st.plotly_chart(fig_pay, use_container_width=True)

with col_h:
    fig_ful = px.bar(
        ful_perf,
        x="Fulfillment",
        y=["Sales", "Profit"],
        barmode="group",
        title="Sales & Profit by Fulfillment Method",
        color_discrete_map={"Sales": COLORS["orange"], "Profit": COLORS["blue"]},
        labels={"value": "Amount (₹)", "variable": "Metric"},
    )
    fig_ful.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis_title="",
    )
    st.plotly_chart(fig_ful, use_container_width=True)

# Geographic
state_perf = (
    filtered.groupby("Ship_State", as_index=False)
    .agg(
        Sales=("Total_Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Orders=("Order_ID", "nunique"),
        Units=("Quantity", "sum"),
    )
    .sort_values("Sales", ascending=False)
)

st.markdown("#### State-wise Performance")

g1, g2, g3 = st.columns(3)

with g1:
    fig_state_sales = px.bar(
        state_perf,
        x="Sales",
        y="Ship_State",
        orientation="h",
        title="State-wise Sales",
        color="Sales",
        color_continuous_scale=["#B3E5FC", "#146EB4"],
        labels={"Sales": "Sales (₹)", "Ship_State": ""},
        text_auto=".2s",
    )
    fig_state_sales.update_layout(
        height=420,
        yaxis={"categoryorder": "total ascending"},
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_state_sales, use_container_width=True)

with g2:
    fig_state_profit = px.bar(
        state_perf,
        x="Profit",
        y="Ship_State",
        orientation="h",
        title="State-wise Profit",
        color="Profit",
        color_continuous_scale=["#C8E6C9", "#067D62"],
        labels={"Profit": "Profit (₹)", "Ship_State": ""},
        text_auto=".2s",
    )
    fig_state_profit.update_layout(
        height=420,
        yaxis={"categoryorder": "total ascending"},
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_state_profit, use_container_width=True)

with g3:
    fig_state_orders = px.bar(
        state_perf,
        x="Orders",
        y="Ship_State",
        orientation="h",
        title="State-wise Orders",
        color="Orders",
        color_continuous_scale=["#FFE0B2", "#FF9900"],
        labels={"Orders": "Orders", "Ship_State": ""},
        text_auto=True,
    )
    fig_state_orders.update_layout(
        height=420,
        yaxis={"categoryorder": "total ascending"},
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_state_orders, use_container_width=True)

# Optional data table
with st.expander("📋 View State-wise Summary Table"):
    display_state = state_perf.copy()
    display_state["Sales"] = display_state["Sales"].apply(fmt_inr)
    display_state["Profit"] = display_state["Profit"].apply(fmt_inr)
    display_state.columns = ["State", "Sales", "Profit", "Orders", "Units"]
    st.dataframe(display_state, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#565959; font-size:0.9rem;">
        Amazon India Dashboard · Built with Streamlit for Sapphire IQ · Data period: Jan 2024 – Aug 2026
    </div>
    """,
    unsafe_allow_html=True,
)
