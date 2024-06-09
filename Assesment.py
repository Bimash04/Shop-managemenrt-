import datetime

# Function to read the laptop information from the text file
def read_laptops(filename):
    laptops = []
    with open(filename, 'r') as file:# Open the file in read mode
        for line in file:# Read each line in the file
            laptop_info = line.strip().split(', ')# Split the line by comma and space to get laptop information
            laptops.append(laptop_info)# Add the laptop information to the list
    return laptops

# Function to write the updated laptop information to the text file
def write_laptops(filename, laptops):
    with open(filename, 'w') as file:
        for laptop in laptops:# Iterate over each laptop in the list
            file.write(', '.join(laptop) + '\n') # Write the laptop information as a line in the file

# Function to display the available laptops
def display_laptops(laptops):
    print("Available Laptops:")
    for laptop in laptops:
        print(", ".join(laptop))

# Function to generate a unique note/invoice filename
def generate_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"note_{timestamp}.txt"

# Function to generate a note/invoice for an order or sale
def generate_note(laptop, customer, date, amount, shipping_cost, total_amount):
    note = f"--- Order Note ---\n"
    note += f"Laptop: {laptop[0]}\n"
    note += f"Brand: {laptop[1]}\n"
    note += f"Customer: {customer}\n"
    note += f"Date: {date}\n"
    note += f"Amount: ${amount}\n"
    note += f"Shipping Cost: ${shipping_cost}\n"
    note += f"Total Amount: ${total_amount}\n"
    return note

# Main program
def main():
    laptops = read_laptops("laptops.txt")# Read the laptop information from the file
    display_laptops(laptops)# Display the available laptops

    while True:
        print("\n1. Place an order from the manufacturer")
        print("2. Sell a laptop to a customer")
        print("3. Quit")
        choice = input("Enter your choice (1-3): ")# Get the user's choice
        if choice == '1':  # Placing an order from the manufacturer
            distributor = input("Enter distributor name: ")
            laptop_name = input("Enter laptop name: ")
            brand = input("Enter brand: ")
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
            while True:
                try:
                    quantity = int(input("Enter quantity: "))
                    break
                except ValueError:
                    print("Please enter a valid integer for the quantity.")

            # Check if the laptop is available in the file
            laptop_found = False
            with open("laptops.txt", "r") as file:
                for line in file:
                    laptop_info = line.strip().split(",")
                    if laptop_info[0] == laptop_name and laptop_info[1] == brand:
                        laptop_found = True
                        break

            if laptop_found:
                # Update stock quantity and generate note/invoice for the order
                for laptop in laptops:
                    if laptop[0] == laptop_name and laptop[1] == brand:
                        laptop[3] = str(int(laptop[3]) + quantity)
                        # Generate note/invoice for the order
                        filename = generate_filename()
                        note = f"--- Order Note ---\n"
                        note += f"Distributor: {distributor}\n"
                        note += f"Laptop: {laptop_name}\n"
                        note += f"Brand: {brand}\n"
                        note += f"Date: {date}\n"
                        note += f"Quantity: {quantity}\n"
                        note += f"Net Amount: ${float(laptop[2]) * quantity}\n"
                        vat_amount = float(laptop[2]) * quantity * 0.13
                        note += f"VAT Amount: ${vat_amount}\n"
                        note += f"Gross Amount: ${float(laptop[2]) * quantity + vat_amount}\n"
                        
                        # Save note/invoice to a file
                        with open(filename, 'w') as file:
                            file.write(note)

                        print(f"\nOrder placed successfully. Note saved to {filename}")
                        write_laptops("laptops.txt", laptops)
                        break
            else:
                print("Laptop not found in the file. Please check the name and brand.")


        elif choice == '2':  # Selling a laptop to a customer
            customer = input("Enter customer name: ")
            laptop_name = input("Enter laptop name: ")
            brand = input("Enter brand: ")
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            quantity = int(input("Enter quantity: "))

            # Check stock quantity
            available_quantity = 0
            for laptop in laptops:
                if laptop[0] == laptop_name and laptop[1] == brand:
                    available_quantity = int(laptop[3])
                    break

            if available_quantity < quantity:
                print("Insufficient stock. Sale canceled.")
            else:
                # Update stock quantity
                for laptop in laptops:
                    if laptop[0] == laptop_name and laptop[1] == brand:
                        current_stock = int(laptop[3])
                        laptop[3] = str(current_stock - quantity)
                        break

                # Update the laptop information in the text file
                write_laptops("laptops.txt", laptops)

                # Generate note/invoice for the sale
                filename = generate_filename()
                laptop = [laptop for laptop in laptops if laptop[0] == laptop_name and laptop[1] == brand][0]
                amount = float(laptop[2]) * quantity
                shipping_cost = 50  # Assuming a fixed shipping cost of $50
                total_amount = amount + shipping_cost
                note = generate_note(laptop, customer, date, amount, shipping_cost, total_amount)

                # Save note/invoice to a file
                try:
                    with open(filename, 'w') as file:
                            file.write(note)

                    print(f"\nSale completed successfully. Note saved to {filename}")
                except IOError:
                    print("An error occurred while saving the note to a file.")
                
        elif choice == '3':  # Quit the program
            print("Thank you for visting us.")
            break

        else:
            print("Invalid choice. Please try again.")

    # Update the laptop information in the text file
    write_laptops("laptops.txt", laptops)

# Run the program
if __name__ == '__main__':
    main()
