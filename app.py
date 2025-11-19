import pandas as pd
from flask import Flask, jsonify, request

# Initialize the Flask application
app = Flask(__name__)

# Load the dataset globally
# We don't set index here because we need to search the 'title' column
try:
    df = pd.read_csv('Poster_df_final.csv')
    
    # Convert NaN values to None (null) so JSON serialization works correctly
    # and ensure columns are string type for searching
    df = df.where(pd.notnull(df), None)
    df['title'] = df['title'].astype(str)
    
except FileNotFoundError:
    print("Error: Poster_df_final.csv not found. Please make sure the CSV file is in the same directory.")
    df = pd.DataFrame(columns=['imdb_id', 'title', 'cast', 'poster_path'])

@app.route('/search_movie', methods=['GET'])
def search_movie():
    """
    Takes a 'title' query parameter, searches the dataframe,
    and returns the top 8 matching results with full details.
    """
    # Get the search query from parameters
    query = request.args.get('title')

    if not query:
        return jsonify({"error": "Title parameter is required"}), 400

    # Perform case-insensitive string search
    # na=False ensures we don't crash on missing titles
    matches = df[df['title'].str.contains(query, case=False, na=False)]

    # Get top 8 results
    top_results = matches.head(8)

    output_list = []

    # Iterate through the results to format them
    for _, row in top_results.iterrows():
        poster_path = row['poster_path']
        full_poster_url = None
        
        # Construct full URL if path exists
        if poster_path:
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

        output_list.append({
            "imdb_id": row['imdb_id'],
            "title": row['title'],
            "cast": row['cast'],
            "poster_path": full_poster_url
        })

    return jsonify(output_list)

if __name__ == '__main__':
    # This runs on port 5000 for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)