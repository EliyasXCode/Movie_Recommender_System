import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Step 1: TMDb API Setup
API_KEY = 'df5e4d9f1141abb4aedd02e7f5a21176'  # Replace with your actual TMDb API Key
BASE_URL = 'https://api.themoviedb.org/3/'

# Function to get movie details and recommendations using TMDb API
def get_movie_recommendations(movie_name):
    search_url = f"{BASE_URL}search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    data = response.json()
    if data['results']:
        movie_id = data['results'][0]['id']  # Get the first movie result's ID
        recommend_url = f"{BASE_URL}movie/{movie_id}/recommendations?api_key={API_KEY}"
        recommendations = requests.get(recommend_url).json()
        recommended_movies = [rec['title'] for rec in recommendations['results'][:5]]  # Get top 5 recommended movies
        return recommended_movies
    return None

# Step 2: Create the Tkinter UI
def on_recommend():
    movie_name = movie_entry.get()
    if not movie_name:
        messagebox.showwarning("Input Error", "Please enter the movie name.")
        return
    
    recommendations = get_movie_recommendations(movie_name)
    if recommendations:
        result_label.config(text="Recommended Movies:\n" + "\n".join(recommendations), fg="#FFD700")  # Gold color for text
    else:
        result_label.config(text="No recommendations found.", fg="red")

# Initialize the main window
root = tk.Tk()
root.title("Movie Recommender System")
root.geometry("500x450")
root.config(bg="#2E2E2E")  # Dark background color

# Load and resize TMDb logo image
logo_image = Image.open("tmdb_logo.png")  # Ensure 'tmdb_logo.png' is available
logo_image = logo_image.resize((120, 120), Image.LANCZOS)
tmdb_logo = ImageTk.PhotoImage(logo_image)

# Create a frame for better layout
main_frame = tk.Frame(root, bg="#2E2E2E")
main_frame.pack(pady=30)

# Display the TMDb logo
logo_label = tk.Label(main_frame, image=tmdb_logo, bg="#2E2E2E")
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Title label
title_label = tk.Label(main_frame, text="Movie Recommender System", font=("Helvetica", 20, "bold"), bg="#2E2E2E", fg="#FFD700")
title_label.grid(row=1, column=0, columnspan=2, pady=10)

# Movie name label and entry
movie_label = tk.Label(main_frame, text="Enter Movie Name:", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
movie_label.grid(row=2, column=0, pady=10, padx=20, sticky="e")
movie_entry = tk.Entry(main_frame, width=30, font=("Helvetica", 12), bg="#444444", fg="white", insertbackground='white')
movie_entry.grid(row=2, column=1, pady=10)

# Recommend Button
recommend_button = tk.Button(main_frame, text="Get Recommendations", command=on_recommend, font=("Helvetica", 12), bg="#FF5722", fg="white", activebackground="#FF8A65", activeforeground="white", relief="raised")
recommend_button.grid(row=3, column=0, columnspan=2, pady=20)

# Label to display the recommendations
result_label = tk.Label(main_frame, text="Recommended Movies:", font=("Helvetica", 14, "bold"), bg="#2E2E2E", fg="white")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
