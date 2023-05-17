import threading
import queue
import time

def async_job(input_queue, output_queue):
    while True:
        # Get input from the input queue
        input_data = input_queue.get()

        # Perform the asynchronous job
        # Replace this with your actual job logic
        time.sleep(2)  # Simulating some time-consuming task

        # Put the result in the output queue
        output_queue.put(input_data + " processed")

def main():
    # Create input and output queues
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    # Start the asynchronous job thread
    job_thread = threading.Thread(target=async_job, args=(input_queue, output_queue))
    job_thread.start()

    # Submit input to the job thread asynchronously
    input_queue.put("Data 1")
    input_queue.put("Data 2")
    input_queue.put("Data 3")

    # Continue doing other work in the main thread
    print("Main thread doing other work...")

    # Retrieve the output from the job thread
    result1 = output_queue.get()
    result2 = output_queue.get()
    result3 = output_queue.get()

    # Print the results
    print(result1)
    print(result2)
    print(result3)
    return 13

    # Wait for the job thread to finish
    job_thread.join()

if __name__ == "__main__":
    main()