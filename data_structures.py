# ============================================================
#  data_structures.py
#  Pure Python implementations of DS concepts from the lab
#  (Singly Linked List, Stack, Queue, Hashing, Sorting)
# ============================================================


# ─── SINGLY LINKED LIST ──────────────────────────────────────
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """Used to store the train route (stations in order)."""

    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self._size += 1

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def contains(self, data):
        cur = self.head
        while cur:
            if cur.data == data:
                return True
            cur = cur.next
        return False

    def __len__(self):
        return self._size


# ─── STACK ───────────────────────────────────────────────────
class Stack:
    """Used for booking history / undo operations."""

    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def to_list(self):
        return list(reversed(self._data))


# ─── QUEUE ───────────────────────────────────────────────────
class Queue:
    """Used as a waiting / cancellation queue."""

    def __init__(self):
        self._data = []

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def to_list(self):
        return list(self._data)


# ─── HASH TABLE ──────────────────────────────────────────────
class HashTable:
    """
    Simple chaining hash table.
    Used to store & look up bookings by PNR.
    """

    def __init__(self, capacity=64):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        idx = self._hash(key)
        for i, (k, _) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))
        self._size += 1

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._hash(key)
        for i, (k, _) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx].pop(i)
                self._size -= 1
                return True
        return False

    def all_values(self):
        result = []
        for bucket in self.buckets:
            for _, v in bucket:
                result.append(v)
        return result

    def __len__(self):
        return self._size


# ─── SORTING ─────────────────────────────────────────────────
def merge_sort(arr, key=lambda x: x):
    """
    Merge sort — O(n log n).
    Used to sort bookings by date / passenger name.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def bubble_sort(arr, key=lambda x: x):
    """Bubble sort — simple O(n²), used for small lists."""
    arr = list(arr)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
