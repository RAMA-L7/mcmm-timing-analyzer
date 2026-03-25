import re
import pandas as pd

def parse_mcmm_report(filename):
    results = []

    current_mode = None
    current_corner = None
    current_scenario = None
    current_path = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            # -------------------------
            # Context Tracking
            # -------------------------
            if line.startswith("Mode:"):
                current_mode = line.split("Mode:")[1].strip()

            elif line.startswith("Corner:"):
                current_corner = line.split("Corner:")[1].strip()

            elif line.startswith("Scenario:"):
                current_scenario = line.split("Scenario:")[1].strip()

            # -------------------------
            # Path Start
            # -------------------------
            elif line.startswith("Startpoint:"):
                if current_path:
                    results.append(current_path)

                current_path = {
                    "Mode": current_mode,
                    "Corner": current_corner,
                    "Scenario": current_scenario,
                    "Startpoint": line.split("Startpoint:")[1].strip()
                }

            elif line.startswith("Endpoint:"):
                current_path["Endpoint"] = line.split("Endpoint:")[1].strip()

            elif line.startswith("Path Group:"):
                current_path["Path Group"] = line.split("Path Group:")[1].strip()

            elif line.startswith("Path Type:"):
                current_path["Path Type"] = line.split("Path Type:")[1].strip()

            # -------------------------
            # Timing Data
            # -------------------------
            elif "data arrival time" in line:
                try:
                    current_path["Data Arrival"] = float(line.split()[-1])
                except:
                    current_path["Data Arrival"] = None

            elif "data required time" in line:
                try:
                    current_path["Data Required"] = float(line.split()[-1])
                except:
                    current_path["Data Required"] = None

            elif "slack" in line:
                match = re.search(r"([-]?\d+\.\d+)", line)
                if match:
                    current_path["Slack"] = float(match.group(1))

    if current_path:
        results.append(current_path)

    return pd.DataFrame(results)