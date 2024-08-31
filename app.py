import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import *

class RequestHandler(BaseHTTPRequestHandler):
    def do_get(self):
        if self.path == '/todos':
            tasks = get_all_tasks()
            response = json.dumps([{'id': row[0], 'task': row[1], 'completed': bool(row[2])} for row in tasks])
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_post(self):
        if self.path == '/todos':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            task = data.get('task')
            if task:
                task_id = create_task(task)
                response = json.dumps({'message': 'Task created', 'id': task_id})
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_response(400)
                self.end_headers()

    def do_put(self):
        if self.path.startswith('/todos/'):
            task_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode())
            task = data.get('task')
            completed = data.get('completed')
            if task and completed is not None:
                update_task(task_id, task, completed)
                response = json.dumps({'message': 'Task updated'})
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_delete(self):
        if self.path.startswith('/todos/'):
            task_id = self.path.split('/')[-1]
            delete_task(task_id)
            response = json.dumps({'message': 'Task deleted'})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    create_table()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
