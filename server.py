from flask import Flask, url_for, request, json, Response
import datetime, time
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/messages/<user>/write', methods = ['POST'])
def api_write_new_message(user):
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(request.data)
        new_message = {
            'id': next_id,
            'from': user,
            'to': data['to'],
            'content': data['content'],
            'read': False,
            'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        messages.append(new_message)
        return_message = "The message is on it's way!"
    else:
        return_message = "Sorry, format not supported :-("

    return return_message

@app.route('/messages/<user>/new', methods = ['GET'])
def api_get_new_messages(user):
    result = messages_for_user(user, True)
    resp = Response(result, status=200, mimetype='text/plain')
    return resp

@app.route('/messages/<user>/all', methods = ['GET'])
def api_get_all_messages(user):
    result = messages_for_user(user, False)
    resp = Response(result, status=200, mimetype='text/plain')
    return resp

def messages_for_user(user, only_unread):
    result = ""
    for message in messages:
        if message['to'] == user:
            if only_unread:
                if not message['read']:
                    result += message_json_to_string(message)
            else:
                result += message_json_to_string(message)
    return result

def message_json_to_string(message):
    result = ""

    result += message['from'] + " wrote:\n"
    result += message['content'] + "\n"
    result += "Message id: " + json.dumps(message['id']) + " sent on " + message['timestamp'] + "\n"
    message['read'] = True

    return result

if __name__ == '__main__':
    global messages, next_id
    messages = [
        {
            'id': 0,
            'from': 'Robin',
            'to': 'Hellgren',
            'content': 'This is what I want to tell you!',
            'read': False,
            'timestamp': '2017-03-19 13:08:21'
        },
        {
            'id': 1,
            'from': 'Tri',
            'to': 'Optima',
            'content': 'This is the second message',
            'read': False,
            'timestamp': '2017-03-18 11:18:00'
        },
        {
            'id': 2,
            'from': 'Robin',
            'to': 'Optima',
            'content': 'Third message coming up!',
            'read': False,
            'timestamp': '2017-02-11 03:59:59'
        }
    ]
    next_id = 3
    app.run()