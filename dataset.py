import pandas as pd
from datetime import datetime, timedelta

def generate_enterprise_inventory():
    today = datetime.today()
    
    # 50+ Comprehensive SKUs spanning 12-14 Professional Enterprise Categories
    items = [
        # 1. DAIRY & PERISHABLES
        ("SKU-1001", "Amul Taaza Toned Milk 1L", "Dairy", 45, 100, 70, -3, 1, "Andheri Hub"),
        ("SKU-1002", "Mother Dairy Cow Milk 500ml", "Dairy", 12, 80, 32, -4, 2, "Borivali Hub"),
        ("SKU-1003", "Epigamia Greek Yogurt Blueberry", "Dairy", 18, 40, 120, -10, 4, "Malad Hub"),
        ("SKU-1004", "Amul Butter Block 500g", "Dairy", 120, 50, 275, -20, 25, "Goregaon Hub"),
        ("SKU-1005", "Britannia Cheese Slices 200g", "Dairy", 8, 25, 150, -12, 3, "Navi Mumbai Hub"),

        # 2. BAKERY & BREADS
        ("SKU-2001", "Britannia Brown Bread 400g", "Bakery", 15, 50, 50, -2, 1, "Goregaon Hub"),
        ("SKU-2002", "Modern Whole Wheat Bread", "Bakery", 6, 40, 45, -3, 1, "Navi Mumbai Hub"),
        ("SKU-2003", "Fresh Butter Croissant (Pack of 2)", "Bakery", 4, 20, 90, -1, 1, "Andheri Hub"),
        ("SKU-2004", "Harvest Gold Burger Buns", "Bakery", 22, 30, 40, -2, 3, "Borivali Hub"),

        # 3. PHARMACEUTICALS & HEALTH
        ("SKU-3001", "Dolo 650mg Paracetamol Tablets", "Pharmacy", 450, 150, 30, -90, 365, "Borivali Hub"),
        ("SKU-3002", "Limcee Vitamin C Chewable 500mg", "Pharmacy", 25, 80, 105, -200, 6, "Malad Hub"),
        ("SKU-3003", "Dettol Antiseptic Liquid 500ml", "Pharmacy", 85, 40, 215, -120, 450, "Goregaon Hub"),
        ("SKU-3004", "Volini Pain Relief Spray 100g", "Pharmacy", 14, 50, 290, -150, 8, "Navi Mumbai Hub"),

        # 4. BEVERAGES & JUICES
        ("SKU-4001", "Raw Pressery Cold Pressed Carrot Juice", "Beverages", 12, 40, 110, -5, 2, "Navi Mumbai Hub"),
        ("SKU-4002", "Tropicana 100% Orange Juice 1L", "Beverages", 48, 60, 145, -15, 18, "Andheri Hub"),
        ("SKU-4003", "Beetroot & Apple Health Drink 500ml", "Beverages", 10, 30, 130, -8, 4, "Borivali Hub"),
        ("SKU-4004", "Red Bull Energy Drink 250ml", "Beverages", 220, 80, 125, -60, 300, "Malad Hub"),

        # 5. GROCERIES & STAPLES
        ("SKU-5001", "Fortune Sunlite Sunflower Oil 1L", "Groceries", 210, 100, 145, -30, 240, "Andheri Hub"),
        ("SKU-5002", "Aashirvaad Shuddh Chakki Atta 10kg", "Groceries", 85, 50, 420, -45, 180, "Borivali Hub"),
        ("SKU-5003", "India Gate Basmati Rice 5kg", "Groceries", 130, 60, 550, -90, 500, "Malad Hub"),
        ("SKU-5004", "Tata Salt Vacuum Evaporated 1kg", "Groceries", 500, 200, 28, -100, 700, "Goregaon Hub"),

        # 6. FROZEN FOODS
        ("SKU-6001", "McCain French Fries 1kg", "Frozen", 40, 50, 240, -30, 90, "Borivali Hub"),
        ("SKU-6002", "Godrej Yummiez Chicken Nuggets 500g", "Frozen", 15, 30, 290, -40, 10, "Malad Hub"),
        ("SKU-6003", "Sumeru Frozen Green Peas 1kg", "Frozen", 70, 40, 130, -60, 150, "Goregaon Hub"),

        # 7. ELECTRONICS & HARDWARE
        ("SKU-7001", "ESP32 Wi-Fi + BT Microcontroller Board", "Electronics", 85, 30, 450, -120, 1200, "Andheri Hub"),
        ("SKU-7002", "DS18B20 Waterproof Temp Sensor", "Electronics", 120, 50, 150, -100, 1200, "Borivali Hub"),
        ("SKU-7003", "Analog pH Sensor Module V1.1", "Electronics", 14, 25, 1100, -80, 1200, "Malad Hub"),
        ("SKU-7004", "16x2 I2C LCD Display Module", "Electronics", 95, 40, 220, -150, 1200, "Goregaon Hub"),

        # 8. PERSONAL CARE
        ("SKU-8001", "Dove Cream Beauty Bathing Bar 125g", "Personal Care", 180, 60, 85, -60, 400, "Borivali Hub"),
        ("SKU-8002", "Colgate Strong Teeth Toothpaste 200g", "Personal Care", 250, 80, 115, -90, 500, "Malad Hub"),
        ("SKU-8003", "Himalaya Purifying Neem Face Wash 150ml", "Personal Care", 60, 30, 190, -120, 300, "Andheri Hub"),

        # 9. HOUSEHOLD & CLEANING
        ("SKU-9001", "Surf Excel Easy Wash Detergent Powder 1kg", "Household", 140, 50, 140, -100, 700, "Goregaon Hub"),
        ("SKU-9002", "Vim Dishwash Gel Lemon 500ml", "Household", 90, 40, 120, -70, 360, "Navi Mumbai Hub"),
        ("SKU-9003", "Colin Glass Surface Cleaner Spray 500ml", "Household", 35, 30, 110, -80, 450, "Andheri Hub"),

        # 10. SNACKS & CONFECTIONERY
        ("SKU-10010", "Farmley Roasted Makhana 250g", "Snacks", 180, 60, 199, -45, 150, "Goregaon Hub"),
        ("SKU-10011", "Lays Chips Cream & Onion 50g", "Snacks", 350, 100, 20, -30, 180, "Navi Mumbai Hub"),
        ("SKU-10012", "Haldiram Bhujia Sev 500g", "Snacks", 140, 50, 135, -40, 120, "Andheri Hub"),
        ("SKU-10013", "Cadbury Dairy Milk Silk Chocolate Bar", "Confectionery", 95, 40, 175, -15, 60, "Borivali Hub"),

        # 11. BABY CARE
        ("SKU-11001", "Pampers Active Baby Diapers Medium Pack", "Baby Care", 55, 30, 699, -150, 730, "Malad Hub"),
        ("SKU-11002", "Johnson's Baby Powder 400g", "Baby Care", 70, 25, 230, -200, 900, "Goregaon Hub"),

        # 12. PET CARE
        ("SKU-12001", "Pedigree Adult Dry Dog Food Chicken 3kg", "Pet Care", 25, 15, 850, -60, 365, "Andheri Hub"),
        ("SKU-12002", "Whiskas Adult Wet Cat Food Tuna 85g", "Pet Care", 80, 30, 45, -40, 180, "Borivali Hub"),

        # 13. STATIONERY & OFFICE SUPPLIES
        ("SKU-13001", "Classmate A4 Notebook 300 Pages", "Stationery", 300, 100, 110, -200, 1500, "Malad Hub"),
        ("SKU-13002", "Reynolds Ball Pen Jar (Pack of 25)", "Stationery", 150, 50, 125, -100, 730, "Goregaon Hub"),

        # 14. FITNESS & HEALTH SUPPLEMENTS
        ("SKU-14001", "Optimum Nutrition Gold Standard Whey 1kg", "Fitness", 18, 10, 2899, -180, 730, "Navi Mumbai Hub"),
        ("SKU-14002", "MuscleBlaze Creatine Monohydrate 250g", "Fitness", 35, 15, 699, -120, 500, "Andheri Hub")
    ]
    
    records = []
    for item in items:
        sku, name, cat, qty, reorder, price, mfg_offset, exp_offset, wh = item
        
        mfg_date = today + timedelta(days=mfg_offset)
        exp_date = today + timedelta(days=exp_offset)
        days_to_expiry = (exp_date - today).days
        
        if days_to_expiry <= 3:
            expiry_status = "CRITICAL (Immediate Action)"
        elif days_to_expiry <= 10:
            expiry_status = "WARNING (Near Expiry)"
        else:
            expiry_status = "OPTIMAL (Safe)"
            
        stock_status = "LOW STOCK ALERT" if qty <= reorder else "SUFFICIENT"
        
        records.append({
            "SKU Code": sku,
            "Item Description": name,
            "Category": cat,
            "Stock Quantity": qty,
            "Reorder Level": reorder,
            "Unit Price (INR)": price,
            "Total Inventory Value (INR)": qty * price,
            "Manufacturing Date": mfg_date.strftime('%Y-%m-%d'),
            "Expiry Date": exp_date.strftime('%Y-%m-%d'),
            "Days to Expiry": days_to_expiry,
            "Expiry Risk Level": expiry_status,
            "Stock Level Status": stock_status,
            "Fulfillment Warehouse": wh
        })
        
    return pd.DataFrame(records)
