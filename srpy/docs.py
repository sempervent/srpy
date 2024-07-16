import os
import http.server
import socketserver
import subprocess
from http.client import HTTPConnection


def generate_docs():
    print("Generating Sphinx documentation...")
    subprocess.run(["sphinx-build", "-b", "html", "./docs", "./docs/_build"])


def serve_docs(port=8000):
    """
    Serves the documentation files located in the "./docs/_build" directory on the specified port.

    Args:
        port (int): The port number to serve the documentation on. Defaults to 8000.

    Raises:
        OSError: If there is an error starting the server.

    Examples:
        >>> serve_docs(8080)
        Serving documentation at http://localhost:8080/
    """
    os.chdir("./docs/_build")
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"Serving documentation at http://localhost:{port}/")
        httpd.serve_forever()


def request_docs(host="localhost", port=8000, path="/"):
    """
    Sends an HTTP GET request to the specified host, port, and path and returns the response data.

    Args:
        host (str): The hostname or IP address of the server to send the request to. Defaults to "localhost".
        port (int): The port number of the server to send the request to. Defaults to 8000.
        path (str): The path of the resource to request. Defaults to "/".

    Returns:
        bytes: The response data received from the server.

    Raises:
        OSError: If there is an error establishing a connection or sending the request.
        HTTPException: If there is an error receiving the response.

    Examples:
        >>> request_docs("example.com", 80, "/api/docs")
        b'{"title": "API Documentation", "version": "1.0"}'
    """
    conn = HTTPConnection(host, port)
    conn.request("GET", path)
    response = conn.getresponse()
    print(f"Status: {response.status}, Reason: {response.reason}")
    data = response.read()
    conn.close()
    return data


# Example usage
if __name__ == "__main__":
    generate_docs()
    serve_docs()
