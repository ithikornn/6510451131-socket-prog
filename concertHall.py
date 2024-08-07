import json

class ConcertHall:
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.slot = [["o" for _ in range(cols)] for _ in range(rows)]
        self.load_seats()

    def display_slots(self):
        print("   ",end="")
        for i in range(self.cols):
            print(i+1, end=" ")
        print("")
        for row in range(self.rows):
            print(f"{chr(65 + row)}:", end=" ")
            print(" ".join(self.slot[row]))

    def book_seat(self, row, seat, username):
        row_idx, seat_idx = self._seat_to_indices(row, seat)
        if self.slot[row_idx][seat_idx] == "o":
            self.slot[row_idx][seat_idx] = "x"
            self.save_seats(username)
            return "202 Booked"
        elif self.slot[row_idx][seat_idx] == "x":
            return "423 Already Booked"
        else:
            return "400 Bad Request"

    def load_seats(self):
        try:
            with open('seats.json', 'r') as file:
                data = json.load(file)
                for seat_name, status in data.items():
                    row_idx, seat_idx = self._seat_to_indices(seat_name[0], int(seat_name[1:]))
                    self.slot[row_idx][seat_idx] = "o" if status is None else "x"
        except (FileNotFoundError, json.JSONDecodeError):
            return "502 Error"

    def save_seats(self, username):
        seats = {self._indices_to_seat(row_idx, seat_idx): (None if seat == "o" else username)
                 for row_idx, row in enumerate(self.slot)
                 for seat_idx, seat in enumerate(row)}

        with open('seats.json', 'w') as file:
            json.dump(seats, file, indent=4)

    def _seat_to_indices(self, row, seat):
        """Convert seat name (e.g., 'A1') to row and column indices."""
        row_idx = ord(row.upper()) - 65
        seat_idx = seat - 1
        return row_idx, seat_idx

    def _indices_to_seat(self, row_idx, seat_idx):
        """Convert row and column indices to seat name (e.g., 'A1')."""
        row = chr(65 + row_idx)
        seat = seat_idx + 1
        return f"{row}{seat}"