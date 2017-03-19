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
    list_of_messages = [];
    for message in messages:
        if message['to'] == user:
            if only_unread:
                if not message['read']:
                    list_of_messages.append(message_json_to_string(message))
            else:
                list_of_messages.append(message_json_to_string(message))

    string_of_messages = ""
    list_of_messages.reverse()
    for message in list_of_messages:
        string_of_messages += message + "\n"

    return string_of_messages

def message_json_to_string(message):
    result = message['from'] + " wrote:\n"
    result += message['content'] + "\n"
    result += "Message id: " + json.dumps(message['id']) + " sent on " + message['timestamp'] + "\n"
    message['read'] = True

    return result

if __name__ == '__main__':
    global messages, next_id
    messages = []
    next_id = 3
    app.run()