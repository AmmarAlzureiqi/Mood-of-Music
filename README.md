<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mood of Music - README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 20px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Mood of Music</h1>
    <p>Mood of Music allows users to upload an image of their environment, such as a landscape, and generate a Spotify playlist that matches the setting/theme. The generated playlist is added directly to the user's Spotify account and embedded into the webpage for immediate listening.</p>
    
    <h2>Features</h2>
    <ul>
        <li>Upload an image to generate a matching Spotify playlist.</li>
        <li>Authenticate and connect to the user's Spotify account using the Spotify API.</li>
        <li>Use OpenAI's API to analyze the image and generate playlist themes.</li>
        <li>Embed the generated playlist in the webpage for easy access.</li>
    </ul>

    <h2>Technologies Used</h2>
    <ul>
        <li>Python</li>
        <li>Flask (for the web framework)</li>
        <li>HTML, CSS, JavaScript (for the front-end)</li>
        <li>Spotipy (for interacting with the Spotify API)</li>
        <li>Docker (for containerization and deployment)</li>
        <li>OpenAI API (for image analysis and playlist generation)</li>
        <li>MySQL (for database storage)</li>
    </ul>

    <h2>Setup and Installation</h2>
    <h3>Prerequisites</h3>
    <ul>
        <li>Python 3.8 or higher</li>
        <li>Docker</li>
        <li>Spotify Developer Account with credentials</li>
        <li>OpenAI API key</li>
        <li>MySQL Database</li>
    </ul>

    <h3>Steps to Run</h3>
    <ol>
        <li>Clone the repository:
            <pre><code>git clone https://github.com/yourusername/mood-of-music.git</code></pre>
        </li>
        <li>Navigate to the project directory:
            <pre><code>cd mood-of-music</code></pre>
        </li>
        <li>Create a `.env` file and add your Spotify and OpenAI credentials:
            <pre><code>
APP_SECRET_KEY=your_secret_key
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:5001/callback
AUTH_URL=https://accounts.spotify.com/authorize
TOKEN_URL=https://accounts.spotify.com/api/token
API_BASE_URL=https://api.spotify.com/v1
OPENAI_API_KEY=your_openai_api_key
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_mysql_db_name
            </code></pre>
        </li>
        <li>Build and run the Docker container:
            <pre><code>docker-compose up --build</code></pre>
        </li>
        <li>Access the application in your web browser at <a href="http://localhost:5001">http://localhost:5001</a>.</li>
    </ol>

    <h2>Usage</h2>
    <ol>
        <li>Navigate to the home page.</li>
        <li>Log in with your Spotify account.</li>
        <li>Fill out the form with the playlist name, theme, and upload an image.</li>
        <li>Submit the form to generate the playlist.</li>
        <li>Listen to the embedded playlist on the webpage.</li>
    </ol>

    <h2>Code Overview</h2>
    <h3>main.py</h3>
    <p>This file contains the Flask application setup, routes, and logic for handling user authentication, playlist creation, and integration with the Spotify and OpenAI APIs.</p>

    <h3>utils.py</h3>
    <p>This file includes utility functions for interacting with the Spotify API, processing images, and generating descriptions and playlists using OpenAI's API.</p>


    <h2>Contact</h2>
    <p>If you have any questions, feel free to open an issue or contact me at <a href="mailto:your.email@example.com">your.email@example.com</a>.</p>
</body>
</html>
