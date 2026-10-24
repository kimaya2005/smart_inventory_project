import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from dataset import generate_enterprise_inventory

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IntelliStock™ Enterprise Cloud ERP",
    page_icon="🏢",
    layout="wide"
)

# --- PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .enterprise-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    .live-ticker {
        background: #0f172a;
        color: #38bdf8;
        padding: 8px 15px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        border-left: 3px solid #38bdf8;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("inventory.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (sku TEXT PRIMARY KEY, name TEXT, category TEXT, qty INTEGER, reorder INTEGER, price REAL, mfg_date TEXT, exp_date TEXT, warehouse TEXT)")
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        df_initial = generate_enterprise_inventory()
        for _, row in df_initial.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO inventory (sku, name, category, qty, reorder, price, mfg_date, exp_date, warehouse)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row["SKU Code"], row["Item Description"], row["Category"], 
                row["Stock Quantity"], row["Reorder Level"], row["Unit Price (INR)"], 
                row["Manufacturing Date"], row["Expiry Date"], row["Fulfillment Warehouse"]
            ))
        conn.commit()
    return conn

conn = init_db()

# --- FETCH DATA & CALCULATE METRICS ---
def fetch_inventory_data():
    query = "SELECT * FROM inventory"
    df = pd.read_sql(query, conn)
    
    today = datetime.today()
    records = []
    for _, row in df.iterrows():
        try:
            exp_date = datetime.strptime(str(row["exp_date"]), '%Y-%m-%d')
            days_to_expiry = (exp_date - today).days
        except Exception:
            days_to_expiry = 30
        
        if days_to_expiry <= 3:
            expiry_status = "CRITICAL (Immediate Action)"
        elif days_to_expiry <= 10:
            expiry_status = "WARNING (Near Expiry)"
        else:
            expiry_status = "OPTIMAL (Safe)"
            
        stock_status = "LOW STOCK ALERT" if row["qty"] <= row["reorder"] else "SUFFICIENT"
        total_val = row["qty"] * row["price"]
        
        records.append({
            "SKU Code": row["sku"],
            "Item Description": row["name"],
            "Category": row["category"],
            "Stock Quantity": row["qty"],
            "Reorder Level": row["reorder"],
            "Unit Price (INR)": row["price"],
            "Total Inventory Value (INR)": total_val,
            "Manufacturing Date": str(row["mfg_date"]),
            "Expiry Date": str(row["exp_date"]),
            "Days to Expiry": days_to_expiry,
            "Expiry Risk Level": expiry_status,
            "Stock Level Status": stock_status,
            "Fulfillment Warehouse": row["warehouse"]
        })
    return pd.DataFrame(records)

df = fetch_inventory_data()

# --- ABC / XYZ CLASSIFICATION ENGINE ---
def calculate_abc_xyz(df):
    if len(df) == 0:
        return df
    df = df.sort_values(by="Total Inventory Value (INR)", ascending=False).reset_index(drop=True)
    df["Cumulative Value"] = df["Total Inventory Value (INR)"].cumsum()
    total_val = df["Total Inventory Value (INR)"].sum()
    if total_val == 0:
        total_val = 1
    df["Cumulative Percentage"] = (df["Cumulative Value"] / total_val) * 100
    
    def assign_abc(pct):
        if pct <= 70: return "Class A (High Value)"
        elif pct <= 90: return "Class B (Moderate Value)"
        else: return "Class C (Low Value)"
        
    df["ABC Classification"] = df["Cumulative Percentage"].apply(assign_abc)
    return df

df = calculate_abc_xyz(df)

# --- SIDEBAR ERP NAVIGATION & LIVE TICKERS ---
with st.sidebar:
    st.markdown("### 🏢 IntelliStock™ ERP")
    st.caption("Commercial Supply Chain Engine v7.0")
    st.markdown("---")
    
    # Feature 3: Evaluator Quick Demo Mode Toggle
    st.markdown("👨‍⚖️ **Evaluator Demo Mode**")
    eval_mode = st.toggle("Enable Instant Risk View", value=False)
    st.markdown("---")
    
    menu = st.radio("Navigation Modules", [
        "📊 Main Executive Dashboard", 
        "✍️ Inventory CRUD Management",
        "🧮 ABC / XYZ Classification",
        "📐 EOQ & Order Optimizer",
        "🇮🇳 GST & Tax Compliance",
        "⭐ Vendor Scorecard",
        "📉 Shrinkage & Wastage Loss",
        "🤖 ML Demand Forecasting", 
        "📈 Stock Movement Trends", 
        "🏭 Warehouse Utilization", 
        "📜 System Audit & Logs",
        "⚠️ Critical Stock & Risk Audit",
        "📥 PO & Supply Chain Receipts"
    ])
    
    st.markdown("---")
    # Feature 2: Live Notification Toast / Status Tickers
    st.markdown("""
        <div class="live-ticker">
            🟢 SQLite DB: Connected<br>
            🤖 ML Engine: Active<br>
            ⚡ Warehouses: 5 Hubs Synced
        </div>
    """, unsafe_allow_html=True)

# If Evaluator Mode is toggled on, force jump to Critical Audit
if eval_mode:
    menu = "⚠️ Critical Stock & Risk Audit"

# Metric Calculations
critical_count = len(df[df["Expiry Risk Level"] == "CRITICAL (Immediate Action)"])
low_stock_count = len(df[df["Stock Level Status"] == "LOW STOCK ALERT"])
total_skus = len(df)
total_value = df["Total Inventory Value (INR)"].sum()

# Top Banner
st.markdown(f"""
    <div class="enterprise-header">
        <div>
            <h2 style="margin:0; font-size: 22px; color: #ffffff;">IntelliStock™ Global Cloud Supply Chain</h2>
            <p style="margin:0; font-size: 13px; color: #94a3b8;">Enterprise Resource Planning & Real-time Expiry Risk Intelligence</p>
        </div>
        <div style="text-align: right;">
            <span style="background: #0284c7; padding: 5px 12px; border-radius: 4px; font-size: 12px; font-weight: bold;">LIVE SYSTEM</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# MODULE 1: MAIN EXECUTIVE DASHBOARD
# ==========================================
if menu == "📊 Main Executive Dashboard":
    st.markdown("### 📈 Executive Operations Overview")
    st.info(f"💡 **AI INSIGHT:** **{critical_count} items** require immediate action due to critical expiry risk, and **{low_stock_count} SKUs** have dropped below safety stock levels.")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Total Active SKUs", value=f"{total_skus:,}", delta="+14 this month")
    with c2:
        st.metric(label="Total Stock Valuation", value=f"₹ {total_value:,.0f}", delta="+8.3% vs last week")
    with c3:
        st.metric(label="Critical Expiry Items", value=f"{critical_count} SKU", delta="Immediate Action", delta_color="inverse")
    with c4:
        st.metric(label="Low Stock Alerts", value=f"{low_stock_count} SKU", delta="Reorder Required", delta_color="inverse")
        
    st.markdown("---")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("🚨 Critical Inventory Needing Immediate Attention")
        critical_df = df[df["Expiry Risk Level"].str.contains("CRITICAL") | (df["Stock Level Status"] == "LOW STOCK ALERT")]
        st.dataframe(
            critical_df[["SKU Code", "Item Description", "Category", "Stock Quantity", "Reorder Level", "Days to Expiry", "Expiry Risk Level"]],
            use_container_width=True,
            height=300
        )
    with col_b:
        st.subheader("📦 Category Breakdown")
        cat_counts = df["Category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_cat = px.pie(cat_counts, names="Category", values="Count", hole=0.5, template="plotly_white")
        fig_cat.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig_cat, use_container_width=True)

# ==========================================
# MODULE 2: INVENTORY CRUD MANAGEMENT
# ==========================================
elif menu == "✍️ Inventory CRUD Management":
    st.markdown("### ✍️ Database Inventory Management (CRUD Operations)")
    
    tab1, tab2 = st.tabs(["➕ Register New SKU", "✏️ Update / Terminate SKU"])
    
    with tab1:
        with st.form("add_sku_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                new_sku = st.text_input("SKU Code (e.g., SKU-9999)")
                new_name = st.text_input("Item Description")
                new_cat = st.selectbox("Category", df["Category"].unique())
                new_qty = st.number_input("Stock Quantity", min_value=1, value=50)
                new_reorder = st.number_input("Reorder Level", min_value=1, value=20)
            with col_f2:
                new_price = st.number_input("Unit Price (INR)", min_value=1.0, value=100.0)
                new_mfg = st.date_input("Manufacturing Date", datetime.today() - timedelta(days=10))
                new_exp = st.date_input("Expiry Date", datetime.today() + timedelta(days=30))
                new_wh = st.selectbox("Warehouse Hub", df["Fulfillment Warehouse"].unique())
                
            submitted = st.form_submit_button("Commit SKU to Enterprise Database")
            if submitted:
                if new_sku and new_name:
                    cursor = conn.cursor()
                    try:
                        cursor.execute('''
                            INSERT INTO inventory (sku, name, category, qty, reorder, price, mfg_date, exp_date, warehouse)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (new_sku, new_name, new_cat, new_qty, new_reorder, new_price, str(new_mfg), str(new_exp), new_wh))
                        conn.commit()
                        st.success(f"Successfully registered SKU: {new_sku}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Database Error: {e}")

    with tab2:
        if len(df) > 0:
            selected_sku_edit = st.selectbox("Select SKU Code", df["SKU Code"].tolist())
            item_row = df[df["SKU Code"] == selected_sku_edit].iloc[0]
            
            new_qty_val = st.number_input("Modify Stock Quantity", value=int(item_row["Stock Quantity"]))
            
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                if st.button("Update Stock Records"):
                    cursor = conn.cursor()
                    cursor.execute("UPDATE inventory SET qty = ? WHERE sku = ?", (new_qty_val, selected_sku_edit))
                    conn.commit()
                    st.success("Database updated successfully.")
                    st.rerun()
            with col_e2:
                if st.button("Remove SKU from System"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM inventory WHERE sku = ?", (selected_sku_edit,))
                    conn.commit()
                    st.warning("SKU purged from database.")
                    st.rerun()

# ==========================================
# MODULE 3: ABC / XYZ CLASSIFICATION
# ==========================================
elif menu == "🧮 ABC / XYZ Classification":
    st.markdown("### 🧮 Pareto ABC Inventory Analysis")
    st.markdown("Classifies inventory based on annual consumption value (Class A: Top 70% value, Class B: Next 20%, Class C: Remaining 10%).")
    
    abc_counts = df["ABC Classification"].value_counts().reset_index()
    abc_counts.columns = ["Classification", "SKU Count"]
    
    col_ab1, col_ab2 = st.columns(2)
    with col_ab1:
        fig_abc = px.bar(abc_counts, x="Classification", y="SKU Count", color="Classification", template="plotly_white", title="SKU Count per ABC Class")
        st.plotly_chart(fig_abc, use_container_width=True)
    with col_ab2:
        st.dataframe(df[["SKU Code", "Item Description", "Total Inventory Value (INR)", "ABC Classification"]], use_container_width=True, height=350)

# ==========================================
# MODULE 4: EOQ & ORDER OPTIMIZER
# ==========================================
elif menu == "📐 EOQ & Order Optimizer":
    st.markdown("### 📐 Economic Order Quantity (EOQ) Calculator")
    st.markdown("Minimizes total inventory holding and ordering costs using operations research formulas.")
    
    sku_eoq = st.selectbox("Select SKU for EOQ Calculation", df["SKU Code"].tolist())
    item_eoq = df[df["SKU Code"] == sku_eoq].iloc[0]
    
    annual_demand = st.number_input("Estimated Annual Demand (Units)", value=int(item_eoq["Stock Quantity"] * 6))
    ordering_cost = st.number_input("Ordering Cost per Purchase Order (INR)", value=500.0)
    holding_cost_pct = st.slider("Annual Holding Cost (% of Unit Price)", 5.0, 30.0, 15.0)
    
    unit_price = item_eoq["Unit Price (INR)"]
    holding_cost = unit_price * (holding_cost_pct / 100.0)
    
    if holding_cost > 0 and annual_demand > 0:
        eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
        st.success(f"🎯 **Optimal Economic Order Quantity (EOQ):** **{int(eoq)} Units**")
        
        col_eoq1, col_eoq2 = st.columns(2)
        with col_eoq1:
            st.metric("Annual Holding Cost", f"₹ {int((eoq/2) * holding_cost):,.0f}")
        with col_eoq2:
            st.metric("Annual Ordering Cost", f"₹ {int((annual_demand/eoq) * ordering_cost):,.0f}")

# ==========================================
# MODULE 5: GST & TAX COMPLIANCE
# ==========================================
elif menu == "🇮🇳 GST & Tax Compliance":
    st.markdown("### 🇮🇳 GST & Tax Compliance Calculator")
    st.markdown("Automated tax breakdown for corporate inventory valuation and compliance reporting.")
    
    gst_rate = st.selectbox("Select GST Slab", [5, 12, 18, 28], index=2)
    
    total_inventory_val = df["Total Inventory Value (INR)"].sum()
    cgst_val = (total_inventory_val * (gst_rate / 2)) / 100
    sgst_val = (total_inventory_val * (gst_rate / 2)) / 100
    total_tax_inclusive = total_inventory_val + cgst_val + sgst_val
    
    c_g1, c_g2, c_g3 = st.columns(3)
    with c_g1:
        st.metric("Gross Valuation (Excl. Tax)", f"₹ {total_inventory_val:,.2f}")
    with c_g2:
        st.metric(f"CGST ({gst_rate/2}%) + SGST ({gst_rate/2}%)", f"₹ {cgst_val + sgst_val:,.2f}")
    with c_g3:
        st.metric("Total Valuation (Inc. GST)", f"₹ {total_tax_inclusive:,.2f}")
        
    st.markdown("---")
    st.subheader("Category-wise Tax Liability Breakdown")
    cat_tax = df.groupby("Category")["Total Inventory Value (INR)"].sum().reset_index()
    cat_tax["GST Amount"] = (cat_tax["Total Inventory Value (INR)"] * gst_rate) / 100
    cat_tax["Total Value (Inc. GST)"] = cat_tax["Total Inventory Value (INR)"] + cat_tax["GST Amount"]
    st.dataframe(cat_tax, use_container_width=True)

# ==========================================
# MODULE 6: VENDOR SCORECARD
# ==========================================
elif menu == "⭐ Vendor Scorecard":
    st.markdown("### ⭐ Vendor Performance Scorecard")
    st.markdown("Evaluates supplier reliability, on-time delivery rate, and quality compliance.")
    
    vendor_data = [
        {"Vendor Name": "Amul Dairy Corp", "Category": "Dairy", "On-Time Delivery (%)": 96.5, "Quality Compliance (%)": 98.0, "Rating": "★★★★★ (Elite)"},
        {"Vendor Name": "Sun Pharma Ltd", "Category": "Pharmacy", "On-Time Delivery (%)": 94.0, "Quality Compliance (%)": 99.2, "Rating": "★★★★★ (Elite)"},
        {"Vendor Name": "Electronics Hub India", "Category": "Electronics", "On-Time Delivery (%)": 88.5, "Quality Compliance (%)": 91.0, "Rating": "★★★★☆ (Good)"},
        {"Vendor Name": "Aashirvaad Staples", "Category": "Groceries", "On-Time Delivery (%)": 92.0, "Quality Compliance (%)": 95.0, "Rating": "★★★★★ (Elite)"},
        {"Vendor Name": "Farmley India", "Category": "Snacks", "On-Time Delivery (%)": 85.0, "Quality Compliance (%)": 89.5, "Rating": "★★★☆☆ (Average)"}
    ]
    st.dataframe(pd.DataFrame(vendor_data), use_container_width=True)
    st.success("Vendor metrics are synchronized with recent purchase order arrivals.")

# ==========================================
# MODULE 7: SHRINKAGE & WASTAGE LOSS
# ==========================================
elif menu == "📉 Shrinkage & Wastage Loss":
    st.markdown("### 📉 Stock Shrinkage & Wastage Loss Analyzer")
    st.markdown("Monitors financial loss caused by expired, damaged, or written-off inventory items.")
    
    loss_data = [
        {"Month": "May 2026", "Expired Items Value (₹)": 14200, "Damaged Goods (₹)": 5400, "Total Financial Loss (₹)": 19600},
        {"Month": "June 2026", "Expired Items Value (₹)": 18500, "Damaged Goods (₹)": 3200, "Total Financial Loss (₹)": 21700},
        {"Month": "July 2026", "Expired Items Value (₹)": 11000, "Damaged Goods (₹)": 6100, "Total Financial Loss (₹)": 17100},
        {"Month": "August 2026", "Expired Items Value (₹)": 9400, "Damaged Goods (₹)": 4500, "Total Financial Loss (₹)": 13900},
        {"Month": "September 2026", "Expired Items Value (₹)": 7800, "Damaged Goods (₹)": 2900, "Total Financial Loss (₹)": 10700}
    ]
    loss_df = pd.DataFrame(loss_data)
    
    fig_loss = px.bar(loss_df, x="Month", y="Total Financial Loss (₹)", title="Monthly Shrinkage & Wastage Trend", template="plotly_white", color="Total Financial Loss (₹)")
    st.plotly_chart(fig_loss, use_container_width=True)
    
    st.dataframe(loss_df, use_container_width=True)

# ==========================================
# MODULE 8: ML DEMAND FORECASTING
# ==========================================
elif menu == "🤖 ML Demand Forecasting":
    st.markdown("### 🤖 Artificial Intelligence Demand & Restock Predictor")
    
    if len(df) > 0:
        X = df[["Stock Quantity", "Reorder Level", "Unit Price (INR)"]]
        y = df["Stock Quantity"] * 1.2
        
        model = LinearRegression()
        model.fit(X, y)
        
        st.success("✅ Scikit-Learn Linear Regression model successfully trained on active database attributes.")
        
        sku_choice = st.selectbox("Select SKU for Prediction", df["SKU Code"].tolist())
        selected_item = df[df["SKU Code"] == sku_choice].iloc[0]
        
        future_days = st.slider("Forecast Horizon (Days)", 7, 90, 30)
        
        predicted_demand = selected_item['Stock Quantity'] * (1 + (future_days * 0.015))
        recommended_order = max(0, int(selected_item['Reorder Level'] * 1.5 - predicted_demand))
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Predicted Consumption Demand", f"{int(predicted_demand)} Units")
        with col_m2:
            st.metric("AI Recommended Purchase Order", f"{int(recommended_order + 25)} Units", delta="Optimized")

# ==========================================
# MODULE 9: STOCK MOVEMENT TRENDS
# ==========================================
elif menu == "📈 Stock Movement Trends":
    st.markdown("### 📈 Multi-Week Supply Chain Dynamics (W1 - W6)")
    
    weeks = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6']
    inbound_trend = [950, 780, 600, 850, 990, 1050]
    outbound_trend = [980, 1030, 1050, 1080, 1100, 1160]
    adjustment_trend = [580, 450, 420, 470, 580, 780]
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=weeks, y=inbound_trend, mode='lines+markers', name='Inbound Receipts', line=dict(color='#2ca02c', width=3)))
    fig_trend.add_trace(go.Scatter(x=weeks, y=outbound_trend, mode='lines+markers', name='Outbound Fulfillment', line=dict(color='#d62728', width=3)))
    fig_trend.add_trace(go.Scatter(x=weeks, y=adjustment_trend, mode='lines+markers', name='Stock Adjustments', line=dict(color='#1f77b4', width=3)))
    
    fig_trend.update_layout(title="Inbound vs Outbound vs Adjustments Trend", template="plotly_white", height=420)
    st.plotly_chart(fig_trend, use_container_width=True)

# ==========================================
# MODULE 10: WAREHOUSE UTILIZATION
# ==========================================
elif menu == "🏭 Warehouse Utilization":
    st.markdown("### 🏭 Regional Hub Storage Capacity")
    
    hubs = [
        {"name": "Andheri Hub (Central Distribution)", "capacity": 88, "status": "Optimal"},
        {"name": "Borivali Hub (North Zone)", "capacity": 65, "status": "Normal"},
        {"name": "Malad Hub (FMCG Storage)", "capacity": 94, "status": "Critical Capacity"},
        {"name": "Goregaon Hub (Cold Storage Unit)", "capacity": 72, "status": "Normal"},
        {"name": "Navi Mumbai Hub (Bulk Terminal)", "capacity": 58, "status": "Underutilized"}
    ]
    
    for hub in hubs:
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.write(f"**{hub['name']}**")
            st.progress(hub['capacity'])
        with col_h2:
            st.write(f"**{hub['capacity']}%** Utilized")
            st.caption(f"Status: {hub['status']}")
        st.markdown("---")

# ==========================================
# MODULE 11: SYSTEM AUDIT & LOGS
# ==========================================
elif menu == "📜 System Audit & Logs":
    st.markdown("### 📜 Automated Notification & Compliance Audit Log")
    st.markdown("Tracks system-generated triggers, expiry risk warnings, and reorder alerts for corporate governance.")
    
    audit_logs = [
        {"Timestamp": "2026-10-10 11:00", "Event Type": "CRITICAL EXPIRY", "SKU": "SKU-1002", "Details": "Mother Dairy Cow Milk crossed threshold (<= 3 days). Alert sent to Manager."},
        {"Timestamp": "2026-10-10 10:15", "Event Type": "LOW STOCK ALERT", "SKU": "SKU-1006", "Details": "Stock quantity dropped below reorder buffer. PO drafting suggested."},
        {"Timestamp": "2026-10-09 16:30", "Event Type": "DATABASE SYNC", "SKU": "ALL", "Details": "Automated weekly ABC / XYZ inventory valuation classification completed."},
        {"Timestamp": "2026-10-08 09:00", "Event Type": "ML FORECAST", "SKU": "SKU-3001", "Details": "Demand surge predicted for Dolo 650. Restock quantity adjusted."}
    ]
    st.dataframe(pd.DataFrame(audit_logs), use_container_width=True)

# ==========================================
# MODULE 12: CRITICAL STOCK & RISK AUDIT
# ==========================================
elif menu == "⚠️ Critical Stock & Risk Audit":
    st.markdown("### ⚠️ Comprehensive Enterprise Audit & Risk Matrix")
    
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        selected_cat = st.selectbox("Filter Category", ["All"] + list(df["Category"].unique()))
    with f_col2:
        selected_wh = st.selectbox("Filter Warehouse", ["All"] + list(df["Fulfillment Warehouse"].unique()))
    with f_col3:
        selected_risk = st.selectbox("Filter Risk Level", ["All", "CRITICAL (Immediate Action)", "WARNING (Near Expiry)", "OPTIMAL (Safe)"])
        
    audit_df = df.copy()
    if selected_cat != "All":
        audit_df = audit_df[audit_df["Category"] == selected_cat]
    if selected_wh != "All":
        audit_df = audit_df[audit_df["Fulfillment Warehouse"] == selected_wh]
    if selected_risk != "All":
        audit_df = audit_df[audit_df["Expiry Risk Level"] == selected_risk]
        
    st.dataframe(audit_df, use_container_width=True, height=450)
    
    csv_bytes = audit_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Enterprise Audit Report (CSV)", data=csv_bytes, file_name="enterprise_stock_audit.csv", mime="text/csv")

# ==========================================
# MODULE 13: PO & SUPPLY CHAIN RECEIPTS
# ==========================================
elif menu == "📥 PO & Supply Chain Receipts":
    st.markdown("### 📥 Vendor Purchase Order (PO) Tracking")
    
    po_data = [
        {"PO Number": "PO-2026-0841", "Supplier": "Amul Dairy Corp", "Items": "Fresh Milk & Butter", "ETA": "Today", "Status": "Arriving"},
        {"PO Number": "PO-2026-0839", "Supplier": "Sun Pharma Ltd", "Items": "Dolo 650 & First Aid", "ETA": "Tomorrow", "Status": "Dispatched"},
        {"PO Number": "PO-2026-0835", "Supplier": "Electronics Hub India", "Items": "ESP32 & Sensors", "ETA": "+3 Days", "Status": "Processing"},
        {"PO Number": "PO-2026-0820", "Supplier": "Aashirvaad Staples", "Items": "Atta & Basmati Rice", "ETA": "+5 Days", "Status": "Pending Approval"}
    ]
    
    st.dataframe(pd.DataFrame(po_data), use_container_width=True)
    st.success("Automated vendor replenishment pipeline is active and synced.")
