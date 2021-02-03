from users.request import create_user, get_all_users, get_single_user, logged_user
from posts import get_all_posts, get_single_post, delete_post, get_users_post, create_post, update_post
from categories import get_all_categories, create_new_category
from tags import get_all_tags, create_tag
from users.request import create_user
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
# from users.request import create_user
# from posts import get_all_posts, get_single_post, delete_post
from users.request import create_user, get_all_users, get_single_user, logged_user


class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:

            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return (resource, key, value)

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

        return (resource, id)

# Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in variable
        parsed = self.parse_url(self.path)

        #
        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"    

                    
            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"
            elif resource == "categories":
                if id is not None:
                    response = {"Get category by id needed"}
                else:
                    response = f"{get_all_categories()}"
            elif resource == "tags":
                if id is not None:
                    response = {"Get tag by id needed"}
                else:
                    response = f"{get_all_tags()}"

        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "user_id" and resource == "posts":
                response = get_users_post(value)

        self.wfile.write(response.encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

    # rest of the elif's
        if resource == "posts":
            success = update_post(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_entry = None

        if resource == "register":
            new_entry = create_user(post_body)
        elif resource == "login":
            new_entry = logged_user(post_body)
        if resource == "tags":
            new_entry = create_tag(post_body)
        if resource == "categories":
            new_entry = create_new_category(post_body)
        elif resource == "posts":
            new_entry = create_post(post_body)

        self.wfile.write(f"{new_entry}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # parsing the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            delete_post(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
