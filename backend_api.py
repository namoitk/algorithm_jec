import random
import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame
from PIL import Image, ImageTk
import os

# Define image folder path
image_folder = r"C:\Users\ittik\OneDrive\Desktop\nba.logos"

def load_team_image(team_name):
    image_name = team_name.replace(" ", "_") + ".png"
    image_path = os.path.join(image_folder, image_name)

    try:
        img = Image.open(image_path)
        img = img.resize((80, 80), Image.LANCZOS)  # Resize to a uniform size
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print(f"Error: Image for {team_name} not found at {image_path}.")
        default_image = Image.new('RGB', (80, 80), color='gray')
        return ImageTk.PhotoImage(default_image)

def insertion_sort(arr):
    i = 1
    while i < len(arr):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        i += 1
    return arr

# Sample team data
team_ratings = {
    "Boston Celtics": 95,
    "New York Knicks": 85,
    "Milwaukee Bucks": 90,
    "Cleveland Cavaliers": 88,
    "Orlando Magic": 80,
    "Indiana Pacers": 82,
    "Philadelphia 76ers": 89,
    "Miami Heat": 86,
    "Chicago Bulls": 84,
    "Atlanta Hawks": 83,
    "Brooklyn Nets": 87,
    "Toronto Raptors": 81,
    "Charlotte Hornets": 78,
    "Washington Wizards": 77,
    "Detroit Pistons": 79,
    "Oklahoma City Thunder": 84,
    "Denver Nuggets": 88,
    "Minnesota Timberwolves": 80,
    "LA Clippers": 86,
    "Dallas Mavericks": 85,
    "Phoenix Suns": 82,
    "New Orleans Pelicans": 79,
    "Los Angeles Lakers": 90,
    "Sacramento Kings": 78,
    "Golden State Warriors": 92,
    "Houston Rockets": 83,
    "Utah Jazz": 81,
    "Memphis Grizzlies": 80,
    "San Antonio Spurs": 84,
    "Portland Trail Blazers": 82
}

eastern_team = [
    "Boston Celtics", "New York Knicks", "Milwaukee Bucks", "Cleveland Cavaliers", 
    "Orlando Magic", "Indiana Pacers", "Philadelphia 76ers", "Miami Heat", 
    "Chicago Bulls", "Atlanta Hawks", "Brooklyn Nets", "Toronto Raptors", 
    "Charlotte Hornets", "Washington Wizards", "Detroit Pistons"
]

western_team = [
    "Oklahoma City Thunder", "Denver Nuggets", "Minnesota Timberwolves", 
    "LA Clippers", "Dallas Mavericks", "Phoenix Suns", "New Orleans Pelicans", 
    "Los Angeles Lakers", "Sacramento Kings", "Golden State Warriors", 
    "Houston Rockets", "Utah Jazz", "Memphis Grizzlies", "San Antonio Spurs", 
    "Portland Trail Blazers"
]

def simulate_set(team1, team2):
    score1 = random.randint(20, 30) + team_ratings[team1] // 10
    score2 = random.randint(20, 30) + team_ratings[team2] // 10
    
    if score1 > score2:
        return 1, 0 
    elif score2 > score1:
        return 0, 1  
    else:
        overtime_score1 = random.randint(5, 10) + team_ratings[team1] // 20
        overtime_score2 = random.randint(5, 10) + team_ratings[team2] // 20
        if overtime_score1 > overtime_score2:
            return 1, 0  
        else:
            return 0, 1

def simulate_match(team1, team2):
    sets_team1 = 0
    sets_team2 = 0

    while sets_team1 < 4 and sets_team2 < 4:
        set_result = simulate_set(team1, team2)
        sets_team1 += set_result[0]
        sets_team2 += set_result[1]

    if sets_team1 > sets_team2:
        return [team1, team2, sets_team1, sets_team2]
    else:
        return [team2, team1, sets_team2, sets_team1]

class TournamentApp:
    def __init__(self, master):
        self.master = master
        self.master.title("NBA Tournament Simulator")

        # Create a canvas and scrollbar
        self.canvas = Canvas(master)
        self.scrollbar = Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.start_button = tk.Button(self.scrollable_frame, text="Start Tournament", command=self.run_tournament)
        self.start_button.grid(row=0, column=0, columnspan=10)

        # Dictionary to store images
        self.loaded_images = {}

    def run_tournament(self):
        eastern_selection = random.sample(eastern_team, 4)
        western_selection = random.sample(western_team, 4)
        selected_teams = eastern_selection + western_selection
        sorted_teams = insertion_sort(selected_teams)

        self.match_results = []
        self.display_matches(sorted_teams)

        winners = [match[0] for match in self.match_results]
        semifinal_winners, semifinal_losers = self.display_semifinals(winners)

        # Find the third place and final winners
        third_place = self.find_third_place(semifinal_losers)
        final_winner = self.find_final_winner(semifinal_winners)

        # After the main tournament, run the bottom four tournament
        self.run_bottom_four_tournament(semifinal_losers)

    def display_matches(self, sorted_teams):
        for i in range(4):
            match = simulate_match(sorted_teams[2 * i], sorted_teams[2 * i + 1])
            self.match_results.append(match)

            # Load images
            winning_team_img = self.load_team_image(match[0])
            losing_team_img = self.load_team_image(match[1])
            
            row = 1 + i
            # Add team names before the logos
            tk.Label(self.scrollable_frame, text=f"Match {i + 1}:").grid(row=row, column=0)
            tk.Label(self.scrollable_frame, text=match[0]).grid(row=row, column=1)  # Winner name
            tk.Label(self.scrollable_frame, image=winning_team_img).grid(row=row, column=2)  # Winner image
            tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
            tk.Label(self.scrollable_frame, text=match[1]).grid(row=row, column=4)  # Loser name
            tk.Label(self.scrollable_frame, image=losing_team_img).grid(row=row, column=5)  # Loser image
            tk.Label(self.scrollable_frame, text=f"Sets: {match[2]} - {match[3]}").grid(row=row, column=6)
            tk.Label(self.scrollable_frame, text=f"Winner: {match[0]}").grid(row=row, column=7)

            # Keep a reference to avoid garbage collection
            self.loaded_images[match[0]] = winning_team_img
            self.loaded_images[match[1]] = losing_team_img

    def load_team_image(self, team_name):
        # Check if the image is already loaded
        if team_name in self.loaded_images:
            return self.loaded_images[team_name]
        
        # Load new image
        img = load_team_image(team_name)
        self.loaded_images[team_name] = img
        return img

    def display_semifinals(self, winners):
        semifinal_results = []
        semifinal_losers = []

        for i in range(2):
            match = simulate_match(winners[2 * i], winners[2 * i + 1])
            semifinal_results.append(match)
            semifinal_losers.append(match[1])

            # Load images
            winning_team_img = self.load_team_image(match[0])
            losing_team_img = self.load_team_image(match[1])

            row = 5 + i
            tk.Label(self.scrollable_frame, text=f"Semifinal Match {i + 1}:").grid(row=row, column=0)
            tk.Label(self.scrollable_frame, text=match[0]).grid(row=row, column=1)  # Winner name
            tk.Label(self.scrollable_frame, image=winning_team_img).grid(row=row, column=2)  # Winner image
            tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
            tk.Label(self.scrollable_frame, text=match[1]).grid(row=row, column=4)  # Loser name
            tk.Label(self.scrollable_frame, image=losing_team_img).grid(row=row, column=5)  # Loser image
            tk.Label(self.scrollable_frame, text=f"Sets: {match[2]} - {match[3]}").grid(row=row, column=6)
            tk.Label(self.scrollable_frame, text=f"Winner: {match[0]}").grid(row=row, column=7)

            # Keep a reference to avoid garbage collection
            self.loaded_images[match[0]] = winning_team_img
            self.loaded_images[match[1]] = losing_team_img

        return [match[0] for match in semifinal_results], semifinal_losers

    def find_third_place(self, semifinal_losers):
        match = simulate_match(semifinal_losers[0], semifinal_losers[1])
        tk.Label(self.scrollable_frame, text=f"Third Place Match:").grid(row=7, column=0)
        tk.Label(self.scrollable_frame, text=match[0]).grid(row=7, column=1)  # Winner name
        tk.Label(self.scrollable_frame, text="vs").grid(row=7, column=3)
        tk.Label(self.scrollable_frame, text=match[1]).grid(row=7, column=4)  # Loser name
        tk.Label(self.scrollable_frame, text=f"Sets: {match[2]} - {match[3]}").grid(row=7, column=6)
        tk.Label(self.scrollable_frame, text=f"Winner: {match[0]}").grid(row=7, column=7)
        return match[0]  # Returning third place winner

    def find_final_winner(self, semifinal_winners):
        match = simulate_match(semifinal_winners[0], semifinal_winners[1])
        tk.Label(self.scrollable_frame, text=f"Final Match:").grid(row=8, column=0)
        tk.Label(self.scrollable_frame, text=match[0]).grid(row=8, column=1)  # Winner name
        tk.Label(self.scrollable_frame, text="vs").grid(row=8, column=3)
        tk.Label(self.scrollable_frame, text=match[1]).grid(row=8, column=4)  # Loser name
        tk.Label(self.scrollable_frame, text=f"Sets: {match[2]} - {match[3]}").grid(row=8, column=6)
        tk.Label(self.scrollable_frame, text=f"Winner: {match[0]}").grid(row=8, column=7)
        return match[0]  # Returning final winner

    def run_bottom_four_tournament(self, semifinal_losers):
        bottom_four_teams = semifinal_losers  # This will take the losers from the semifinals
        self.bottom_four_results = []

        # Display bottom four matches
        for i in range(2):
            match = simulate_match(bottom_four_teams[i], bottom_four_teams[i + 2])
            self.bottom_four_results.append(match)

            # Load images
            winning_team_img = self.load_team_image(match[0])
            losing_team_img = self.load_team_image(match[1])

            row = 10 + i
            tk.Label(self.scrollable_frame, text=f"Bottom Four Match {i + 1}:").grid(row=row, column=0)
            tk.Label(self.scrollable_frame, text=match[0]).grid(row=row, column=1)  # Winner name
            tk.Label(self.scrollable_frame, image=winning_team_img).grid(row=row, column=2)  # Winner image
            tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
            tk.Label(self.scrollable_frame, text=match[1]).grid(row=row, column=4)  # Loser name
            tk.Label(self.scrollable_frame, image=losing_team_img).grid(row=row, column=5)  # Loser image
            tk.Label(self.scrollable_frame, text=f"Sets: {match[2]} - {match[3]}").grid(row=row, column=6)
            tk.Label(self.scrollable_frame, text=f"Winner: {match[0]}").grid(row=row, column=7)

            # Keep a reference to avoid garbage collection
            self.loaded_images[match[0]] = winning_team_img
            self.loaded_images[match[1]] = losing_team_img

        # Display final match for bottom four
        final_match = simulate_match(self.bottom_four_results[0][0], self.bottom_four_results[1][0])
        tk.Label(self.scrollable_frame, text=f"Bottom Four Final Match:").grid(row=12, column=0)
        tk.Label(self.scrollable_frame, text=final_match[0]).grid(row=12, column=1)  # Winner name
        tk.Label(self.scrollable_frame, text="vs").grid(row=12, column=3)
        tk.Label(self.scrollable_frame, text=final_match[1]).grid(row=12, column=4)  # Loser name
        tk.Label(self.scrollable_frame, text=f"Sets: {final_match[2]} - {final_match[3]}").grid(row=12, column=6)
        tk.Label(self.scrollable_frame, text=f"Winner: {final_match[0]}").grid(row=12, column=7)

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()
