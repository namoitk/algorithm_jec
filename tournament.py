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
        third_place_winner, fourth_place = self.find_third_place(semifinal_losers)
        final_winner, runner_up = self.find_final_winner(semifinal_winners)

        # Display rankings
        self.display_rankings(final_winner, runner_up, third_place_winner, fourth_place)

        # Determine and display the bottom four teams
        self.display_bottom_teams(sorted_teams, winners, semifinal_winners)

        # Start tournament for bottom four teams
        self.run_bottom_tournament(sorted_teams)

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
            tk.Label(self.scrollable_frame, text=f"Winner: {match[0]}").grid(row=row, column=7)  # Display winner

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
        semifinal_winners = []
        semifinal_losers = []
        for i in range(2):
            semifinal_match = simulate_match(winners[2 * i], winners[2 * i + 1])
            self.match_results.append(semifinal_match)
            semifinal_winners.append(semifinal_match[0])  # Winner
            semifinal_losers.append(semifinal_match[1])   # Loser

            # Load images
            winning_team_img = self.load_team_image(semifinal_match[0])
            losing_team_img = self.load_team_image(semifinal_match[1])

            row = 5 + i
            tk.Label(self.scrollable_frame, text=f"Semifinal {i + 1}:").grid(row=row, column=0)
            tk.Label(self.scrollable_frame, text=semifinal_match[0]).grid(row=row, column=1)  # Winner name
            tk.Label(self.scrollable_frame, image=winning_team_img).grid(row=row, column=2)  # Winner image
            tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
            tk.Label(self.scrollable_frame, text=semifinal_match[1]).grid(row=row, column=4)  # Loser name
            tk.Label(self.scrollable_frame, image=losing_team_img).grid(row=row, column=5)  # Loser image
            tk.Label(self.scrollable_frame, text=f"Sets: {semifinal_match[2]} - {semifinal_match[3]}").grid(row=row, column=6)
            tk.Label(self.scrollable_frame, text=f"Winner: {semifinal_match[0]}").grid(row=row, column=7)  # Display winner

            self.loaded_images[semifinal_match[0]] = winning_team_img
            self.loaded_images[semifinal_match[1]] = losing_team_img

        return semifinal_winners, semifinal_losers

    def find_third_place(self, semifinal_losers):
        third_place_match = simulate_match(semifinal_losers[0], semifinal_losers[1])
        self.match_results.append(third_place_match)

        third_place_winner = third_place_match[0]
        fourth_place = third_place_match[1]

        # Load images
        third_place_img = self.load_team_image(third_place_winner)
        fourth_place_img = self.load_team_image(fourth_place)

        row = 7
        tk.Label(self.scrollable_frame, text="Third Place Match:").grid(row=row, column=0)
        tk.Label(self.scrollable_frame, text=third_place_winner).grid(row=row, column=1)  # Winner name
        tk.Label(self.scrollable_frame, image=third_place_img).grid(row=row, column=2)  # Winner image
        tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
        tk.Label(self.scrollable_frame, text=f"{fourth_place}").grid(row=row, column=4)  # Loser name
        tk.Label(self.scrollable_frame, image=fourth_place_img).grid(row=row, column=5)  # Loser image
        tk.Label(self.scrollable_frame, text=f"Sets: {third_place_match[2]} - {third_place_match[3]}").grid(row=row, column=6)
        tk.Label(self.scrollable_frame, text=f"Third Place: {third_place_winner}").grid(row=row, column=7)

        return third_place_winner, fourth_place

    def find_final_winner(self, semifinal_winners):
        final_match = simulate_match(semifinal_winners[0], semifinal_winners[1])
        self.match_results.append(final_match)

        final_winner = final_match[0]
        runner_up = final_match[1]

        # Load images
        final_winner_img = self.load_team_image(final_winner)
        runner_up_img = self.load_team_image(runner_up)

        row = 8
        tk.Label(self.scrollable_frame, text="Final Match:").grid(row=row, column=0)
        tk.Label(self.scrollable_frame, text=final_winner).grid(row=row, column=1)  # Winner name
        tk.Label(self.scrollable_frame, image=final_winner_img).grid(row=row, column=2)  # Winner image
        tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
        tk.Label(self.scrollable_frame, text=f"{runner_up}").grid(row=row, column=4)  # Loser name
        tk.Label(self.scrollable_frame, image=runner_up_img).grid(row=row, column=5)  # Loser image
        tk.Label(self.scrollable_frame, text=f"Sets: {final_match[2]} - {final_match[3]}").grid(row=row, column=6)
        tk.Label(self.scrollable_frame, text=f"Champion: {final_winner}").grid(row=row, column=7)

        return final_winner, runner_up

    def display_rankings(self, champion, runner_up, third_place_winner, fourth_place):
        rankings = tk.Label(self.scrollable_frame, text="Tournament Rankings:")
        rankings.grid(row=9, column=0, columnspan=10)

        tk.Label(self.scrollable_frame, text=f"1st: {champion}").grid(row=10, column=0)
        tk.Label(self.scrollable_frame, text=f"2nd: {runner_up}").grid(row=11, column=0)
        tk.Label(self.scrollable_frame, text=f"3rd: {third_place_winner}").grid(row=12, column=0)
        tk.Label(self.scrollable_frame, text=f"4th: {fourth_place}").grid(row=13, column=0)

    def display_bottom_teams(self, sorted_teams, winners, semifinal_winners):
        bottom_teams = [team for team in sorted_teams if team not in winners and team not in semifinal_winners]

        bottom_team_matches = []
        for i in range(0, len(bottom_teams), 2):
            match = simulate_match(bottom_teams[i], bottom_teams[i + 1])
            bottom_team_matches.append(match)

            # Load images
            winning_team_img = self.load_team_image(match[0])
            losing_team_img = self.load_team_image(match[1])

            row = 14 + (i // 2)
            tk.Label(self.scrollable_frame, text=f"Bottom Match {i//2 + 1}:").grid(row=row, column=0)
            tk.Label(self.scrollable_frame, text=match[0]).grid(row=row, column=1)  # Winner name
            tk.Label(self.scrollable_frame, image=winning_team_img).grid(row=row, column=2)  # Winner image
            tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
            tk.Label(self.scrollable_frame, text=match[1]).grid(row=row, column=4)  # Loser name
            tk.Label(self.scrollable_frame, image=losing_team_img).grid(row=row, column=5)  # Loser image
            tk.Label(self.scrollable_frame, text=f"Sets: {match[2]} - {match[3]}").grid(row=row, column=6)
            tk.Label(self.scrollable_frame, text=f"Winner: {match[0]}").grid(row=row, column=7)  # Display winner

            self.loaded_images[match[0]] = winning_team_img
            self.loaded_images[match[1]] = losing_team_img

        # Conduct final match for bottom teams
        self.final_bottom_match(bottom_team_matches)

    def final_bottom_match(self, bottom_team_matches):
        # Get winners of the bottom matches
        bottom_winners = [match[0] for match in bottom_team_matches]

        if len(bottom_winners) == 2:
            final_bottom_match = simulate_match(bottom_winners[0], bottom_winners[1])
            self.match_results.append(final_bottom_match)

            final_winner = final_bottom_match[0]
            final_loser = final_bottom_match[1]

            # Load images
            final_winner_img = self.load_team_image(final_winner)
            final_loser_img = self.load_team_image(final_loser)

            row = 18  # Adjust row for the final match
            tk.Label(self.scrollable_frame, text="Bottom Teams Final Match:").grid(row=row, column=0)
            tk.Label(self.scrollable_frame, text=final_winner).grid(row=row, column=1)  # Winner name
            tk.Label(self.scrollable_frame, image=final_winner_img).grid(row=row, column=2)  # Winner image
            tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
            tk.Label(self.scrollable_frame, text=f"{final_loser}").grid(row=row, column=4)  # Loser name
            tk.Label(self.scrollable_frame, image=final_loser_img).grid(row=row, column=5)  # Loser image
            tk.Label(self.scrollable_frame, text=f"Sets: {final_bottom_match[2]} - {final_bottom_match[3]}").grid(row=row, column=6)
            tk.Label(self.scrollable_frame, text=f"Bottom Champion: {final_winner}").grid(row=row, column=7)

            # Losers from Bottom Match 1 and Bottom Match 2 go head-to-head
            loser1 = bottom_team_matches[0][1]
            loser2 = bottom_team_matches[1][1]
            third_place_match = simulate_match(loser1, loser2)

            third_place_winner = third_place_match[0]
            fourth_place = third_place_match[1]

            # Load images for the third-place match
            third_place_img = self.load_team_image(third_place_winner)
            fourth_place_img = self.load_team_image(fourth_place)

            row += 2  # Adjust row for third-place match
            tk.Label(self.scrollable_frame, text="Bottom Third Place Match:").grid(row=row, column=0)
            tk.Label(self.scrollable_frame, text=third_place_winner).grid(row=row, column=1)  # Winner name
            tk.Label(self.scrollable_frame, image=third_place_img).grid(row=row, column=2)  # Winner image
            tk.Label(self.scrollable_frame, text="vs").grid(row=row, column=3)
            tk.Label(self.scrollable_frame, text=third_place_match[1]).grid(row=row, column=4)  # Loser name
            tk.Label(self.scrollable_frame, image=fourth_place_img).grid(row=row, column=5)  # Loser image
            tk.Label(self.scrollable_frame, text=f"Sets: {third_place_match[2]} - {third_place_match[3]}").grid(row=row, column=6)
            tk.Label(self.scrollable_frame, text=f"Winner: {third_place_winner}").grid(row=row, column=7)

            # Final rankings for the bottom teams
            tk.Label(self.scrollable_frame, text="Bottom Tournament Rankings:").grid(row=row+1, column=0, columnspan=10)
            tk.Label(self.scrollable_frame, text=f"1st: {final_winner}").grid(row=row+2, column=0)
            tk.Label(self.scrollable_frame, text=f"2nd: {final_loser}").grid(row=row+3, column=0)
            tk.Label(self.scrollable_frame, text=f"3rd: {third_place_winner}").grid(row=row+4, column=0)
            tk.Label(self.scrollable_frame, text=f"4th: {fourth_place}").grid(row=row+5, column=0)

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()
