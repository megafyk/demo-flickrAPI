# Download images using flickr api

App downloads highest resolution flickr images which allowed permission by owner

## Features

- Download link one by one
- Download multiple links set in file

## Installation

App requires **[python 3.x](https://www.python.org)** to run.

1. In **src/data** config json value in 2 file.

    - api_data.json

    ```json
    {
        "api_key": "Your Api Key",
        "api_secret": "Your Api Secret",
        "api_url": "https://api.flickr.com/services/rest/"
    }
    ```
    - app_data.json

    ```json
    {
        "path_saved":"Your Path Saver"
    }
    ```

2. Install enviroment and packages and start app.

    ```sh
    pip install -r requirements.txt
    cd src
    python main.py
    ```