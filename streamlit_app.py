import streamlit as st
import sec_api
from sec_api import QueryApi

queryApi = QueryApi(api_key="e87e55b9ef3850879b46121c8aa1254876d5ea6333813507d101b35f7925506b")
query = {
  "query": "ticker:TSLA AND filedAt:[2020-01-01 TO 2021-12-31] AND formType:\"10-K\"",
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

response = queryApi.get_filings(query)
import json 

API_KEY = 'e87e55b9ef3850879b46121c8aa1254876d5ea6333813507d101b35f7925506b'
from sec_api import ExtractorApi

extractorApi = ExtractorApi(API_KEY)

print(json.dumps(response["filings"][0], indent=2))
for filing in response['filings']:
    print(f"Company: {filing['companyName']}")
    print(f"Ticker: {filing['ticker']}")
    print(f"Form Type: {filing['formType']}")
    print(f"Filed At: {filing['filedAt']}")
    print(f"Link to Filing: {filing['linkToFilingDetails']}")
    print("\n")
    # Get the full-text filing document URL
    document_url = filing['linkToTxt']
    item_1_a_text  = extractorApi.get_section(document_url, '1A', 'text')
    input_text = item_1_a_text[0:1500]
print(item_1_a_text[0:1500])
