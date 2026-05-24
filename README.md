# 🚆 Rail Express — Train Ticket Reservation System
## Data Structures Project (Python + Streamlit)

---

## 📁 File Structure

```
train_system/
│
├── app.py               ← Streamlit UI (run this)
├── models.py            ← ReservationSystem engine + Train/Booking classes
├── data_structures.py   ← All DS implementations (LinkedList, Stack, Queue, HashTable, MergeSort)
└── README.md            ← This file
```

---

## 🚀 How to Run

```bash
# 1. Install dependency (only needed once)
pip install streamlit pandas

# 2. Run the app
streamlit run app.py
```

Then open your browser at: **http://localhost:8501**

---

## 📚 Data Structures Used

| DS | Lab | How it's used |
|----|-----|---------------|
| Singly Linked List | Lab #02 | Stores train route stations in order |
| Stack (LIFO) | Lab #05 | Booking history + Undo last booking |
| Queue (FIFO) | Lab #07 | Waiting/cancellation list |
| Hash Table (Chaining) | Lab #11 | O(1) booking lookup by PNR |
| Merge Sort | Lab #09 | Sort bookings by name/date/fare |

---

## ✨ Features

- Search trains by departure / arrival city
- Book tickets (auto-waitlists if seats full)
- Cancel ticket (auto-promotes from waiting queue)
- Undo last booking (pops from stack)
- View & sort all bookings (merge sort)
- Dashboard with live stats
