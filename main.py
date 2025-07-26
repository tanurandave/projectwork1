import json
from datetime import datetime


# Helper function: Convert ISO 8601 timestamp to milliseconds
def iso_to_millis(iso_string):
    """
    Converts an ISO timestamp string (e.g., '2025-07-26T10:15:30Z') to milliseconds since epoch.
    """
    dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ")
    return int(dt.timestamp() * 1000)


# IMPLEMENT: Transform Format 1 (data-1.json) to the unified format
def transform_data1(data):
    """
    Converts data from format 1 (data-1.json) to the unified format (data-result.json).
    Expected format:
    {
        "device": "sensor-1",
        "timestamp": "2025-07-26T10:15:30Z",
        "reading": 123.45
    }
    Output format:
    {
        "deviceId": "sensor-1",
        "timestamp": 1753521330000,
        "value": 123.45
    }
    """
    return {
        "deviceId": data["device"],
        "timestamp": iso_to_millis(data["timestamp"]),
        "value": data["reading"]
    }


# IMPLEMENT: Transform Format 2 (data-2.json) to the unified format
def transform_data2(data):
    """
    Converts data from format 2 (data-2.json) to the unified format (data-result.json).
    Expected format:
    {
        "id": "sensor-2",
        "time": 1753521330000,
        "val": 98.76
    }
    Output format:
    {
        "deviceId": "sensor-2",
        "timestamp": 1753521330000,
        "value": 98.76
    }
    """
    return {
        "deviceId": data["id"],
        "timestamp": data["time"],
        "value": data["val"]
    }


# DO NOT EDIT BELOW THIS LINE
# ---------------------------


def main():
    # Load the input files
    with open("data-1.json") as f1, open("data-2.json") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Transform both inputs into the unified format
    result1 = transform_data1(data1)
    result2 = transform_data2(data2)

    # Combine results into a list
    combined_result = [result1, result2]

    # Output the result in JSON format
    with open("result.json", "w") as outfile:
        json.dump(combined_result, outfile, indent=4)


if __name__ == "__main__":
    main()
