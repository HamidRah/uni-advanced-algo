import time
import tracemalloc

# Function to retrieve memory usage in MB
def get_memory_usage():
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics("lineno")
    total_size = sum(stat.size for stat in stats)
    return total_size / (1024 ** 2)  # Convert to MB

def remove_duplicates(input_file, output_file):
    # Read in the input file and store the numbers in a list
    with open(input_file, 'r') as f:
        numbers = [int(x) for x in f.read().split()]

    #print(f'\nNumbers = {numbers}\n')
    # Determine which unique elements to keep
    counts = {}
    for i, num in enumerate(numbers):
        if num not in counts:
            counts[num] = [i]  # Store the initial index
        else:
            counts[num].append(i)  # Append the index

    #print(f'\nCounts = {counts}\n')
    # Filter the numbers list based on the rule while retaining the order
    retained_indices = []
    filtered_numbers = []
    for num, indices in counts.items():
        #print(f'\nNumber = {num}')
        #print(f'Indices = {indices}\n')
        if len(indices) > 1:
            middle_index = len(indices) // 2
            if len(indices) % 2 == 0:
                middle_index += 1
            #print(f'\nMiddle Index = {middle_index}\n')
            duplicates_to_remove = len(indices) - 1
            #print(f'\nDuplicates to remove = {duplicates_to_remove}\n')
            if middle_index == 1:
                retained_index = indices[middle_index]
            else:
                retained_index = indices[middle_index-1]
            retained_indices.append(retained_index)
        else:
            retained_indices.append(indices[0])

    retained_indices.sort()
    #print(f'\nRetained indices = {retained_indices}\n')

    for index in retained_indices:
        filtered_numbers.append(numbers[index])

    #print(f'\nNew Numbers = {filtered_numbers}\n')
    # Write the result to the output file
    with open(output_file, 'w') as f:
        f.write(' '.join(str(x) for x in filtered_numbers))
    print(f'All duplicates removed and outputted to {output_file}')
# Usage: specify the input and output file names
input_file = 'task1_1_numbers.txt'
output_file = 'task1_1_output.txt'

start_time = time.time()

tracemalloc.start()

initial_memory = get_memory_usage()
print(f"Initial memory usage: {initial_memory} MB")

remove_duplicates(input_file, output_file)

end_memory = get_memory_usage()
print(f"Final memory usage: {end_memory} MB")

tracemalloc.stop()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")