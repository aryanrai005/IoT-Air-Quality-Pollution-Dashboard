import os
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION INTERFACE ---
CSV_FILE_PATH = "data/sensor_logs.csv"
OUTPUT_CHART_PATH = "outputs/air_quality_trends.png"
OUTPUT_REPORT_PATH = "reports/sample_air_quality_report.txt"

# Ensure our output directory assets exist safely
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("reports", exist_ok=True)

def generate_analytics_dashboard():
    print("=================================================================")
    print("       ANALYSING PERSISTENT AIR QUALITY DATABASE REGISTRY        ")
    print("=================================================================")
    
    # 1. Verification and Safe Fallback Check
    if not os.path.isfile(CSV_FILE_PATH) or os.stat(CSV_FILE_PATH).st_size == 0:
        print(f"[ERROR] Database file not found or empty at: {CSV_FILE_PATH}")
        print("Please run 'python python_simulation/simulation.py' first to generate logs.")
        return

    # 2. Data Ingestion & Cleansing Phase
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        expected_columns = [
            'Timestamp',
            'Air_Quality_PPM',
            'Temperature_C',
            'Humidity_Pct',
            'Air_Category',
            'Alert_Status'
        ]

        if 'Timestamp' not in df.columns:
            if df.shape[1] >= len(expected_columns):
                df = pd.read_csv(CSV_FILE_PATH, header=None, names=expected_columns)
            else:
                raise ValueError('CSV file has an unexpected column structure.')

        # Ensure timestamp strings are parsed into functional date-time index arrays
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    except Exception as e:
        print(f"[CRITICAL] Failed to parse transaction metrics cleanly: {str(e)}")
        return

    total_records = len(df)
    print(f"[SUCCESS] Ingested {total_records} continuous sensor transactions.")

    # 3. Statistical Calculations Engine
    avg_gas = round(df['Air_Quality_PPM'].mean(), 1)
    max_gas = df['Air_Quality_PPM'].max()
    avg_temp = round(df['Temperature_C'].mean(), 1)
    avg_hum = round(df['Humidity_Pct'].mean(), 1)
    
    # Extract distribution breakdown percentages
    category_counts = df['Air_Category'].value_counts()
    category_percentages = df['Air_Category'].value_counts(normalize=True) * 100

    # 4. Generate Professional Text Summary Report
    with open(OUTPUT_REPORT_PATH, mode='w', encoding='utf-8') as f:
        f.write("=========================================================\n")
        f.write("      ENVIRONMENTAL METRICS COMPLIANCE AUDIT REPORT      \n")
        f.write("=========================================================\n")
        f.write(f"Report Generated On : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Logged Windows: {total_records} active entries\n\n")
        f.write("--- CRITICAL HISTORICAL SUMMARY STATISTICS ---\n")
        f.write(f" Mean Atmospheric Gas Loading : {avg_gas} PPM\n")
        f.write(f" Absolute Peak Pollution Surge: {max_gas} PPM\n")
        f.write(f" Thermal Arithmetic Baseline  : {avg_temp} °C\n")
        f.write(f" Moisture Saturation Baseline : {avg_hum} %\n\n")
        f.write("--- AIR QUALITY SAFETY DISTRIBUTION ---\n")
        for cat, pct in category_percentages.items():
            count = category_counts[cat]
            f.write(f" -> Status Class '{cat}': {pct:.1f}% ({count} records)\n")
        f.write("=========================================================\n")

    print(f"[SUCCESS] Compiled environmental validation report at: {OUTPUT_REPORT_PATH}")

    # 5. Data Visualization Suite via Matplotlib
    # Set up a structured 2x1 canvas grid layout
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=False)
    fig.suptitle("IoT Air Quality Monitoring Network Real-Time Trends Dashboard", fontsize=14, fontweight='bold')

    # Chart 1: Chronological Gas Loading Plot with Threshold Baseline Grid Lines
    ax1.plot(df['Timestamp'], df['Air_Quality_PPM'], color='#2c3e50', linewidth=2, marker='o', markersize=4, label='Gas Density (PPM)')
    ax1.axhline(y=150, color='#2ecc71', linestyle='--', alpha=0.7, label='Good/Safe Cap (<150)')
    ax1.axhline(y=300, color='#f1c40f', linestyle='--', alpha=0.7, label='Moderate Cap (<300)')
    ax1.axhline(y=700, color='#e74c3c', linestyle='--', alpha=0.7, label='Hazardous Floor (>700)')
    
    ax1.set_title("Gas Density Fluctuations Over Time Axis", fontsize=11, fontweight='bold')
    ax1.set_ylabel("Concentration Levels (PPM)", fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', fontsize=8)
    ax1.tick_params(axis='x', rotation=15, labelsize=9)

    # Chart 2: Secondary Multi-Axis Thermal and Moisture Trends Plot
    ax2.plot(df['Timestamp'], df['Temperature_C'], color='#e67e22', linewidth=1.8, linestyle='-', label='Temperature (°C)')
    ax2.set_ylabel("Ambient Temperature (°C)", color='#e67e22', fontsize=10)
    ax2.tick_params(axis='y', labelcolor='#e67e22')
    
    # Instantiate duplicate twin x-axis overlaying the exact grid
    ax3 = ax2.twinx()
    ax3.plot(df['Timestamp'], df['Humidity_Pct'], color='#3498db', linewidth=1.8, linestyle=':', label='Humidity (%)')
    ax3.set_ylabel("Relative Humidity (%)", color='#3498db', fontsize=10)
    ax3.tick_params(axis='y', labelcolor='#3498db')

    ax2.set_title("Correlated Ambient Temperature & Humidity Profiles", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    # Gather legends from both merged axes layers seamlessly
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax2.legend(lines2 + lines3, labels2 + labels3, loc='upper right', fontsize=8)
    ax2.tick_params(axis='x', rotation=15, labelsize=9)

    plt.tight_layout()
    # Export rendering out safely to static visual PNG format file
    plt.savefig(OUTPUT_CHART_PATH, dpi=300)
    plt.close()
    
    print(f"[SUCCESS] Graphical dashboard trend chart exported to: {OUTPUT_CHART_PATH}")
    print("=================================================================")

if __name__ == "__main__":
    generate_analytics_dashboard()
