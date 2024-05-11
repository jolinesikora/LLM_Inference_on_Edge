import re

file_path = 'stats_gpt.txt'

averages = {
    "VDD_GPU_SOC": {"sum": 0, "count": 0},
    "VDD_CPU_CV": {"sum": 0, "count": 0},
    "VIN_SYS_5V0": {"sum": 0, "count": 0},
    "VDDQ_VDD2_1V8AO": {"sum": 0, "count": 0}
}

patterns = {
    "VDD_GPU_SOC": re.compile(r"VDD_GPU_SOC (\d+)mW"),
    "VDD_CPU_CV": re.compile(r"VDD_CPU_CV (\d+)mW"),
    "VIN_SYS_5V0": re.compile(r"VIN_SYS_5V0 (\d+)mW"),
    "VDDQ_VDD2_1V8AO": re.compile(r"VDDQ_VDD2_1V8AO (\d+)mW")
}

with open(file_path, 'r') as file:
    for line in file:
        for key, pattern in patterns.items():
            match = pattern.search(line)
            if match:
                value = int(match.group(1))
                averages[key]["sum"] += value
                averages[key]["count"] += 1

total_power_sum = 0
total_power_count = 0

results = {}
for key, stats in averages.items():
    if stats["count"] > 0:
        average = stats["sum"] / stats["count"]
    else:
        average = 0
    results[key] = average
    total_power_sum += stats["sum"]
    total_power_count += stats["count"]

total_average_power = total_power_sum / total_power_count if total_power_count > 0 else 0

print(results, total_average_power)
