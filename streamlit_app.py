import requests
import json
import boto3

filing_url = "https://www.sec.gov/Archives/edgar/data/320193/000032019321000056/aapl-20210327.htm"

xbrl_converter_api_endpoint = "https://api.sec-api.io/xbrl-to-json"

api_key = "e87e55b9ef3850879b46121c8aa1254876d5ea6333813507d101b35f7925506b"

final_url = f"{xbrl_converter_api_endpoint}?htm-url={filing_url}&token={api_key}"

response = requests.get(final_url)

xbrl_json = json.loads(response.text)

statements_of_income = xbrl_json.get('StatementsOfIncome', {})

statements_of_income_str = json.dumps(statements_of_income, indent=4)

client = boto3.client("bedrock-runtime", region_name="us-east-1")

model_id = "anthropic.claude-3-haiku-20240307-v1:0"

prompt = f"""Analyze the StatementsOfIncome to assess the financial health and risk profile of a company. Act as a Know Your Customer Analyst.
StatementsOfIncome:
{statements_of_income_str}
"""

native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "temperature": 0.0,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ],
}

request = json.dumps(native_request)

response = client.invoke_model(modelId=model_id, body=request)

model_response = json.loads(response["body"].read())

response_text = model_response["content"][0]["text"]
print(response_text)
