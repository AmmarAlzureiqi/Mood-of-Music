# from dotenv import load_dotenv
# from pprint import pprint
# import requests
# import os

# load_dotenv()


# if __name__ == "__main__":

#     print('Hello')


class Playlist:
    """Playlist represents a Spotify playlist."""

    def __init__(self, name, id):
        """
        :param name (str): Playlist name
        :param id (int): Spotify playlist id
        """
        self.name = name
        self.id = id

    def __str__(self):
        return f"Playlist: {self.name}"