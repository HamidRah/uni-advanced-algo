import csv
import time
import tracemalloc

# Function to retrieve memory usage in MB
def get_memory_usage():
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics("lineno")
    total_size = sum(stat.size for stat in stats)
    return total_size / (1024 ** 2)  # Convert to MB


# Step 1: Importing the CSV file
def import_railway_network(filename):
    railway_network = {}

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            station_a, station_b, cost = row
            station_a = station_a.lower()
            station_b = station_b.lower()
            if station_a not in railway_network:
                railway_network[station_a] = {}
            if station_b not in railway_network:
                railway_network[station_b] = {}
            railway_network[station_a][station_b] = int(cost)
            railway_network[station_b][station_a] = int(cost)

    return railway_network

# Step 2: Inputting departure and destination stations
def get_user_input():
    departure = input("Enter the departure station: ").lower()
    destination = input("Enter the destination station: ").lower()
    return departure, destination

# Step 3: Finding the cheapest cost and route
def find_cheapest_route(railway_network, departure, destination):
    visited = set()
    cheapest_costs = {station: float('inf') for station in railway_network}
    cheapest_costs[departure] = 0
    previous_station = {}

    def get_cheapest_station():
        return min((station for station in railway_network if station not in visited),
                   key=lambda x: cheapest_costs[x])

    def reconstruct_route():
        route = []
        current_station = destination
        while current_station != departure:
            route.append(current_station)
            current_station = previous_station[current_station]
        route.append(departure)
        route.reverse()
        return route

    current_station = get_cheapest_station()
    while current_station != destination:
        visited.add(current_station)
        for neighbor_station, cost in railway_network[current_station].items():
            if neighbor_station not in visited:
                new_cost = cheapest_costs[current_station] + cost
                if new_cost < cheapest_costs[neighbor_station]:
                    cheapest_costs[neighbor_station] = new_cost
                    previous_station[neighbor_station] = current_station

        current_station = get_cheapest_station()

    route = reconstruct_route()
    cheapest_cost = cheapest_costs[destination]
    return cheapest_cost, route

# Step 4: Modify the raw data
def modify_raw_data(railway_network, filename):
    station_a = input("Enter the first station: ").lower()
    station_b = input("Enter the second station: ").lower()
    cost = int(input("Enter the cost: "))

    # Update the railway network
    if station_a not in railway_network:
        railway_network[station_a] = {}
    if station_b not in railway_network:
        railway_network[station_b] = {}

    # Check if the route already exists
    if station_b in railway_network[station_a]:
        print(f"Route from {station_a} to {station_b} already exists. Modifying the cost.")
    else:
        print(f"New route from {station_a} to {station_b} has been added.")

    railway_network[station_a][station_b] = cost
    railway_network[station_b][station_a] = cost

    # Write the updated data to the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for station_a, connections in railway_network.items():
            for station_b, cost in connections.items():
                writer.writerow([station_a, station_b, cost])

    print("Raw data has been modified.")

# Main program
def main():
    filename = 'task1_4_railway_network.csv'
    railway_network = import_railway_network(filename)

    while True:
        departure, destination = get_user_input()
        
        departure = departure.lower()
        destination = destination.lower()

        if departure not in railway_network:
            print(f"Departure station '{departure}' not found in the railway network.")
            continue

        if destination not in railway_network:
            print(f"Destination station '{destination}' not found in the railway network.")
            continue

        start_time = time.time()

        tracemalloc.start()

        initial_memory = get_memory_usage()
        print(f"Initial memory usage: {initial_memory} MB")

        cheapest_cost, route = find_cheapest_route(railway_network, departure, destination)

        end_memory = get_memory_usage()
        print(f"Final memory usage: {end_memory} MB")

        tracemalloc.stop()

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Cheapest cost between {departure} and {destination}: {cheapest_cost}")
        print("Route:")
        print(" -> ".join(route))

        print(f"Execution time: {execution_time} seconds")

        repeat = input("Do you want to search for another route? (Y/N): ")
        if repeat.lower() != 'y':
            break

    modify = input("Do you want to modify the raw data? (Y/N): ")
    if modify.lower() == 'y':
        modify_raw_data(railway_network, filename)

if __name__ == '__main__':
    main()