import json
import sys
sys.path.insert(0, '/var/task')
from agent import create_scam_detector_agent, analyze_and_parse

agent = create_scam_detector_agent()

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    message = body.get("message", "")
    result = analyze_and_parse(agent, message)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
