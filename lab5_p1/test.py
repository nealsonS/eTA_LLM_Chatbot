import requests

def fetch_and_print_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully fetched the webpage")
        html_content = response.text
        print(html_content)  # Print the entire HTML content
    else:
        print(f"Failed to fetch the webpage, status code: {response.status_code}")

# Example usage
api_number = "33-053-04852"  # Example API number for demonstration
url = f"https://www.drillingedge.com/search?type=wells&api_no={api_number}"
fetch_and_print_html(url)
