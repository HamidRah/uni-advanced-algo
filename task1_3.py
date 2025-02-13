import multiprocessing
import time
import tracemalloc

# Function to retrieve memory usage in MB
def get_memory_usage():
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics("lineno")
    total_size = sum(stat.size for stat in stats)
    return total_size / (1024 ** 2)  # Convert to MB


def count_frequency(name, text):
    frequency = text.lower().count(name.lower())
    return name, frequency

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    names = set()
    with open('task1_3_names.txt', 'r', encoding='utf-8') as names_file:
        names = set(names_file.read().splitlines())

    num_cores = multiprocessing.cpu_count()

    # Adjust the number of processes based on the input size
    num_processes = min(len(names), num_cores)
    pool = multiprocessing.Pool(processes=num_processes)
    results = []
    for name in names:
        results.append(pool.apply_async(count_frequency, args=(name, text)))

    pool.close()
    pool.join()

    frequencies = {}
    for result in results:
        name, frequency = result.get()
        frequencies[name] = frequency

    with open('task1_3_results.txt', 'w') as output_file:
        for name, frequency in frequencies.items():
            output_file.write(f"{name} {frequency}\n")

    print("Frequency counting completed. Results saved in 'task1_3_results.txt'.")

if __name__ == '__main__':
    start_time = time.time()

    tracemalloc.start()

    initial_memory = get_memory_usage()
    print(f"Initial memory usage: {initial_memory} MB")

    process_file('task1_3_text.txt')

    end_memory = get_memory_usage()
    print(f"Final memory usage: {end_memory} MB")

    tracemalloc.stop()

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds.")