import requests

def get_exchange_rates():
    url = "https://api.vatcomply.com/rates"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data.get('rates', {})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}

def print_exchange_rates(rates):
    if not rates:
        print("Error : Rates cannot recieved or its empty.")
    else:
        print("Exchange Rates:")
        for currency, rate in rates.items():
            print(f"{currency}: {rate}")

def compare_currencies():
    currency1 = input("Enter the first currency: ")
    currency2 = input("Enter the second currency: ")

    rates = get_exchange_rates()

    if rates:
        rate1 = rates.get(currency1)
        rate2 = rates.get(currency2)

        if rate1 is not None and rate2 is not None:
            if rate1 < rate2:
                print(f"{currency1} is more valuable.")
            elif rate1 > rate2:
                print(f"{currency2} is more valuable.")
            else:
                print(f"{currency1} and {currency2} rates are equal.")
        else:
            print("Error : Currencies cannot find.")
    else:
        print("Error: Currencies cannot recieved.")

rates = get_exchange_rates()

print_exchange_rates(rates)

user_choice = input("Do you want to compare exhange rates? (Yes/No): ")

if user_choice.lower() == 'yes':
    compare_currencies()

