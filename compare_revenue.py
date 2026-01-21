### Compare Apple and AMD Revenue
### m02a-instructor/compare_revenue.py
###
### Author: Dhilan + GitHub Copilot
### Date: Jan 10, 2026
###
### Fabricated data, failed revenue retrieval.  Using GPT-4o

import json

def load_amd_data(file_path):
    """Load AMD revenue data from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = (json.load(file)).get('revenue')
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data.")
        return None

def get_apple_data():
    """Placeholder function to fetch Apple revenue data."""
    # Replace this with actual API calls or data loading logic
    apple_data = {
        "2023": 394.33,  # Example revenue in billions
        "2022": 387.54,
        "2021": 365.82
    }
    return apple_data

def compare_revenue(amd_data, apple_data):
    """Compare AMD and Apple revenue data."""
    print("Year\tAMD Revenue (B)\tApple Revenue (B)")
    print("-" * 40)

    for year, amd_revenue in amd_data.items():
        apple_revenue = apple_data.get(year, "N/A")
        print(f"{year}\t{amd_revenue}\t{apple_revenue}")

def main():
    amd_file_path = "amd_data.json"

    # Load AMD data
    amd_data = load_amd_data(amd_file_path)
    if amd_data is None:
        return

    # Get Apple data
    apple_data = get_apple_data()

    # Compare revenue
    compare_revenue(amd_data, apple_data)

if __name__ == "__main__":
    main()
