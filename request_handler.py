import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_all_sizes, get_all_styles, get_all_orders, get_single_metal, get_single_style, get_single_size, get_single_order, create_metal, create_order, create_size, create_style, delete_metal, delete_order, delete_size, delete_style, update_metal, update_order, update_size, update_style


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """Handles GET requests to the server """
        self._set_headers(200)

        response = {}  # Default response

    # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
          if id is not None:
            response = get_single_metal(id)
          else:
            response = get_all_metals()
        if resource == "sizes":
            if id is not None:
                response = get_single_size(id)
            else:
                response = get_all_sizes()
        if resource == "styles":
            if id is not None:
                response = get_single_style(id)
            else:
                response = get_all_styles()
        if resource == "orders":
            if id is not None:
                response = get_single_order(id)
            else:
                response = get_all_orders()
                

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_resource = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "metals":
            new_resource = create_metal(post_body)
        if resource == "sizes":
            new_resource = create_size(post_body)
        if resource == "styles":
            new_resource = create_style(post_body)
        if resource == "orders":
            new_resource = create_order(post_body)
        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_resource).encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "metals":
         update_metal(id, post_body)
        if resource == "sizes":
         update_size(id, post_body)
        if resource == "styles":
         update_style(id, post_body)
        if resource == "orders":
            update_order(id, post_body)
        
        

    # Encode the new animal and send in response
        self.wfile.write("".encode())
    

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()
    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "metals":
            delete_metal(id)
        if resource == "sizes":
            delete_size(id)
        if resource == "styles":
            delete_style(id)
        if resource == "orders":
            delete_order(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())



# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
