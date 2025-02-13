import time
import tracemalloc

def get_memory_usage():
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics("lineno")
    total_size = sum(stat.size for stat in stats)
    return total_size / (1024 ** 2)  # Convert to MB

# merge sort
def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers

    mid = len(numbers) // 2
    left = merge_sort(numbers[:mid])
    right = merge_sort(numbers[mid:])
    return merge(left, right)

def sort_numbers(numbers):
    start_time = time.time()
    sorted_numbers = merge_sort(numbers)
    sorting_time = time.time() - start_time
    return sorted_numbers, sorting_time



# binary search
def binary_search(numbers, value):
    low = 0
    high = len(numbers) - 1

    while low <= high:
        mid = (low + high) // 2
        if numbers[mid] == value:
            return mid
        elif numbers[mid] < value:
            low = mid + 1
        else:
            high = mid - 1

    return low

def binary_search_delete(numbers, value):
    low = 0
    high = len(numbers) - 1

    while low <= high:
        mid = (low + high) // 2
        if numbers[mid] == value:
            return mid
        elif numbers[mid] < value:
            low = mid + 1
        else:
            high = mid - 1

    return -1

def search_number(numbers, value):
    start_time = time.time()
    found = binary_search(numbers, value) != len(numbers) and numbers[binary_search(numbers, value)] == value
    search_time = time.time() - start_time
    return found, search_time

def insert_number(numbers, value):
    start_time = time.time()
    index = binary_search(numbers, value)
    numbers.insert(index, value)
    insertion_time = time.time() - start_time
    return insertion_time

def delete_number(numbers, value):
    start_time = time.time()
    indexes = []

    # Find all occurrences of the value using binary search
    index = binary_search(numbers, value)
    while index != len(numbers) and numbers[index] == value:
        indexes.append(index)
        index += 1

    # Delete the occurrences in reverse order by shifting elements
    for idx in reversed(indexes):
        numbers.pop(idx)

    deletion_time = time.time() - start_time
    return deletion_time

def perform_operations(numbers, operations):
    for operation in operations:
        operation_code, value = operation
        if operation_code == 1:
            found, search_time = search_number(numbers, value)
            print(f"Search for {value}: {found}! (Execution time: {search_time} seconds)")
        elif operation_code == 2:
            insertion_time = insert_number(numbers, value)
            #print(f"Insert {value} into the list (Execution time: {insertion_time} seconds)")
        elif operation_code == 3:
            deletion_time = delete_number(numbers, value)
            #print(f"Delete {value} from the list (Execution time: {deletion_time} seconds)")

    return numbers

numbers = []
with open('task1_2_numbers.txt', 'r') as f:
    numbers = [int(x) for x in f.read().split()]

operations = []
with open('task1_2_operations.txt', 'r') as file:
    for line in file:
        operation_code, value = map(int, line.strip().split())
        operations.append((operation_code, value))

tracemalloc.start()

initial_memory = get_memory_usage()
print(f"Initial memory usage: {initial_memory} MB")

start_time = time.time()

sorted_numbers, sorting_time = sort_numbers(numbers)

end_memory_sorting = get_memory_usage()
print(f"Memory usage after sorting: {end_memory_sorting} MB")

sorted_numbers = perform_operations(sorted_numbers, operations)

end_memory_operations = get_memory_usage()
print(f"Memory usage after operations: {end_memory_operations} MB")

tracemalloc.stop()

print(f"Sorting time: {sorting_time} seconds")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

# Write the updated numbers list to a new file
with open('task1_2_output.txt', 'w') as file:
    file.write(' '.join(map(str, sorted_numbers)))

print("Updated numbers list written to 'task1_2_output.txt'")