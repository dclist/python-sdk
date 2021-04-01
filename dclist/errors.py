"""
GQL-API wrapper errors module
~~~~~~~~~~~~~~~~~~~
A gql wrapper errors module for the dclist.net API.
:copyright: (c) 2021-present ilkergzlkkr
:license: MIT, see LICENSE for more details.
"""

class DCListException(Exception):
    """Base exception class for dclistpy.
    
    
    This could be caught to handle any exceptions thrown from this library.
    """
    pass

class ClientException(DCListException):
    """Exception that is thrown when an operation in the :class:`DCLClient` fails.

    These are usually for exceptions that happened due to user input.
    """
    pass

class NoTokenProvided(DCListException):
    """Exception that's thrown when no API Token is provided.

    Subclass of :exc:`DCListException`
    """
    pass

class HTTPException(DCListException):
    """Exception that's thrown when an HTTP request operation fails.

    Attributes
    ----------
    response: `aiohttp.ClientResponse`
        The response of the failed HTTP request.
    text: str
        The text of the error. Could be an empty string.
    """

    def __init__(self, response, message):
        self.response = response
        if isinstance(message, dict):
            self.text = message.get('message', '')
            self.code = message.get('extensions', {}).get('code', 0)
        else:
            self.text = message

        fmt = f"{self.text} (status code: {getattr(self, 'code', 0) or self.text})"

        super().__init__(fmt)

class Unauthorized(HTTPException):
    """Exception that's thrown for when unauthorized exception occurs.

    Subclass of :exc:`HTTPException`
    """
    pass