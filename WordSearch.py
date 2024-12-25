import tkinter as tk
from tkinter import messagebox, scrolledtext

class WordSearchSolver:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.directions = [
            (0, 1),   # right
            (1, 0),   # down
            (0, -1),  # left
            (-1, 0),  # up
            (1, 1),   # down-right
            (1, -1),  # down-left
            (-1, 1),  # up-right
            (-1, -1)  # up-left
        ]

    def search_word(self, word):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == word[0]:  # Check if the first letter matches
                    for dr, dc in self.directions:
                        if self._search_from(r, c, dr, dc, word):
                            return (r, c)  # Return the starting position of the found word
        return None  # Word not found

    def _search_from(self, r, c, dr, dc, word):
        for i in range(len(word)):
            nr, nc = r + i * dr, c + i * dc
            if not (0 <= nr < self.rows and 0 <= nc < self.cols) or self.grid[nr][nc] != word[i]:
                return False
        return True

    def find_words(self, words):
        found_words = {}
        for word in words:
            position = self.search_word(word)
            if position:
                found_words[word] = position
        return found_words


class WordSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search Solver")

        # Grid input
        self.grid_label = tk.Label(root, text="Enter the grid (one row per line):")
        self.grid_label.pack()

        self.grid_text = scrolledtext.ScrolledText(root, width=40, height=10)
        self.grid_text.pack()

        # Words input
        self.words_label = tk.Label(root, text="Enter words to search (one per line):")
        self.words_label.pack()

        self.words_text = scrolledtext.ScrolledText(root, width=40, height=5)
        self.words_text.pack()

        # Solve button
        self.solve_button = tk.Button(root, text="Solve", command=self.solve)
        self.solve_button.pack()

        # Result display
        self.result_label = tk.Label(root, text="Results:")
        self.result_label.pack()

        self.result_text = scrolledtext.ScrolledText(root, width=40, height=10)
        self.result_text.pack()

    def solve(self):
        # Clear previous results
        self.result_text.delete(1.0, tk.END)

        # Get grid input
        grid_input = self.grid_text.get("1.0", tk.END).strip().splitlines()
        grid = [list(row.strip().upper()) for row in grid_input if row.strip()]

        # Get words input
        words_input = self.words_text.get("1.0", tk.END).strip().splitlines()
        words = [word.strip().upper() for word in words_input if word.strip()]

        if not grid or not words:
            messagebox.showwarning("Input Error", "Please enter both grid and words.")
            return

        # Solve the word search
        solver = WordSearchSolver(grid)
        results = solver.find_words(words)

        # Display results
        if results:
            for word, position in results.items():
                self.result_text.insert(tk.END, f"Word '{word}' found at position: {position}\n")
        else:
            self.result_text.insert(tk.END, "No words found.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = WordSearchApp(root)
    root.mainloop()