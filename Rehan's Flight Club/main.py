import time
from datetime import datetime, timedelta
from data_manager import DataManager
from user_manager import UserManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from signup import run_signup_flow

ORIGIN = {
    "skyId": "LOND",
    "entityId": "27544008"
}

CITY_MAP = {
    "Paris": {"skyId": "PARI", "entityId": "27539733"},
    "Tokyo": {"skyId": "TYOA", "entityId": "27547053"},
    "New York": {"skyId": "NYCA", "entityId": "27537542"},
    "Sydney": {"skyId": "SYD", "entityId": "27547070"},
    "Lahore": {"skyId": "LHE", "entityId": "27542478"},
    "Berlin": {"skyId": "BERL", "entityId": "27538571"},
}

data_manager = DataManager()
user_manager = UserManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

def main():
    current_user = run_signup_flow(user_manager)
    if not current_user:
        print("Sign-up aborted or failed. Exiting Rehan's Flight Club.")
        exit()

    print("\n==========================================")
    print("        POPULAR DESTINATIONS MENU        ")
    print("==========================================")
    cities = list(CITY_MAP.keys())
    for index, city in enumerate(cities, start=1):
        print(f"{index}. {city}")

    user_input = input("\nSelect a number, OR type ANY city in the world: ").strip()

    # Determine if user selected a pre-mapped city or typed a custom city
    if user_input.isdigit() and 1 <= int(user_input) <= len(cities):
        selected_city = cities[int(user_input) - 1]
    else:
        selected_city = user_input.title()

    if not selected_city:
        print("No city entered. Exiting.")
        exit()

    print(f"\nTarget Destination: {selected_city}")

    # ----- Step 3: Budget Input -----
    try:
        user_budget = float(input(f"Enter your maximum target budget for {selected_city} (£): "))
    except ValueError:
        user_budget = 500.0
        print("Invalid budget amount entered. Defaulting budget to £500.00")

    # ----- Step 4: Resolve Destination Location Data -----
    destination = CITY_MAP.get(selected_city)
    if not destination:
        print(f"\nLooking up airport location code for '{selected_city}'...")
        destination = flight_search.get_destination_code(selected_city)

    if not destination:
        print(f"Could not find valid airport data for '{selected_city}'. Stopping.")
        exit()

    # ----- Step 5: Real-Time Flight Search -----
    print(f"\nSearching live flights from London to {selected_city}...")
    travel_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    flight = flight_search.check_flights(ORIGIN, destination, travel_date=travel_date)

    # ----- Step 6: Budget Analysis & Booking Confirmation -----
    if flight:
        print("\n==========================================")
        print("          FLIGHT ITINERARY DETAILS        ")
        print("==========================================")
        print(f"Origin Airport:      {flight.origin_airport}")
        print(f"Destination City:    {flight.destination_city} ({flight.destination_airport})")
        print(f"Departure Date:      {flight.out_date}")
        print(f"Stops:               {flight.stops}")
        print(f"Current Flight Price: £{flight.price}")
        print(f"Your Saved Budget:   £{user_budget}")
        print("==========================================")

        price_difference = user_budget - flight.price

        if flight.price <= user_budget:
            print(f"✓ GREAT DEAL! This flight is WITHIN your budget (Save £{price_difference:.2f}).")
        else:
            print(f"⚠ NOTICE: This flight exceeds your target budget by £{abs(price_difference):.2f}.")

        # User Decision Point
        decision = input("\nDo you want to reserve/take this ticket? (yes/no): ").strip().lower()

        if decision in ["yes", "y", "ok"]:
            print(f"\nTicket selected! Sending flight confirmation alert to {current_user['email']}...")
            
            # Send notification email via SMTP
            notification_manager.send_flight_email(flight, [current_user["email"]])
            
            # Generate direct Skyscanner hold/booking link
            booking_url = f"https://www.skyscanner.com/transport/flights/lond/{destination['skyId'].lower()}/"
            print("\n------------------------------------------")
            print("RESERVATION LINK GENERATED SUCCESSFULY!")
            print(f"Complete your hold & booking here:\n{booking_url}")
            print("------------------------------------------")
        else:
            print("\nTicket purchase canceled. No deal alert requested.")

    else:
        print(f"No active flight offers available for {selected_city} on {travel_date}.")

    print("\nThank you for using Rehan's Flight Club!")


if __name__ == "__main__":
    main()