import threading
import time
import queue
import random

waiting_chairs = None
barber_sleeping = None
customer_queue = None
active_customers = None

def initialize_barbershop(num_chairs):
    global waiting_chairs, barber_sleeping, customer_queue, active_customers
    waiting_chairs = threading.Semaphore(num_chairs)
    barber_sleeping = threading.Event()
    customer_queue = queue.Queue(maxsize=num_chairs)
    active_customers = threading.Event()  # Event to track active customers

def barber():
    while True:
        print('\n' + "Barber is sleeping.")
        barber_sleeping.wait()
        waiting_chairs.release()
        customer_name = customer_queue.get()  # Get the customer from the queue and remove them
        print('\n' + f"Barber is cutting hair for {customer_name}.")
        time.sleep(random.randint(1, 5))
        print('\n' + f"Barber finished cutting hair for {customer_name}.")
        customer_queue.task_done()
        
        
        if customer_queue.empty() or not active_customers.is_set():
            print('\n' + "No more customers. Barber is going to sleep.")
            
            restart_option = input("Do you want to Continue? (yes/no): " + '\n')
            if restart_option.lower() in ["yes", "y", "ye", "ys", "es"]:
                while True:
                    add_customer_option = input('\n' + "Do you want to add a customer? (yes/no): " + '\n')
                    if add_customer_option.lower() in ["yes", "y", "ye", "ys", "es"]:
                        add_customer()
                    elif add_customer_option.lower() in ["no", "n", "o"]:
                        print( '\n' + "Barbershop simulation started.")
                        break 
                    else:
                        print( '\n' + "Enter YES or NO. ")
                active_customers.set()  # Set the flag to indicate there are active customers
                barber_sleeping.set()  # Barber wakes up
                barber_thread = threading.Thread(target=barber)
                barber_thread.start()
                barber_thread.join()
            elif restart_option.lower() in ["no", "n", "o"]:
                print('\n' + "Barbershop simulation ended.")
                break
            else:
                print( '\n' + "Enter YES or NO. ")
            break
        
    



def add_customer():
    customer_name = input('\n' + "Enter customer name: " + '\n' )
    try:
        customer_queue.put_nowait(customer_name)
        print('\n' + f"{customer_name} entered the shop and sat in a chair.")
        barber_sleeping.set()
        active_customers.set()  # Set the flag to indicate there are active customers
    except queue.Full:
        print( '\n' + f"{customer_name} will not enter the shop.")
        print( '\n' + "No available chairs. Barber shop is full." + '\n')
        barber_thread = threading.Thread(target=barber)
        barber_thread.start()
        barber_thread.join()

def main():
    num_chairs = int(input("Enter the number of chairs in the barbershop: " + '\n' ))
    initialize_barbershop(num_chairs)
    
    while True:
        add_customer_option = input('\n' + "Do you want to add a customer? (yes/no): " + '\n')
        if add_customer_option.lower() in ["yes", "y", "ye", "ys", "es"]:
            add_customer()
        elif add_customer_option.lower() in ["no", "n", "o"]:
            print( '\n' + "Barbershop simulation started.")
            break 
        else:
            print( '\n' + "Enter YES or NO. ")
    
    barber_thread = threading.Thread(target=barber)
    barber_thread.start()
    barber_thread.join()

if __name__ == "__main__":
    main()
