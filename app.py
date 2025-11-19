import pandas as pd
from flask import Flask, jsonify, request
import gc

# Initialize the Flask application
app = Flask(__name__)

# Load the dataset globally
try:
    # OPTIMIZATION: Only load the columns we actually need to save memory
    cols_to_keep = ['imdb_id', 'title', 'cast', 'poster_path']
    
    df = pd.read_csv('Poster_df_final.csv', usecols=cols_to_keep)
    
    # Ensure title is string for searching
    df['title'] = df['title'].astype(str)
    
    # Fill NaN values with empty strings or a placeholder to avoid JSON errors later
    # This is more memory efficient than converting the whole DF to object via .where
    df.fillna('', inplace=True)
    
    # Manually run garbage collection to free up setup memory
    gc.collect()
    
except FileNotFoundError:
    print("Error: Poster_df_final.csv not found.")
    df = pd.DataFrame(columns=['imdb_id', 'title', 'cast', 'poster_path'])

@app.route('/search_movie', methods=['GET'])
def search_movie():
    # Get the search query
    query = request.args.get('title')

    if not query:
        return jsonify({"error": "Title parameter is required"}), 400

    # Perform case-insensitive string search
    matches = df[df['title'].str.contains(query, case=False, na=False)]

    # Get top 8 results
    top_results = matches.head(8)

    output_list = []

    for _, row in top_results.iterrows():
        poster_path = row['poster_path']
        full_poster_url = None
        
        # Check if poster_path is not empty string (since we filled NaNs with '')
        if poster_path and poster_path != '':
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

        output_list.append({
            "imdb_id": row['imdb_id'],
            "title": row['title'],
            "cast": row['cast'],
            "poster_path": full_poster_url
        })

    return jsonify(output_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)