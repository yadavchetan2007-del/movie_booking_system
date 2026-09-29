# Movie Ticket Booking System

A simple **Movie Ticket Booking System** made using basic Python. The program runs in the terminal and allows users to view movies, check seats, book tickets, cancel bookings, calculate ticket prices, and view booking records.

## Features

- Display currently available movies
- View seat layout for each movie
- Book one or more movie tickets
- Select Silver and Gold seats
- Check whether a seat is already booked
- Calculate ticket price
- Apply a 10% discount for 4 or more seats
- Use the `CINEMA10` coupon for a 10% discount
- Add 5% GST to the final amount
- Cancel an existing booking
- View all booking records
- Print a booking receipt
- Save bookings in a simple text file
- Load previous bookings when the program starts

## Requirements

- Python 3.x
- No external Python libraries are required
- Uses only basic Python features and a normal text file

## How to Run

1. Make sure Python 3 is installed.
2. Keep `movie_ticket_booking_simple.py` in a folder.
3. Open a terminal or command prompt in that folder.
4. Run:

```bash
python movie_ticket_booking_simple.py
```

A `bookings.txt` file will be created automatically when a booking is saved.

## Main Menu

When the program starts, it shows these options:

```text
1. Display Movies
2. View Seats
3. Book Tickets
4. Cancel Booking
5. Calculate Ticket Amount
6. View Bookings
7. Exit
```

### 1. Display Movies

Shows the movie ID, title, show time, and Silver/Gold ticket prices.

### 2. View Seats

Shows the seating arrangement from rows **A to E** and columns **1 to 6**.

- Rows **A and B** are Silver seats.
- Rows **C, D and E** are Gold seats.
- `[A1]` means the seat is available.
- `[ X ]` means the seat is booked.

Each movie has 30 seats in total.

### 3. Book Tickets

The booking process is:

1. Select a movie.
2. Enter customer name.
3. Enter phone number.
4. Enter seat numbers such as `A1,A2,B3`.
5. Enter a coupon code if available.
6. Check the ticket amount.
7. Confirm the booking.
8. The selected seats are marked as booked.
9. A booking receipt is displayed.

Each confirmed booking gets a booking ID starting from **1001**.

### 4. Cancel Booking

A booking can be searched using either:

- Booking ID
- Customer phone number

After cancellation, the seats become available again and the booking status changes to `Cancelled`.

### 5. Calculate Ticket Amount

This option gives a price estimate without making an actual booking.

The calculation is:

```text
Ticket price
     ↓
Discount (if applicable)
     ↓
5% GST
     ↓
Final amount
```

### 6. View Bookings

Displays saved bookings with:

- Booking ID
- Customer name
- Seats
- Total amount
- Booking status

A full receipt can also be printed by entering a booking ID.

### 7. Exit

Closes the program.

## Ticket Prices

| Movie | Silver | Gold |
|---|---:|---:|
| Inception | Rs. 150 | Rs. 250 |
| Interstellar | Rs. 150 | Rs. 250 |
| The Dark Knight | Rs. 150 | Rs. 250 |
| Avatar: The Way of Water | Rs. 180 | Rs. 280 |

## Discount Rules

### Bulk Discount

A **10% discount** is given when **4 or more seats** are selected.

### Coupon Discount

The coupon:

```text
CINEMA10
```

gives a **10% discount**.

When 4 or more seats are booked, the bulk discount is applied before the coupon.

## GST

The program adds **5% GST** after the discount.

For example:

```text
Subtotal = Rs. 1000
Discount = Rs. 100
Taxable amount = Rs. 900
GST = Rs. 45
Final amount = Rs. 945
```

## File Storage

The program stores booking information in:

```text
bookings.txt
```

The file uses a simple `|` separated text format instead of JSON or a database.

The stored information includes:

```text
Booking ID
Customer name
Phone number
Movie ID
Movie name
Show time
Seats
Subtotal
Discount
Tax
Total
Status
```

When the program starts again, it reads the file and restores confirmed bookings and their booked seats.

## Project Structure

```text
Movie Ticket Booking System/
│
├── movie_ticket_booking_simple.py
├── bookings.txt              # Created automatically
└── README.md
```

## Technologies Used

- Python 3
- Dictionaries
- Lists
- Loops
- Functions
- Conditional statements
- File handling
- String formatting

No GUI, database, JSON, or external Python packages are used.

## Notes

- The program is designed for terminal/command-line use.
- Booking data is stored locally in `bookings.txt`.
- The phone number check requires at least 10 digits.
- Seat codes must match the available layout, for example `A1` or `C4`.
- If the `bookings.txt` file does not exist, the program simply starts with no previous bookings.

## Example Seat Layout

```text
        1     2     3     4     5     6
       -----------------------------------
Row A: [A1] [A2] [A3] [A4] [A5] [A6] Rs.150
Row B: [B1] [B2] [B3] [B4] [B5] [B6] Rs.150
Row C: [C1] [C2] [C3] [C4] [C5] [C6] Rs.250
Row D: [D1] [D2] [D3] [D4] [D5] [D6] Rs.250
Row E: [E1] [E2] [E3] [E4] [E5] [E6] Rs.250
       -----------------------------------
```

## Project Objective

The main objective of this project is to demonstrate a basic **console-based movie ticket booking system** using simple Python programming concepts such as functions, dictionaries, lists, loops, conditions, and file handling.
