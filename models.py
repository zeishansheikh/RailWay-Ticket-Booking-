# ============================================================
#  models.py
#  Train, Booking data classes + ReservationSystem (engine)
# ============================================================

import uuid
import datetime
from data_structures import (
    SinglyLinkedList, Stack, Queue, HashTable, merge_sort
)


# ─── DATA CLASSES ────────────────────────────────────────────
class Train:
    def __init__(self, train_id, name, departure, arrival, total_seats, price_per_seat):
        self.train_id = train_id
        self.name = name
        self.departure = departure          # string city name
        self.arrival = arrival              # string city name
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.price_per_seat = price_per_seat
        # Route stored as a Singly Linked List
        self.route = SinglyLinkedList()
        self.route.append(departure)
        self.route.append(arrival)

    def add_stop(self, city):
        """Insert an intermediate stop (appended before arrival for demo)."""
        # Re-build route: departure -> stops -> arrival
        stops = self.route.to_list()
        if city not in stops:
            stops.insert(-1, city)          # before arrival
            self.route = SinglyLinkedList()
            for s in stops:
                self.route.append(s)

    def to_dict(self):
        return {
            "train_id": self.train_id,
            "name": self.name,
            "departure": self.departure,
            "arrival": self.arrival,
            "total_seats": self.total_seats,
            "available_seats": self.available_seats,
            "price_per_seat": self.price_per_seat,
            "route": self.route.to_list(),
        }


class Booking:
    STATUS_CONFIRMED = "Confirmed"
    STATUS_WAITLISTED = "Waitlisted"
    STATUS_CANCELLED = "Cancelled"

    def __init__(self, passenger_name, passenger_id, train: Train,
                 seat_class, num_seats, journey_date):
        self.pnr = "PNR" + str(uuid.uuid4())[:8].upper()
        self.passenger_name = passenger_name
        self.passenger_id = passenger_id
        self.train = train
        self.seat_class = seat_class
        self.num_seats = num_seats
        self.journey_date = journey_date
        self.booking_time = datetime.datetime.now()
        self.status = self.STATUS_CONFIRMED
        self.total_fare = num_seats * train.price_per_seat

    def to_dict(self):
        return {
            "pnr": self.pnr,
            "passenger_name": self.passenger_name,
            "passenger_id": self.passenger_id,
            "train_id": self.train.train_id,
            "train_name": self.train.name,
            "departure": self.train.departure,
            "arrival": self.train.arrival,
            "seat_class": self.seat_class,
            "num_seats": self.num_seats,
            "journey_date": str(self.journey_date),
            "booking_time": str(self.booking_time),
            "status": self.status,
            "total_fare": self.total_fare,
        }


# ─── RESERVATION SYSTEM ENGINE ───────────────────────────────
class ReservationSystem:
    """
    Core engine using:
      HashTable  → fast PNR lookup
      Stack      → booking history (undo last booking)
      Queue      → waiting list
      LinkedList → train route
      MergeSort  → sort bookings
    """

    def __init__(self):
        self._trains: dict[str, Train] = {}          # train_id → Train
        self._bookings = HashTable()                  # PNR → Booking
        self._history = Stack()                       # recent confirmed bookings
        self._waiting_queue = Queue()                 # waitlisted bookings
        self._seed_data()

    # ── Seed default trains ──────────────────────────────────
    def _seed_data(self):
        trains = [
            Train("T001", "Green Express",   "Karachi",   "Lahore",     120, 1500),
            Train("T002", "Blue Falcon",     "Lahore",    "Islamabad",   80, 900),
            Train("T003", "Red Arrow",       "Islamabad", "Peshawar",    60, 700),
            Train("T004", "Silver Star",     "Karachi",   "Quetta",     100, 1800),
            Train("T005", "Golden Crescent", "Lahore",    "Multan",      90, 800),
            Train("T006", "Desert Wind",     "Quetta",    "Islamabad",   70, 2000),
        ]
        # Add intermediate stops
        trains[0].add_stop("Hyderabad")
        trains[0].add_stop("Multan")
        trains[1].add_stop("Gujranwala")
        trains[3].add_stop("Sukkur")
        trains[5].add_stop("Dera Ghazi Khan")

        for t in trains:
            self._trains[t.train_id] = t

    # ── Train queries ────────────────────────────────────────
    def get_all_trains(self):
        return list(self._trains.values())

    def search_trains(self, departure: str, arrival: str):
        return [
            t for t in self._trains.values()
            if t.departure.lower() == departure.lower()
            and t.arrival.lower() == arrival.lower()
        ]

    def get_train(self, train_id: str):
        return self._trains.get(train_id)

    # ── Booking ──────────────────────────────────────────────
    def book_ticket(self, passenger_name, passenger_id, train_id,
                    seat_class, num_seats, journey_date):
        train = self._trains.get(train_id)
        if not train:
            return None, "Train not found."

        booking = Booking(passenger_name, passenger_id, train,
                          seat_class, num_seats, journey_date)

        if train.available_seats >= num_seats:
            train.available_seats -= num_seats
            booking.status = Booking.STATUS_CONFIRMED
            self._bookings.insert(booking.pnr, booking)
            self._history.push(booking)          # push to stack
            return booking, "Booking confirmed!"
        else:
            booking.status = Booking.STATUS_WAITLISTED
            self._bookings.insert(booking.pnr, booking)
            self._waiting_queue.enqueue(booking)  # enqueue to waiting list
            return booking, f"Seats full. Added to waitlist (position {self._waiting_queue.size()})."

    # ── Cancel & promote from queue ──────────────────────────
    def cancel_ticket(self, pnr: str):
        booking = self._bookings.get(pnr)
        if not booking:
            return False, "PNR not found."
        if booking.status == Booking.STATUS_CANCELLED:
            return False, "Already cancelled."

        old_status = booking.status
        booking.status = Booking.STATUS_CANCELLED

        if old_status == Booking.STATUS_CONFIRMED:
            booking.train.available_seats += booking.num_seats
            # Promote from waiting queue if seats freed
            self._promote_from_queue(booking.train, booking.num_seats)

        return True, f"Booking {pnr} cancelled."

    def _promote_from_queue(self, train: Train, freed: int):
        promoted = []
        temp = []
        while not self._waiting_queue.is_empty():
            w = self._waiting_queue.dequeue()
            if (w.train.train_id == train.train_id
                    and w.status == Booking.STATUS_WAITLISTED
                    and w.num_seats <= freed):
                w.status = Booking.STATUS_CONFIRMED
                train.available_seats -= w.num_seats
                freed -= w.num_seats
                self._history.push(w)
                promoted.append(w)
            else:
                temp.append(w)
        for item in temp:
            self._waiting_queue.enqueue(item)
        return promoted

    # ── PNR lookup ───────────────────────────────────────────
    def get_booking(self, pnr: str):
        return self._bookings.get(pnr)

    # ── Undo last booking ────────────────────────────────────
    def undo_last_booking(self):
        if self._history.is_empty():
            return None, "No booking history."
        last = self._history.pop()
        if last.status == Booking.STATUS_CONFIRMED:
            ok, msg = self.cancel_ticket(last.pnr)
            return last, f"Undone: {msg}"
        return last, "Last booking was already cancelled/waitlisted."

    # ── All bookings (sorted) ────────────────────────────────
    def get_all_bookings(self, sort_by="booking_time"):
        all_b = self._bookings.all_values()
        if sort_by == "passenger_name":
            return merge_sort(all_b, key=lambda b: b.passenger_name.lower())
        elif sort_by == "journey_date":
            return merge_sort(all_b, key=lambda b: str(b.journey_date))
        elif sort_by == "fare":
            return merge_sort(all_b, key=lambda b: b.total_fare)
        else:
            return merge_sort(all_b, key=lambda b: str(b.booking_time))

    # ── Waiting queue ────────────────────────────────────────
    def get_waiting_list(self):
        return self._waiting_queue.to_list()

    # ── Stats ────────────────────────────────────────────────
    def stats(self):
        all_b = self._bookings.all_values()
        confirmed = [b for b in all_b if b.status == Booking.STATUS_CONFIRMED]
        cancelled = [b for b in all_b if b.status == Booking.STATUS_CANCELLED]
        waitlisted = [b for b in all_b if b.status == Booking.STATUS_WAITLISTED]
        total_revenue = sum(b.total_fare for b in confirmed)
        return {
            "total_bookings": len(all_b),
            "confirmed": len(confirmed),
            "cancelled": len(cancelled),
            "waitlisted": len(waitlisted),
            "total_revenue": total_revenue,
            "history_depth": self._history.size(),
        }
