import tkinter as tk
from tkinter import messagebox
import random

class LemonadeStandGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Lemonade Stand Game")

        # Game variables
        self.cash = 20.0
        self.water = 0
        self.cups = 0
        self.sugar = 0
        self.lemons = 0
        self.price_per_cup = 1.0
        self.weather = "Sunny"

        # Recipe
        self.recipe = {
            "water": 1,
            "sugar": 1,
            "lemons": 1
        }

        # Random events
        self.random_event = None

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        # Cash and inventory display
        self.stats_label = tk.Label(self.root, text=f"Cash: ${self.cash:.2f}")
        self.stats_label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.inventory_label = tk.Label(
            self.root,
            text=f"Inventory - Water: {self.water}, Sugar: {self.sugar}, Lemons: {self.lemons}, Cups: {self.cups}"
        )
        self.inventory_label.grid(row=1, column=0, columnspan=2, sticky="w")

        # Buying supplies
        tk.Label(self.root, text="Buy Supplies:").grid(row=2, column=0, sticky="w")

        tk.Button(self.root, text="Buy Water ($0.50)", command=lambda: self.buy("water", 0.5)).grid(row=3, column=0, sticky="w")
        tk.Button(self.root, text="Buy Sugar ($0.25)", command=lambda: self.buy("sugar", 0.25)).grid(row=4, column=0, sticky="w")
        tk.Button(self.root, text="Buy Lemons ($0.75)", command=lambda: self.buy("lemons", 0.75)).grid(row=5, column=0, sticky="w")
        tk.Button(self.root, text="Buy Cups ($0.10)", command=lambda: self.buy("cups", 0.10)).grid(row=6, column=0, sticky="w")

        # Set recipe and price
        tk.Label(self.root, text="Set Recipe (units per cup):").grid(row=7, column=0, sticky="w")

        tk.Label(self.root, text="Water:").grid(row=8, column=0, sticky="w")
        self.water_entry = tk.Entry(self.root, width=5)
        self.water_entry.grid(row=8, column=1, sticky="w")

        tk.Label(self.root, text="Sugar:").grid(row=9, column=0, sticky="w")
        self.sugar_entry = tk.Entry(self.root, width=5)
        self.sugar_entry.grid(row=9, column=1, sticky="w")

        tk.Label(self.root, text="Lemons:").grid(row=10, column=0, sticky="w")
        self.lemons_entry = tk.Entry(self.root, width=5)
        self.lemons_entry.grid(row=10, column=1, sticky="w")

        tk.Button(self.root, text="Set Recipe", command=self.set_recipe).grid(row=11, column=0, sticky="w")

        tk.Label(self.root, text="Set Price per Cup:").grid(row=12, column=0, sticky="w")
        self.price_entry = tk.Entry(self.root, width=5)
        self.price_entry.grid(row=12, column=1, sticky="w")
        tk.Button(self.root, text="Set Price", command=self.set_price).grid(row=13, column=0, sticky="w")

        # Weather and simulate day
        tk.Label(self.root, text=f"Today's Weather: {self.weather}").grid(row=14, column=0, sticky="w")

        tk.Button(self.root, text="Simulate Day", command=self.simulate_day).grid(row=15, column=0, sticky="w")

    def buy(self, item, cost):
        if self.cash >= cost:
            self.cash -= cost
            setattr(self, item, getattr(self, item) + 1)
            self.update_stats()
        else:
            messagebox.showerror("Error", "Not enough cash to buy this item!")

    def set_recipe(self):
        try:
            self.recipe["water"] = int(self.water_entry.get())
            self.recipe["sugar"] = int(self.sugar_entry.get())
            self.recipe["lemons"] = int(self.lemons_entry.get())
            messagebox.showinfo("Success", "Recipe updated!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for the recipe!")

    def set_price(self):
        try:
            self.price_per_cup = float(self.price_entry.get())
            messagebox.showinfo("Success", "Price updated!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price!")

    def simulate_day(self):
        self.random_event = self.get_random_event()
        customers = random.randint(10, 30)
        cups_sold = 0

        # Apply random event impact
        if self.random_event == "Festival Nearby":
            customers += 10
        elif self.random_event == "Bad News Spread":
            customers -= 5
        elif self.random_event == "Health Trend Boost":
            customers += 7
        elif self.random_event == "Supply Issue":
            self.water = max(0, self.water - 5)
            self.sugar = max(0, self.sugar - 5)

        for _ in range(customers):
            if self.water >= self.recipe["water"] and self.sugar >= self.recipe["sugar"] and self.lemons >= self.recipe["lemons"] and self.cups > 0:
                self.water -= self.recipe["water"]
                self.sugar -= self.recipe["sugar"]
                self.lemons -= self.recipe["lemons"]
                self.cups -= 1
                self.cash += self.price_per_cup
                cups_sold += 1

        feedback = "Great!" if cups_sold >= customers * 0.7 else "Okay." if cups_sold >= customers * 0.4 else "Poor."
        self.update_stats()
        messagebox.showinfo(
            "Day Summary",
            f"Cups sold: {cups_sold}\nFeedback: {feedback}\nRandom Event: {self.random_event if self.random_event else 'None'}"
        )

    def get_random_event(self):
        events = [
            "Festival Nearby",
            "Bad News Spread",
            "Health Trend Boost",
            "Supply Issue",
            None  # No event
        ]
        return random.choice(events)

    def update_stats(self):
        self.stats_label.config(text=f"Cash: ${self.cash:.2f}")
        self.inventory_label.config(
            text=f"Inventory - Water: {self.water}, Sugar: {self.sugar}, Lemons: {self.lemons}, Cups: {self.cups}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = LemonadeStandGame(root)
    root.mainloop()