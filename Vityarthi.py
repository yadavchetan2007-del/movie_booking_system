BOOKINGS_FILE = "bookings.txt"

ROWS = ["A", "B", "C", "D", "E"]
COLS = [1, 2, 3, 4, 5, 6]


def make_seats():
    seats = {}
    for row in ROWS:
        for col in COLS:
            seats[row + str(col)] = "Available"
    return seats


movies = [
    {
        "id": 1,
        "title": "Inception (Sci-Fi / Thriller)",
        "duration": "2 hrs 28 mins",
        "time": "10:30 AM",
        "silver": 150,
        "gold": 250,
        "seats": make_seats()
    },
    {
        "id": 2,
        "title": "Interstellar (Sci-Fi / Drama)",
        "duration": "2 hrs 49 mins",
        "time": "02:00 PM",
        "silver": 150,
        "gold": 250,
        "seats": make_seats()
    },
    {
        "id": 3,
        "title": "The Dark Knight (Action / Crime)",
        "duration": "2 hrs 32 mins",
        "time": "06:00 PM",
        "silver": 150,
        "gold": 250,
        "seats": make_seats()
    },
    {
        "id": 4,
        "title": "Avatar: The Way of Water (Adventure)",
        "duration": "3 hrs 12 mins",
        "time": "09:30 PM",
        "silver": 180,
        "gold": 280,
        "seats": make_seats()
    }
]

bookings = []
next_booking_id = 1001


def header(text):
    print("\n" + "=" * 65)
    print(text.center(65))
    print("=" * 65)


def pause():
    input("\nPress Enter to continue...")


def find_movie(movie_id):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None


def show_movies():
    header("MOVIES")
    print("ID   Movie                         Time        Silver  Gold")
    print("-" * 65)

    for movie in movies:
        print(f'{movie["id"]:<4} {movie["title"]:<29} '
              f'{movie["time"]:<11} Rs.{movie["silver"]:<6} Rs.{movie["gold"]}')


def show_seats(movie):
    header("SEAT LAYOUT")
    print("Movie:", movie["title"])
    print("Time :", movie["time"])
    print("Screen\n")

    available = 0

    print("        1     2     3     4     5     6")
    print("       " + "-" * 35)

    for row in ROWS:
        price = movie["silver"] if row in ["A", "B"] else movie["gold"]
        seats = ""

        for col in COLS:
            seat = row + str(col)
            if movie["seats"][seat] == "Available":
                seats += f"[{seat}] "
                available += 1
            else:
                seats += "[ X ] "

        print(f"Row {row}: {seats} Rs.{price}")

    print("       " + "-" * 35)
    print(f"Available: {available} / {len(movie['seats'])}")
    print("[A1] = Available   [ X ] = Booked")


def calculate_price(movie, seats, promo=""):
    silver_count = 0
    gold_count = 0

    for seat in seats:
        if seat[0] in ["A", "B"]:
            silver_count += 1
        else:
            gold_count += 1

    silver_total = silver_count * movie["silver"]
    gold_total = gold_count * movie["gold"]
    subtotal = silver_total + gold_total

    discount = 0
    reason = ""

    if len(seats) >= 4:
        discount = subtotal * 0.10
        reason = "Bulk discount (10%)"
    elif promo.upper() == "CINEMA10":
        discount = subtotal * 0.10
        reason = "CINEMA10 discount (10%)"

    tax = (subtotal - discount) * 0.05
    total = subtotal - discount + tax

    return {
        "silver_count": silver_count,
        "gold_count": gold_count,
        "silver_total": silver_total,
        "gold_total": gold_total,
        "subtotal": subtotal,
        "discount": discount,
        "reason": reason,
        "tax": tax,
        "total": total
    }


def print_bill(booking):
    print("\n" + "*" * 55)
    print("MOVIE TICKET".center(55))
    print("*" * 55)
    print("Booking ID :", booking["booking_id"])
    print("Name       :", booking["name"])
    print("Phone      :", booking["phone"])
    print("Movie      :", booking["movie"])
    print("Time       :", booking["time"])
    print("Seats      :", ", ".join(booking["seats"]))
    print("-" * 55)
    print(f"Subtotal   : Rs.{booking['subtotal']:.2f}")

    if booking["discount"] > 0:
        print(f"Discount   : -Rs.{booking['discount']:.2f}")

    print(f"GST (5%)   : Rs.{booking['tax']:.2f}")
    print(f"Total      : Rs.{booking['total']:.2f}")
    print("Status     :", booking["status"])
    print("*" * 55)


def save_bookings():
    try:
        with open(BOOKINGS_FILE, "w") as file:
            for b in bookings:
                seats = ",".join(b["seats"])
                line = "|".join([
                    str(b["booking_id"]),
                    b["name"],
                    b["phone"],
                    str(b["movie_id"]),
                    b["movie"],
                    b["time"],
                    seats,
                    str(b["subtotal"]),
                    str(b["discount"]),
                    str(b["tax"]),
                    str(b["total"]),
                    b["status"]
                ])
                file.write(line + "\n")
    except Exception as e:
        print("Could not save bookings:", e)


def load_bookings():
    global next_booking_id

    try:
        with open(BOOKINGS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split("|")

                if len(parts) != 12:
                    continue

                booking = {
                    "booking_id": int(parts[0]),
                    "name": parts[1],
                    "phone": parts[2],
                    "movie_id": int(parts[3]),
                    "movie": parts[4],
                    "time": parts[5],
                    "seats": parts[6].split(","),
                    "subtotal": float(parts[7]),
                    "discount": float(parts[8]),
                    "tax": float(parts[9]),
                    "total": float(parts[10]),
                    "status": parts[11]
                }

                bookings.append(booking)

                if booking["status"] == "Confirmed":
                    movie = find_movie(booking["movie_id"])
                    if movie:
                        for seat in booking["seats"]:
                            movie["seats"][seat] = "Booked"

                if booking["booking_id"] >= next_booking_id:
                    next_booking_id = booking["booking_id"] + 1

    except FileNotFoundError:
        pass
    except Exception as e:
        print("Could not load old bookings:", e)


def book_ticket():
    global next_booking_id

    header("BOOK TICKETS")
    show_movies()

    choice = input("\nEnter Movie ID (0 to cancel): ")

    if not choice.isdigit():
        print("Invalid Movie ID.")
        pause()
        return

    if int(choice) == 0:
        return

    movie = find_movie(int(choice))

    if movie is None:
        print("Movie not found.")
        pause()
        return

    show_seats(movie)

    name = input("\nEnter customer name: ").strip()
    phone = input("Enter 10-digit phone number: ").strip()

    if name == "":
        print("Name cannot be empty.")
        pause()
        return

    if not phone.isdigit() or len(phone) < 10:
        print("Please enter at least 10 digits.")
        pause()
        return

    seat_input = input("Enter seats (example: A1,A2,B3): ").upper()
    seats = [seat.strip() for seat in seat_input.split(",") if seat.strip()]

    if not seats:
        print("No seats selected.")
        pause()
        return

    if len(seats) != len(set(seats)):
        print("Same seat entered more than once.")
        pause()
        return

    for seat in seats:
        if seat not in movie["seats"]:
            print("Seat", seat, "does not exist.")
            pause()
            return

        if movie["seats"][seat] != "Available":
            print("Seat", seat, "is already booked.")
            pause()
            return

    promo = input("Enter coupon code (or press Enter): ").strip()
    price = calculate_price(movie, seats, promo)

    print("\nSubtotal :", f"Rs.{price['subtotal']:.2f}")

    if price["discount"] > 0:
        print("Discount :", f"Rs.{price['discount']:.2f}")

    print("GST      :", f"Rs.{price['tax']:.2f}")
    print("Total    :", f"Rs.{price['total']:.2f}")

    confirm = input("\nConfirm booking? (Y/N): ").upper()

    if confirm != "Y":
        print("Booking cancelled.")
        pause()
        return

    for seat in seats:
        movie["seats"][seat] = "Booked"

    booking = {
        "booking_id": next_booking_id,
        "name": name,
        "phone": phone,
        "movie_id": movie["id"],
        "movie": movie["title"],
        "time": movie["time"],
        "seats": seats,
        "subtotal": price["subtotal"],
        "discount": price["discount"],
        "tax": price["tax"],
        "total": price["total"],
        "status": "Confirmed"
    }

    bookings.append(booking)
    next_booking_id += 1
    save_bookings()

    print("\nBooking successful!")
    print_bill(booking)
    pause()


def cancel_booking():
    header("CANCEL BOOKING")

    if not bookings:
        print("No bookings found.")
        pause()
        return

    search = input("Enter Booking ID or Phone Number: ").strip()
    booking = None

    for b in bookings:
        if (str(b["booking_id"]) == search or b["phone"] == search) and b["status"] == "Confirmed":
            booking = b
            break

    if booking is None:
        print("Active booking not found.")
        pause()
        return

    print("\nBooking found:")
    print("ID    :", booking["booking_id"])
    print("Name  :", booking["name"])
    print("Movie :", booking["movie"])
    print("Seats :", ", ".join(booking["seats"]))
    print("Total :", f"Rs.{booking['total']:.2f}")

    confirm = input("Cancel this booking? (Y/N): ").upper()

    if confirm != "Y":
        print("Cancellation stopped.")
        pause()
        return

    movie = find_movie(booking["movie_id"])

    if movie:
        for seat in booking["seats"]:
            movie["seats"][seat] = "Available"

    booking["status"] = "Cancelled"
    save_bookings()

    print("Booking cancelled successfully.")
    pause()


def show_bookings():
    header("BOOKINGS")

    if not bookings:
        print("No bookings yet.")
        pause()
        return

    print("ID    Name               Seats       Total       Status")
    print("-" * 65)

    for b in bookings:
        print(f'{b["booking_id"]:<5} {b["name"]:<18} '
              f'{",".join(b["seats"]):<11} Rs.{b["total"]:<9.2f} {b["status"]}')

    choice = input("\nEnter Booking ID to print receipt, or press Enter: ").strip()

    if choice:
        for b in bookings:
            if str(b["booking_id"]) == choice:
                print_bill(b)
                break
        else:
            print("Booking ID not found.")

    pause()


def fare_calculator():
    header("TICKET PRICE CALCULATOR")
    show_movies()

    movie_id = input("\nEnter Movie ID: ")

    if not movie_id.isdigit():
        print("Invalid Movie ID.")
        pause()
        return

    movie = find_movie(int(movie_id))

    if movie is None:
        print("Movie not found.")
        pause()
        return

    silver = input("Number of Silver seats: ")
    gold = input("Number of Gold seats: ")

    silver = int(silver) if silver.isdigit() else 0
    gold = int(gold) if gold.isdigit() else 0

    if silver + gold == 0:
        print("No seats selected.")
        pause()
        return

    seats = ["A1"] * silver + ["C1"] * gold
    promo = input("Coupon code (or press Enter): ")

    price = calculate_price(movie, seats, promo)

    print("\nMovie    :", movie["title"])
    print("Silver   :", silver, "x", movie["silver"])
    print("Gold     :", gold, "x", movie["gold"])
    print("Subtotal :", f"Rs.{price['subtotal']:.2f}")

    if price["discount"] > 0:
        print("Discount :", f"Rs.{price['discount']:.2f}")

    print("GST      :", f"Rs.{price['tax']:.2f}")
    print("Total    :", f"Rs.{price['total']:.2f}")

    pause()


def main():
    load_bookings()

    while True:
        header("MOVIE TICKET BOOKING SYSTEM")
        print("1. Display Movies")
        print("2. View Seats")
        print("3. Book Tickets")
        print("4. Cancel Booking")
        print("5. Calculate Ticket Amount")
        print("6. View Bookings")
        print("7. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            show_movies()
            pause()

        elif choice == "2":
            show_movies()
            movie_id = input("\nEnter Movie ID: ")

            if movie_id.isdigit():
                movie = find_movie(int(movie_id))
                if movie:
                    show_seats(movie)
                else:
                    print("Movie not found.")
            else:
                print("Invalid Movie ID.")

            pause()

        elif choice == "3":
            book_ticket()

        elif choice == "4":
            cancel_booking()

        elif choice == "5":
            fare_calculator()

        elif choice == "6":
            show_bookings()

        elif choice == "7":
            print("Thank you for using the Movie Ticket Booking System.")
            break

        else:
            print("Invalid choice.")
            pause()


main()
