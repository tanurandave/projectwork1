import json
from datetime import datetime


def iso_to_millis(iso_string):
    """
    Converts an ISO timestamp string to milliseconds since epoch.
    Handles both formats: '2025-07-26T10:15:30Z' and '2021-06-23T10:57:17.783Z'
    """
    try:
        # Try format with milliseconds first
        dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # Fall back to format without milliseconds
        dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ")
    return int(dt.timestamp() * 1000)


def transform_data1(data):
    """
    Converts data from format 1 (data-1.json) to the unified format (data-result.json).
    Expected format:
    {
        "deviceID": "dh28dslkja",
        "deviceType": "LaserCutter",
        "timestamp": 1624445837783,
        "location": "japan/tokyo/keiyō-industrial-zone/daikibo-factory-meiyo/section-1",
        "operationStatus": "healthy",
        "temp": 22
    }
    Output format:
    {
        "deviceId": "dh28dslkja",
        "deviceType": "LaserCutter",
        "timestamp": 1624445837783,
        "location": "japan/tokyo/keiyō-industrial-zone/daikibo-factory-meiyo/section-1",
        "status": "healthy",
        "temperature": 22
    }
    """
    return {
        "deviceId": data["deviceID"],
        "deviceType": data["deviceType"],
        "timestamp": data["timestamp"],
        "location": data["location"],
        "status": data["operationStatus"],
        "temperature": data["temp"]
    }


def transform_data2(data):
    """
    Converts data from format 2 (data-2.json) to the unified format (data-result.json).
    Expected format:
    {
        "device": {
            "id": "dh28dslkja",
            "type": "LaserCutter"
        },
        "timestamp": "2021-06-23T10:57:17.783Z",
        "country": "japan",
        "city": "tokyo",
        "area": "keiyō-industrial-zone",
        "factory": "daikibo-factory-meiyo",
        "section": "section-1",
        "data": {
            "status": "healthy",
            "temperature": 22
        }
    }
    Output format:
    {
        "deviceId": "dh28dslkja",
        "deviceType": "LaserCutter", 
        "timestamp": 1624445837783,
        "location": "japan/tokyo/keiyō-industrial-zone/daikibo-factory-meiyo/section-1",
        "status": "healthy",
        "temperature": 22
    }
    """
    location = f"{data['country']}/{data['city']}/{data['area']}/{data['factory']}/{data['section']}"
    return {
        "deviceId": data["device"]["id"],
        "deviceType": data["device"]["type"],
        "timestamp": iso_to_millis(data["timestamp"]),
        "location": location,
        "status": data["data"]["status"],
        "temperature": data["data"]["temperature"]
    }


def main():
    with open("data-1.json") as f1, open("data-2.json") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    result1 = transform_data1(data1)
    result2 = transform_data2(data2)

    combined_result = [result1, result2]

    with open("result.json", "w") as outfile:
        json.dump(combined_result, outfile, indent=4)


if __name__ == "__main__":
    main()
