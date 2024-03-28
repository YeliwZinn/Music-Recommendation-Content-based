from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

# Loading models (assuming 'songs.pkl' and 'similarities.pkl' exist)
try:
    df = pd.read_pickle('songs.pkl')
    similarities = pd.read_pickle('similarities.pkl')
except FileNotFoundError:
    print("Error: Data files 'songs.pkl' or 'similarities.pkl' not found.")
    exit(1)

class ContentBasedRecommender:
    def __init__(self, matrix):
        self.matrix_similar = matrix
    
    def _print_message(self, song, recom_song):
        rec_items = len(recom_song)

        print(f'The {rec_items} recommended songs for {song} are:')
        for i in range(rec_items):
            print(f"Number {i+1}:")
            print(f"{recom_song[i][1]} by {recom_song[i][2]} with {round(recom_song[i][0], 3)} similarity score")
            print("--------------------")

    def recommendation(self, song, number_songs):
        # Error handling: Check if song exists in data
       
        # Get recommended song indices
        recom_song = self.matrix_similar[song][:number_songs]

        # Get recommended songs using indices (avoids string indexing errors)
        recom_song = self.matrix_similar[song][:number_songs]
        self._print_message(song=song, recom_song=recom_song)
        return recom_song

recommender = ContentBasedRecommender(similarities)

# Flask app
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    # Get song names from the DataFrame
    names = df['song'].values
    return render_template('index.html', names=names)


@app.route('/recom', methods=['POST'])
def recom():
    user_song = request.form.get('names')
    if not user_song:
        return render_template('index.html', error="Please select a song.")

    try:
        # Recommend songs and handle potential errors
        recommended_songs = recommender.recommendation(user_song, 5)  # Assuming you want 5 recommendations
    except Exception as e:
        # Provide informative error message to the user
        return render_template('index.html', error=f"Error: {str(e)}")

    return render_template('index.html', user_song=user_song, recommended_songs=recommended_songs)

# Python execution
if __name__ == "__main__":
    app.run(debug=True)
