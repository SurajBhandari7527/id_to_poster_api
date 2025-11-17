import pandas as pd
from flask import Flask, jsonify, request

# Initialize the Flask application
app = Flask(__name__)

# Load the dataset from a CSV file
try:
    df = pd.read_csv('Poster_df_final.csv')
    # Set the imdb_id as the index for faster lookups
    df.set_index('imdb_id', inplace=True)
    dataset = df.to_dict(orient='index')
except FileNotFoundError:
    print("Error: your_dataset.csv not found. Please make sure the CSV file is in the same directory.")
    dataset = {}

@app.route('/get_poster', methods=['GET'])
def get_poster():
    """
    Takes an imdb_id and returns the full poster URL.
    """
    # Get the imdb_id from the query parameters
    imdb_id = request.args.get('imdb_id')

    if not imdb_id:
        return jsonify({"error": "imdb_id parameter is required"}), 400

    # Find the movie in our dataset
    movie_data = dataset.get(imdb_id)

    if movie_data:
        poster_path = movie_data.get('poster_path')
        # Check if poster_path is not null/NaN
        if pd.notna(poster_path):
            # Construct the full poster path URL
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return jsonify({"poster_path": full_poster_url})
        else:
            return jsonify({"error": "Poster path not found for this IMDB ID"}), 404
    else:
        return jsonify({"error": "IMDB ID not found"}), 404

if __name__ == '__main__':
    # This block is for local development only.
    # When deployed with Gunicorn, this will not be executed.
    app.run(host='0.0.0.0', port=5000, debug=True)