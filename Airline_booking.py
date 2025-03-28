import random
import string
import sqlite3

class AirlineBookingSystem:
    def __init__(self):
        """Initialize the seat matrix: 80 rows and 7 columns, default "F" is empty"""
        self.rows = 80
        self.cols = ['A', 'B', 'C', 'X','D', 'E', 'F']
        self.seating_chart = self.initialize_seats()
        self.generated_references = set()  # Store the generated unique subscription number
        self.db_connection()
    
    def db_connection(self):
        self.conn = sqlite3.connect("airline_bookings.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                                seat TEXT PRIMARY KEY,
                                booking_ref TEXT UNIQUE,
                                first_name TEXT,
                                last_name TEXT,
                                passport_number TEXT)''')
        self.conn.commit()
    
    def initialize_seats(self):
        """Tag unsubscribed areas ('X') and storage areas ('S')"""
        seating = {}
        for row in range(1, self.rows + 1):
            for col in self.cols:
                seat = f"{row}{col}" # Generate seat number
                if seat in ['77D', '78D', '77E', '78E', '77F', '78F']:
                     seating[seat] = 'S' # Storage area
                elif col == 'X':  
                     seating[f"{row}{col}"] = 'X'  # Set aisle at column X
                else:
                    seating[f"{row}{col}"] = 'F'  # Free seats
        return seating
    
    def display_seats(self):
        """Show seat status"""
        print("\nCurrent Seat Status:")
        for row in range(1, self.rows + 1):
            row_display = [] # Stores the status of all seats in this row.
            for col in self.cols:
                seat = f"{row}{col}" # Generate the number of the current seat
                row_display.append(self.seating_chart.get(seat, ' ')) # Get the status of the current seat
            print(f"Row {row}: ", " ".join(row_display)) # Output all seat statuses of this line
    
    def check_availability(self, seat):
        """Check if the selected seat is within the valid range"""
        return self.seating_chart.get(seat) == 'F'
    
    def generate_booking_reference(self):
     """Generate a unique 8-bit random subscription reference number"""
     while True: # Enter a loop to ensure that the generated number does not repeat.
        reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) # Generate a new 8-digit subscription number
        if reference not in self.generated_references: # Check if the number already exists
            self.generated_references.add(reference)
            return reference
    
    def book_seat(self, seat):
        """Book a seat"""
        if self.check_availability(seat):
            self.seating_chart[seat] = 'R' # Check if the seat is available.
            booking_ref = self.generate_booking_reference()
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            passport_number = input("Enter Passport Number: ")
            
            self.seating_chart[seat] = booking_ref
            self.cursor.execute("INSERT INTO bookings VALUES (?, ?, ?, ?, ?)", 
                                (seat, booking_ref, first_name, last_name, passport_number))
            self.conn.commit()
            print(f"Seat {seat} booked successfully! Booking Ref: {booking_ref}")
        else:
            print(f"Seat {seat} is not available.")
    
    def free_seat(self, seat):
        """Free a seat"""
        if self.seating_chart.get(seat) == 'R':
            self.seating_chart[seat] = 'F' # If the seat has been booked, it will be restored to an empty seat
            self.cursor.execute("DELETE FROM bookings WHERE seat = ?", (seat,))
            self.conn.commit()
            print(f"Seat {seat} is now free.")
        else:
            print(f"Seat {seat} is not currently booked.")
    
    def menu(self):
        while True:
            print("\n1. Check Availability\n2. Book a Seat\n3. Free a Seat\n4. Show Booking Status\n5. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                seat = input("Enter seat (e.g., 1A-80F): ")
                available = self.check_availability(seat)
                print(f"Seat {seat} is {'available' if available else 'not available'}.")
            elif choice == '2':
                seat = input("Enter seat (e.g., 1A-80F): ")
                self.book_seat(seat)
            elif choice == '3':
                seat = input("Enter seat (e.g., 1A-80F): ")
                self.free_seat(seat)
            elif choice == '4':
                self.display_seats()
            elif choice == '5':
                print("Exiting program.")
                self.conn.close()
                break
            else:
                print("Invalid option.")

if __name__ == "__main__":
    system = AirlineBookingSystem()
    system.menu()
    
    
    