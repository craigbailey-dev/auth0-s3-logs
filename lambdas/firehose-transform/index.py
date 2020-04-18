import json
import base64
import traceback
from datetime import datetime

def handler(event, context):
    output = []
    for record in event["records"]:
        try:
            # Base64 decode record data and JSON parse data
            entry = base64.b64decode(record["data"]).decode("utf-8")
            parsed_entry = json.loads(entry)
            payload = parsed_entry["detail"]["data"]
            payload["timestamp"] = payload["date"]
            del payload["date"]
            payload["details"] = json.dumps(payload["details"])
            
            # Add new line to payload string, Base64 encode payload and return transformed record
            decoded_data = json.dumps(payload) + "\n"
            encoded_data = base64.b64encode(decoded_data.encode("utf-8")).decode("utf-8")
            output.append({
                "recordId": record["recordId"],
                "result": "Ok",
                "data": encoded_data,
            })
        except:
            # If an error occurs, print error and return record as having failed processing
            traceback.print_exc()
            output.append({
                "recordId": record["recordId"],
                "result": "ProcessingFailed",
                "data": record["data"],
            })
    return {
        "records": output
    }