from flask import Flask, request, json, Response
import datetime, time
app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/messages', methods=['GET'])
def api_get_all_messages():
    return_string = ""
    for message in MESSAGES:
        return_string += message_json_to_string(message) + "\n"
    resp = Response(return_string, status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<id>', methods=['GET'])
def api_get_message(id):
    message = get_single_message(int(id))
    if message is not None:
        resp = Response(message_json_to_string(message), status=200, mimetype='text/plain')
    else:
        resp = Response("No message with that ID\n", status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<id>/remove', methods=['GET'])
def api_remove_message(id):
    message = get_single_message(int(id))
    if message is not None:
        MESSAGES.remove(message)
        resp = Response("Message deleted\n", status=200, mimetype='text/plain')
    else:
        resp = Response("Message could not be deleted, wrong id?\n", status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<user>/all', methods=['GET'])
def api_get_all_user_messages(user):
    if 'before' and 'after' in request.args:
        result = get_all_messages_for_user(user, False, request.args['after'], request.args['before'], None, None)
    elif 'start_index' and 'end_index' in request.args:
        result = get_all_messages_for_user(user, False, None, None, request.args['start_index'], request.args['end_index'])
    else:
        result = get_all_messages_for_user(user, False, None, None, None, None)
    resp = Response(result, status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<user>/new', methods=['GET'])
def api_get_new_messages(user):
    result = get_all_messages_for_user(user, True, None, None, None, None)
    resp = Response(result, status=200, mimetype='text/plain')
    return resp


@app.route('/messages/<user>/write', methods=['POST'])
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
    elif request.headers['Content-Type'] == 'text/plain; charset=UTF-8':
        data = request.get_data().decode('utf-8')
        start = data.index('#') + len('#')
        end = data.index(' ', start)
        to_user = data[start:end]
        message = data[end+1:]
        new_message = {
            'id': NEXT_ID,
            'from': user,
            'to': to_user,
            'content': message,
            'read': False,
            'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        MESSAGES.append(new_message)
        return_message = "The message is on it's way!"
        increment_id()
    else:
        return_message = "Sorry, format not supported :-("

    return return_message


@app.route('/messages/remove_multiple', methods=['GET'])
def api_remove_multiple_messages():
    if 'start_index' and 'end_index' in request.args:
        global MESSAGES
        messages_to_keep = []
        start_index = int(request.args['start_index'])
        end_index = int(request.args['end_index'])
        for message in MESSAGES:
            if int(message['id']) > end_index or int(message['id']) < start_index:
                messages_to_keep.append(message)
        MESSAGES = messages_to_keep
        resp = Response("Messages removed\n", status=200, mimetype='text/plain')
    else:
        resp = Response("You need to specify which messages to remove\n", status=200, mimetype='text/plain')
    return resp


def get_single_message(id):
    for message in MESSAGES:
        if message['id'] == id:
            return message
    return None


def get_all_messages_for_user(user, only_unread, after, before, start_index_string, end_index_string):
    list_of_messages = [];

    # Get all messages for this user
    for message in MESSAGES:
        if message['to'] == user:
            list_of_messages.append(message)

    # Filter out new messages, if applicable
    if only_unread:
        filtered_list_of_messages = []
        for message in list_of_messages:
            if not message['read']:
                filtered_list_of_messages.append(message)
        list_of_messages = filtered_list_of_messages

    # Filter out messages outside of the timerange
    if after is not None and before is not None:
        filtered_list_of_messages = []
        after_datetime = datetime.datetime.strptime(after, '%Y-%m-%dT%H:%M:%S')
        before_datetime = datetime.datetime.strptime(before, '%Y-%m-%dT%H:%M:%S')
        for message in list_of_messages:
            message_datetime = datetime.datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S')
            if message_datetime > after_datetime and message_datetime < before_datetime:
                filtered_list_of_messages.append(message)
        list_of_messages = filtered_list_of_messages

    # Filter out messages outside of index range
    if start_index_string is not None and end_index_string is not None:
        start_index = int(start_index_string)
        end_index = int(end_index_string)
        filtered_list_of_messages = []
        for message in list_of_messages:
            if start_index <= int(message['id']) <= end_index:
                filtered_list_of_messages.append(message)
        list_of_messages = filtered_list_of_messages

    # Build returnstring
    string_of_messages = ""
    list_of_messages.reverse()
    for message in list_of_messages:
        string_of_messages += message_json_to_string(message) + "\n"
        mark_message_as_read(message)
    return string_of_messages


def message_json_to_string(message):
    result = message['from'] + " wrote:\n"
    result += message['content'] + "\n"
    result += "Message id: " + json.dumps(message['id']) + " sent on " + message['timestamp'] + "\n"
    return result


def mark_message_as_read(message_to_mark):
    for message in MESSAGES:
        if message['id'] == message_to_mark['id']:
            message['read'] = True


def increment_id():
    global NEXT_ID
    NEXT_ID += 1


if __name__ == '__main__':
    global MESSAGES
    global NEXT_ID
    MESSAGES = []
    NEXT_ID = 0
    app.run()