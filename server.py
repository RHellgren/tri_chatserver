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
            'id': NEXT_ID,
            'from': user,
            'to': data['to'],
            'content': data['content'],
            'read': False,
            'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        MESSAGES.append(new_message)
        return_message = "The message is on it's way!"
        increment_id()
    else:
        return_message = "Sorry, format not supported :-("

    return return_message


@app.route('/messages/<user>/new', methods = ['GET'])
def api_get_new_messages(user):
    result = get_all_messages_for_user(user, True, None, None)
    resp = Response(result, status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<user>/all', methods = ['GET'])
def api_get_all_messages(user):
    if 'before' and 'after' in request.args:
        result = get_all_messages_for_user(user, False, request.args['after'], request.args['before'])
    else:
        result = get_all_messages_for_user(user, False, None, None)
    resp = Response(result, status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<id>', methods = ['GET'])
def api_get_message(id):
    message = get_single_message(int(id))
    if message is not None:
        resp = Response(message_json_to_string(message), status=200, mimetype='text/plain')
    else:
        resp = Response("No message with that ID\n", status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<id>/remove', methods = ['GET'])
def api_remove_message(id):
    message = get_single_message(int(id))
    if message is not None:
        MESSAGES.remove(message)
        resp = Response("Message deleted\n", status=200, mimetype='text/plain')
    else:
        resp = Response("No message with that ID\n", status=200, mimetype='text/plain')
    return resp


def get_single_message(id):
    for message in MESSAGES:
        print(message['id'])
        if message['id'] == id:
            return message
    return None


def get_all_messages_for_user(user, only_unread, after, before):
    list_of_messages = [];

    # Get all messages for this user
    for message in MESSAGES:
        if message['to'] == user:
            list_of_messages.append(message)

    # Filter out new messages, if applicable
    if only_unread:
        for message in list_of_messages:
            if message['read'] == True:
                list_of_messages.remove(message)

    # Filter out messages outside of the timerange
    if after is not None and before is not None:
        after_datetime = datetime.datetime.strptime(after, '%Y-%m-%dT%H:%M:%S')
        before_datetime = datetime.datetime.strptime(before, '%Y-%m-%dT%H:%M:%S')
        print(after_datetime)
        print(before_datetime)
        for message in list_of_messages:
            message_datetime = datetime.datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S')
            if message_datetime < after_datetime or message_datetime > before_datetime:
                list_of_messages.remove(message)
                print("removed: ")
                print(message_datetime)
            else:
                print("kept: ")
                print(message_datetime)

    # Build returnstring
    string_of_messages = ""
    list_of_messages.reverse()
    for message in list_of_messages:
        string_of_messages += message_json_to_string(message) + "\n"

    return string_of_messages


def message_json_to_string(message):
    result = message['from'] + " wrote:\n"
    result += message['content'] + "\n"
    result += "Message id: " + json.dumps(message['id']) + " sent on " + message['timestamp'] + "\n"
    message['read'] = True

    return result


def increment_id():
    global NEXT_ID
    NEXT_ID += 1


if __name__ == '__main__':
    global MESSAGES
    global NEXT_ID
    MESSAGES = []
    NEXT_ID = 0
    app.run()