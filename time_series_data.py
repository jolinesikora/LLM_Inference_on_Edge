import re
import csv
from datetime import datetime, timedelta
import sys

def parse_datetime(time_str):
    return datetime.strptime(time_str, '%m-%d-%Y %H:%M:%S')

def process_tegrastats(input_file_path, output_csv_path):
    pattern = re.compile(r"(\d\d-\d\d-\d\d\d\d \d\d:\d\d:\d\d) .* VDD_GPU_SOC (\d+)mW.*VDD_CPU_CV (\d+)mW.*VIN_SYS_5V0 (\d+)mW.*VDDQ_VDD2_1V8AO (\d+)mW")
    
    time_series_data = {}
    start_time = None
    interval = timedelta(seconds=30)
    current_interval = None
    total_power = []

    with open(input_file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                time_stamp, gpu_power, cpu_power, sys_power, vdd2_power = match.groups()
                time_stamp = parse_datetime(time_stamp)
                total = int(gpu_power) + int(cpu_power) + int(sys_power) + int(vdd2_power)
                
                if start_time is None:
                    start_time = time_stamp
                    current_interval = start_time + interval

                if time_stamp >= current_interval:
                    if total_power:
                        average_power = sum(total_power) / len(total_power)
                        time_series_data[current_interval.strftime('%m-%d-%Y %H:%M:%S')] = average_power
                    current_interval += interval
                    total_power = []

                total_power.append(total)

        # Handle the last batch if any
        if total_power:
            average_power = sum(total_power) / len(total_power)
            time_series_data[current_interval.strftime('%m-%d-%Y %H:%M:%S')] = average_power

    # Write the results to a CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Time', 'Average Power (mW)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for time_point, avg_power in time_series_data.items():
            writer.writerow({'Time': time_point, 'Average Power (mW)': avg_power})

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file_path> <output_csv_path>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    process_tegrastats(input_file_path, output_csv_path)
