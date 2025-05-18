import random
import calendar
import networkx as nx
import math
from datetime import datetime, timedelta

# Airport and flight data (expanded)
airports = {
    "DEL": {"name": "Delhi", "latitude": 28.5665, "longitude": 77.1031, "timezone": "Asia/Kolkata"},
    "BOM": {"name": "Mumbai", "latitude": 19.0902, "longitude": 72.8683, "timezone": "Asia/Kolkata"},
    "BLR": {"name": "Bengaluru", "latitude": 13.1979, "longitude": 77.7063, "timezone": "Asia/Kolkata"},
    "CCU": {"name": "Kolkata", "latitude": 22.6546, "longitude": 88.4484, "timezone": "Asia/Kolkata"},
    "MAA": {"name": "Chennai", "latitude": 12.9881, "longitude": 80.1656, "timezone": "Asia/Kolkata"},
    "HYD": {"name": "Hyderabad", "latitude": 17.2402, "longitude": 78.4293, "timezone": "Asia/Kolkata"},
    "GOI": {"name": "Goa", "latitude": 15.3808, "longitude": 73.8317, "timezone": "Asia/Kolkata"},
    "AMD": {"name": "Ahmedabad", "latitude": 23.0725, "longitude": 72.6334, "timezone": "Asia/Kolkata"},
    "PNQ": {"name": "Pune", "latitude": 18.5796, "longitude": 73.9015, "timezone": "Asia/Kolkata"},
    "COK": {"name": "Cochin", "latitude": 10.1523, "longitude": 76.4003, "timezone": "Asia/Kolkata"},
    "LKO": {"name": "Lucknow", "latitude": 22.6822, "longitude": 80.8899, "timezone": "Asia/Kolkata"},
    "JAI": {"name": "Jaipur", "latitude": 26.8241, "longitude": 75.8078, "timezone": "Asia/Kolkata"},
    "IXC": {"name": "Chandigarh", "latitude": 30.6835, "longitude": 76.7904, "timezone": "Asia/Kolkata"},
    "VTZ": {"name": "Visakhapatnam", "latitude": 17.7259, "longitude": 83.2252, "timezone": "Asia/Kolkata"},
    "NAG": {"name": "Nagpur", "latitude": 21.0917, "longitude": 79.0433, "timezone": "Asia/Kolkata"},
    "VNS": {"name": "Varanasi", "latitude": 25.4497, "longitude": 82.8541, "timezone": "Asia/Kolkata"},
    "IDR": {"name": "Indore", "latitude": 22.7245, "longitude": 75.8089, "timezone": "Asia/Kolkata"},
    "RPR": {"name": "Raipur", "latitude": 21.1788, "longitude": 81.7348, "timezone": "Asia/Kolkata"},
    "PAT": {"name": "Patna", "latitude": 25.5908, "longitude": 85.0939, "timezone": "Asia/Kolkata"},
    "GAU": {"name": "Guwahati", "latitude": 26.1017, "longitude": 91.5906, "timezone": "Asia/Kolkata"},
    "ATQ": {"name": "Amritsar", "latitude": 31.7083, "longitude": 74.8017, "timezone": "Asia/Kolkata"},
    "IXR": {"name": "Ranchi", "latitude": 23.3134, "longitude": 85.3283, "timezone": "Asia/Kolkata"},
    "IXM": {"name": "Madurai", "latitude": 9.8519, "longitude": 78.0942, "timezone": "Asia/Kolkata"},
    "SHL": {"name": "Shillong", "latitude": 25.6601, "longitude": 91.9702, "timezone": "Asia/Kolkata"},
    "CJB": {"name": "Coimbatore", "latitude": 11.0264, "longitude": 77.0496, "timezone": "Asia/Kolkata"},
    "DXB": {"name": "Dubai", "latitude": 25.2528, "longitude": 55.3644, "timezone": "Asia/Dubai"},
    "SIN": {"name": "Singapore", "latitude": 1.3521, "longitude": 103.9915, "timezone": "Asia/Singapore"},
    "LHR": {"name": "London", "latitude": 51.4700, "longitude": -0.4543, "timezone": "Europe/London"},
    "JFK": {"name": "New York", "latitude": 40.6413, "longitude": -73.7781, "timezone": "America/New_York"},
    "CDG": {"name": "Paris", "latitude": 49.0097, "longitude": 2.5479, "timezone": "Europe/Paris"},
    "SYD": {"name": "Sydney", "latitude": -33.9461, "longitude": 151.1772, "timezone": "Australia/Sydney"},
    "YYZ": {"name": "Toronto", "latitude": 43.6777, "longitude": -79.6248, "timezone": "America/Toronto"},
    "HND": {"name": "Tokyo", "latitude": 35.5534, "longitude": 139.7817, "timezone": "Asia/Tokyo"},
    "DOH": {"name": "Doha", "latitude": 25.2744, "longitude": 51.6081, "timezone": "Asia/Qatar"},
    "IXZ": {"name": "Port Blair", "latitude": 11.6692, "longitude": 92.7348, "timezone": "Asia/Kolkata"},
    "BBI": {"name": "Bhubaneswar", "latitude": 20.2361, "longitude": 85.8197, "timezone": "Asia/Kolkata"}
}

flights = [
    # Direct Flights with departure times
    {"departure": "DEL", "arrival": "BOM", "cost": 4500, "distance": 1100, "layovers": 0, "flight_number": "6E203", "departure_time": "08:00"},
    {"departure": "BOM", "arrival": "BLR", "cost": 3800, "distance": 840, "layovers": 0, "flight_number": "AI405", "departure_time": "10:30"},
    {"departure": "BLR", "arrival": "CCU", "cost": 5500, "distance": 1550, "layovers": 0, "flight_number": "SG721", "departure_time": "12:00"},
    {"departure": "MAA", "arrival": "HYD", "cost": 2800, "distance": 560, "layovers": 0, "flight_number": "6E801", "departure_time": "14:15"},
    {"departure": "GOI", "arrival": "AMD", "cost": 4200, "distance": 1050, "layovers": 0, "flight_number": "AI602", "departure_time": "16:00"},
    {"departure": "PNQ", "arrival": "COK", "cost": 5000, "distance": 1000, "layovers": 0, "flight_number": "SG903", "departure_time": "11:30"},
    {"departure": "LKO", "arrival": "JAI", "cost": 3500, "distance": 480, "layovers": 0, "flight_number": "6E104", "departure_time": "09:00"},
    {"departure": "IXC", "arrival": "VTZ", "cost": 6000, "distance": 1600, "layovers": 0, "flight_number": "AI205", "departure_time": "13:45"},
    {"departure": "NAG", "arrival": "DEL", "cost": 4800, "distance": 800, "layovers": 0, "flight_number": "SG306", "departure_time": "15:30"},
    {"departure": "DEL", "arrival": "VNS", "cost": 3000, "distance": 680, "layovers": 0, "flight_number": "6E407", "departure_time": "17:00"},
    # Flights with Layovers and departure times
    {"departure": "DEL", "arrival": "IXZ", "cost": 6500, "distance": 2400, "layovers": 1, "flight_number": "6E1016", "departure_time": "07:00", "layover_details": [{"airport": "BBI", "duration": 120}]},
    {"departure": "BOM", "arrival": "IXZ", "cost": 7000, "distance": 2200, "layovers": 1, "flight_number": "AI1017", "departure_time": "09:30", "layover_details": [{"airport": "HYD", "duration": 90}]},
    {"departure": "BLR", "arrival": "IXZ", "cost": 6800, "distance": 2000, "layovers": 1, "flight_number": "SG1018", "departure_time": "11:00", "layover_details": [{"airport": "MAA", "duration": 100}]},
    {"departure": "AMD", "arrival": "COK", "cost": 5500, "distance": 1200, "layovers": 1, "flight_number": "6E1019", "departure_time": "13:00", "layover_details": [{"airport": "BLR", "duration": 80}]},
    {"departure": "GAU", "arrival": "DEL", "cost": 6200, "distance": 1800, "layovers": 1, "flight_number": "AI1020", "departure_time": "15:00", "layover_details": [{"airport": "LKO", "duration": 110}]},
    # New flights originating from Chennai (MAA)
    {"departure": "MAA", "arrival": "DEL", "cost": 5000, "distance": 1800, "layovers": 0, "flight_number": "6E211", "departure_time": "09:30"},
    {"departure": "MAA", "arrival": "BOM", "cost": 4200, "distance": 1300, "layovers": 0, "flight_number": "AI422", "departure_time": "11:00"},
    {"departure": "MAA", "arrival": "BLR", "cost": 2500, "distance": 350, "layovers": 0, "flight_number": "SG733", "departure_time": "13:30"},
    {"departure": "MAA", "arrival": "CCU", "cost": 4800, "distance": 1650, "layovers": 0, "flight_number": "6E811", "departure_time": "15:00"},
    {"departure": "MAA", "arrival": "GOI", "cost": 3500, "distance": 750, "layovers": 0, "flight_number": "AI612", "departure_time": "17:30"},
    {"departure": "MAA", "arrival": "AMD", "cost": 5200, "distance": 1600, "layovers": 1, "flight_number": "SG913", "departure_time": "10:00", "layover_details": [{"airport": "BLR", "duration": 75}]},
    {"departure": "MAA", "arrival": "PNQ", "cost": 4500, "distance": 1150, "layovers": 1, "flight_number": "6E114", "departure_time": "12:30", "layover_details": [{"airport": "HYD", "duration": 60}]},
    {"departure": "MAA", "arrival": "COK", "cost": 3000, "distance": 600, "layovers": 0, "flight_number": "AI215", "departure_time": "14:00"},
    {"departure": "MAA", "arrival": "LKO", "cost": 5800, "distance": 1700, "layovers": 1, "flight_number": "SG316", "departure_time": "16:30", "layover_details": [{"airport": "HYD", "duration": 90}]},
    {"departure": "MAA", "arrival": "JAI", "cost": 6000, "distance": 1900, "layovers": 1, "flight_number": "6E417", "departure_time": "08:30", "layover_details": [{"airport": "BLR", "duration": 100}]},
    {"departure": "MAA", "arrival": "IXC", "cost": 6500, "distance": 2200, "layovers": 1, "flight_number": "AI225", "departure_time": "11:30", "layover_details": [{"airport": "HYD", "duration": 110}]},
    {"departure": "MAA", "arrival": "VTZ", "cost": 3200, "distance": 650, "layovers": 0, "flight_number": "SG326", "departure_time": "18:00"},
    {"departure": "MAA", "arrival": "NAG", "cost": 4700, "distance": 1100, "layovers": 1, "flight_number": "6E427", "departure_time": "07:30", "layover_details": [{"airport": "BLR", "duration": 80}]},
    {"departure": "MAA", "arrival": "VNS", "cost": 6200, "distance": 1850, "layovers": 1, "flight_number": "AI235", "departure_time": "10:30", "layover_details": [{"airport": "HYD", "duration": 95}]},
    {"departure": "MAA", "arrival": "IDR", "cost": 5500, "distance": 1400, "layovers": 1, "flight_number": "SG336", "departure_time": "13:00", "layover_details": [{"airport": "BLR", "duration": 70}]},
    {"departure": "MAA", "arrival": "RPR", "cost": 5800, "distance": 1500, "layovers": 1, "flight_number": "6E437", "departure_time": "15:30", "layover_details": [{"airport": "VTZ", "duration": 65}]},
    {"departure": "MAA", "arrival": "PAT", "cost": 6300, "distance": 1950, "layovers": 1, "flight_number": "AI245", "departure_time": "17:00", "layover_details": [{"airport": "CCU", "duration": 105}]},
]
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points on the Earth using the Haversine formula."""
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def create_flight_graph(airports, flights):
    """Creates a graph of flights."""
    graph = nx.Graph()
    for airport_code in airports:
        graph.add_node(airport_code)
    for flight in flights:
        graph.add_edge(flight["departure"], flight["arrival"], weight=flight["cost"])
    return graph

def heuristic(node, goal, airports):
    """Heuristic function for A* search."""
    lat1, lon1 = airports[node]["latitude"], airports[node]["longitude"]
    lat2, lon2 = airports[goal]["latitude"], airports[goal]["longitude"]
    return calculate_distance(lat1, lon1, lat2, lon2)

def find_flight_route(graph, start, end, airports):
    """Finds the shortest flight route using A* search."""
    try:
        path = nx.astar_path(graph, start, end, heuristic=lambda n, g: heuristic(n, g, airports), weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def validate_airport_code(code, airports):
    """Validates an airport code."""
    if code.upper() in airports:
        return code.upper()
    else:
        return None

def display_route(route, airports, flights):
    """Displays a flight route with layover details, departure times, and total distance."""
    if not route:
        print("No route found.")
        return

    route_str = "Route: "
    total_cost = 0
    total_distance = 0
    for i in range(len(route) - 1):
        route_str += f"{route[i]} ({airports[route[i]]['name']}) -> "
        for flight in flights:
            if flight["departure"] == route[i] and flight["arrival"] == route[i + 1]:
                total_cost += flight["cost"]
                total_distance += flight["distance"]
                route_str += f"{route[i+1]} ({airports[route[i+1]]['name']}) "
                route_str += f"(Departure: {flight['departure_time']}) "
                if flight["layovers"] > 0:
                    for layover in flight["layover_details"]:
                        route_str += f"(Layover at {layover['airport']} ({airports[layover['airport']]['name']}) for {layover['duration']} minutes) "
                break  # Move to the next segment of the route once the matching flight is found

    print(route_str)
    print(f"Total Cost: \u20B9{total_cost}")
    print(f"Total Distance: {total_distance} km")

def book_flight(destination, year, month, day, passengers):
    """Simulates booking a flight."""
    confirmation_number = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
    print(f"Your flight to {destination} ({airports[destination]['name']}) on {year}-{month}-{day} for {passengers} passengers has been booked.")
    print(f"Confirmation number: {confirmation_number}")

flight_graph = create_flight_graph(airports, flights)

def main():
    """Main function for the chatbot."""
    print("Welcome to Flight Booking Service! How can I assist you today?")
    while True:
        user_input = input("You: ").lower()
        if "exit" in user_input or "bye" in user_input or "thanks" in user_input or "thanks for help" in user_input:
            print("Bot: You're welcome! Have a great day!")
            break
        elif "route" in user_input:
            departure = input("Enter departure airport code: ").upper()
            arrival = input("Enter arrival airport code: ").upper()

            departure = validate_airport_code(departure, airports)
            arrival = validate_airport_code(arrival, airports)

            if departure and arrival:
                route = find_flight_route(flight_graph, departure, arrival, airports)
                display_route(route, airports, flights)
            else:
                print("Bot: Invalid airport code. Please try again.")
        elif "book flight tickets" in user_input:
            destination = input("Where would you like to fly to? ").upper()
            year = int(input("Enter the year: "))
            month = int(input("Enter the month (1-12): "))
            print(calendar.month(year, month))
            day = int(input("Enter the day: "))
            passengers = int(input("How many passengers will be flying? "))
            print("Passengers Information:")
            names = []
            for i in range(passengers):
                print(f"Details of Passenger {i+1}:")
                first_name = input("Enter first name: ")
                middle_name = input("Enter middle name: ")
                last_name = input("Enter last name: ")
                age = input("Enter age: ")
                gender = input("Enter gender: ")
                names.append(first_name)
            print("Passengers Information:")
            for name in names:
                print(name)
            book_flight(destination, year, month, day, passengers)
        else:
            print("Bot: I'm sorry, I don't understand. Please try again.")

if _name_ == "_main_":
    main()