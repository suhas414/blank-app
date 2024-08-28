import requests
import csv

def get_ticker(company_name):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotesCount": 1, "region": "US"}

    try:
        res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
        res.raise_for_status()  # Raise an exception for HTTP errors

        data = res.json()

        if 'quotes' in data and len(data['quotes']) > 0:
            company_code = data['quotes'][0]['symbol']
            return company_code
        else:
            print(f"No ticker found for company '{company_name}'.")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        return None

def load_ticker_cik_mapping(file_path):
    ticker_cik_map = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    ticker, cik = row
                    ticker_cik_map[ticker.strip().upper()] = cik.strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")
    return ticker_cik_map

def main():
    # Path to the CSV file
    file_path = 'tickers.csv'

    # Load the ticker-CIK mapping from the CSV file
    ticker_cik_map = load_ticker_cik_mapping(file_path)

    # Prompt user for company name
    company_name = input("Enter company name: ").strip()

    # Look up ticker symbol
    ticker_symbol = get_ticker(company_name)

    if ticker_symbol:
        # Retrieve and display the CIK number
        cik_number = ticker_cik_map.get(ticker_symbol.upper())
        if cik_number:
            print(f"The CIK number for ticker symbol '{ticker_symbol}' is {cik_number}.")
        else:
            print(f"No CIK number found for ticker symbol '{ticker_symbol}'.")
    else:
        print("Failed to retrieve ticker symbol.")

if __name__ == "__main__":
    main()
