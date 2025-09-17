"""Utilities for using in the api"""


def get_api_key() -> str:
    """Get the API key from file"""
    with open('gg_api_key', 'r') as gg_api_key_file:
        api_key = gg_api_key_file.read()
    return api_key
