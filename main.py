import os
import subprocess
import sys
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION INTERFACE ---
CSV_FILE_PATH = "data/sensor_logs.csv"
OUTPUT_CHART_PATH = "outputs/air_quality_trends.png"
OUTPUT_REPORT_PATH = "reports/sample_air_quality_report.txt"
SIMULATION_SCRIPT_PATH = "python_simulation/simulation.py"

# Ensure our output directory assets exist safely
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("reports", exist_ok=True)

def run_live_simulation():
    """Launches the sub-process telemetry environmental simulator."""
    print("\n[LAUNCHING] Starting Virtual Environmental Sensor Simulation Core...")
    if not os.path.isfile(SIMULATION_SCRIPT_PATH):
        print(f"[ERROR] Could not find the simulation engine script at: {SIMULATION_SCRIPT_PATH}")
        return
    try:
        # Executes the separate simulation script directly inside this console window
        subprocess.run([sys.executable, SIMULATION_SCRIPT_PATH], check=True)
    except KeyboardInterrupt:
        print("\n[INFO] Returned to Master Control Hub menu.")

def generate_analytics_dashboard():
    """Parses data metrics and exports text summaries along with graphical trends charts."""
    print("\n=================================================================")
    print("       ANALYSING PERSISTENT AIR QUALITY DATABASE REGISTRY        ")
    print("=================================================================")
    
    if not os.path.isfile(CSV_FILE_PATH) or os.stat(CSV_FILE_PATH).st_size == 0:
        print(f"[ERROR] Database file not found or empty at: {CSV_FILE_PATH}")
        print("Please run the live simulation profile first to populate sensor transactions.")
        return

    try:
        df = pd.read_csv(CSV_FILE_PATH)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    except Exception as e:
        print(f"[CRITICAL] Failed to parse transaction metrics cleanly: {str(e)}")
        return

    total_records = len(df)
    print(f"[SUCCESS] Ingested {total_records} continuous sensor transactions.")

    # Statistical Calculations Engine
    avg_gas = round(df['Air_Quality_PPM'].mean(), 1)
    max_gas = df['Air_Quality_PPM'].max()
    avg_temp = round(df['Temperature_C'].mean(), 1)
    avg_hum = round(df['Humidity_Pct'].mean(), 1)
    
    category_percentages = df['Air_Category'].value_counts(normalize=True) * 100
    category_counts = df['Air_Category'].value_counts()

    # Generate Professional Text Summary Report
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

    # Data Visualization Suite via Matplotlib
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7))
    fig.suptitle("IoT Air Quality Monitoring Network Real-Time Trends Dashboard", fontsize=14, fontweight='bold')

    ax1.plot(df['Timestamp'], df['Air_Quality_PPM'], color='#2c3e50', linewidth=2, marker='o', markersize=4, label='Gas Density (PPM)')
    ax1.axhline(y=150, color='#2ecc71', linestyle='--', alpha=0.7, label='Good Cap (<150)')
    ax1.axhline(y=300, color='#f1c40f', linestyle='--', alpha=0.7, label='Mod Cap (<300)')
    ax1.axhline(y=700, color='#e74c3c', linestyle='--', alpha=0.7, label='Haz Floor (>700)')
    ax1.set_title("Gas Density Fluctuations Over Time Axis", fontsize=11, fontweight='bold')
    ax1.set_ylabel("Concentration Levels (PPM)", fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', fontsize=8)

    ax2.plot(df['Timestamp'], df['Temperature_C'], color='#e67e22', linewidth=1.8, label='Temperature (°C)')
    ax2.set_ylabel("Ambient Temperature (°C)", color='#e67e22', fontsize=10)
    ax2.tick_params(axis='y', labelcolor='#e67e22')
    
    ax3 = ax2.twinx()
    ax3.plot(df['Timestamp'], df['Humidity_Pct'], color='#3498db', linewidth=1.8, linestyle=':', label='Humidity (%)')
    ax3.set_ylabel("Relative Humidity (%)", color='#3498db', fontsize=10)
    ax3.tick_params(axis='y', labelcolor='#3498db')

    ax2.set_title("Correlated Ambient Temperature & Humidity Profiles", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax2.legend(lines2 + lines3, labels2 + labels3, loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART_PATH, dpi=300)
    plt.close()
    
    print(f"[SUCCESS] Graphical dashboard trend chart exported to: {OUTPUT_CHART_PATH}")
    print("=================================================================")

def main():
    while True:
        print("\n=========================================================")
        print("  IoT AIR QUALITY MONITORING NETWORK MASTER ENTRY CONTROL ")
        print("=========================================================")
        print("1. [RUN] Launch Live Interactive Environmental Simulation Loop")
        print("2. [ANALYSE] Process Local Database and Generate Graphical Charts")
        print("3. [EXIT] Terminate Active Terminal Session")
        print("=========================================================")
        
        choice = input("Enter selection value [1-3]: ").strip()
        
        if choice == '1':
            run_live_simulation()
        elif choice == '2':
            generate_analytics_dashboard()
        elif choice == '3':
            print("\nShutting down master terminal control hub. Goodbye!")
            break
        else:
            print("\n[INVALID INPUT] Please select an option between 1 and 3.")

if __name__ == "__main__":
    main()
