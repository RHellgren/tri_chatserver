from flask import Flask, url_for, request, json, Response
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/messages/<user>/all', methods = ['GET'])
def api_all_messages(user):
    result = "";
    for message in messages:
        if message['to'] == user:
            result += message['from'] + " wrote:\n"
            result += message['content'] + "\n"
            result += "Message id: " + json.dumps(message['id']) + " sent on " + message['timestamp'] + "\n"

    resp = Response(result, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'

    return resp

if __name__ == '__main__':
    global messages
    messages = [
        {
            'id': 0,
            'from': 'Robin',
            'to': 'Hellgren',
            'content': 'This is what I want to tell you!',
            'read': False,
            'timestamp': '2017-03-19T13:08:21'
        },
        {
            'id': 1,
            'from': 'Tri',
            'to': 'Optima',
            'content': 'This is the second message',
            'read': False,
            'timestamp': '2017-03-18T11:18:00'
        },
        {
            'id': 2,
            'from': 'Robin',
            'to': 'Optima',
            'content': 'Third message coming up!',
            'read': False,
            'timestamp': '2017-02-11T03:59:59'
        }
    ]
    app.run()