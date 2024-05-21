import multiprocessing
import time

# Function 1
def func1(shared_dict):
    for _ in range(5):
        # Access and print the shared dictionary from func1
        print("Function 1 is running, shared_dict:", shared_dict.items())
        time.sleep(1)

# Function 2
def func2(shared_dict):
    for _ in range(5):
        # Access and print the shared dictionary from func2
        print("Function 2 is running, shared_dict:", shared_dict.items())
        time.sleep(1)

# Controller function to manage both functions using multiprocessing
def controller():
    # Create a shared dictionary
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    # Update the shared dictionary before starting the child processes
    shared_dict["initial_key"] = "Initial value"

    # Print the shared dictionary from the controller function
    print("Shared dictionary from controller before processes start:", shared_dict.items())

    # Create separate processes for func1 and func2, passing the shared dictionary
    process1 = multiprocessing.Process(target=func1, args=(shared_dict,))
    process2 = multiprocessing.Process(target=func2, args=(shared_dict,))

    # Start both processes
    process1.start()
    process2.start()

    # Wait for both processes to finish
    process1.join()
    process2.join()

    # Print the shared dictionary from the controller function after processes finish
    print("Shared dictionary from controller after processes finish:", shared_dict.items())

if __name__ == "__main__":
    controller()