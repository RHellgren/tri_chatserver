# tri_chatserver
*Simple chat server in Python, handles GET and POST requests.*
Built to work in Python 2.7.10 with Flask 0.12 (see requirements.txt).

Simply build server with: python server.py

The following endpoints is implemented, with a short explanation and a curl example command:<br />

  *[GET]* '/messages'<br />
  Returns all messages currently in the system<br />
  > curl "http://127.0.0.1:5000/messages"
  
  *[GET]* '/messages/`<id>`'<br />
  Returns the message specified by id, or 'No message with that ID' if non existent.<br />
  > curl "http://127.0.0.1:5000/messages/0"
  
  *[GET]* '/messages/`<id>`/remove'<br />
  Removes the specified message, returns 'Message deleted' if successful<br />
  or 'Message could not be deleted, wrong id?' othewise.<br />
  > curl "http://127.0.0.1:5000/messages/0/remove"
  
  *[GET]* '/messages/`<user>`/all'<br />
  Returns all messages sent to the user specified, empty string if no messages are present in the system.<br />
  Can also filter out messages by id-range or timestamp-range (inclusive), examples shown below.<br />
  > curl "http://127.0.0.1:5000/messages/Hellgren/all"<br />
  > curl "http://127.0.0.1:5000/messages/Hellgren/all?start_index=0&end_index=3"<br />
  > curl "http://127.0.0.1:5000/messages/Hellgren/all?before=2017-03-20T10:31:45&after=2017-03-20T10:31:30"<br />
  
  *[GET]* '/messages/`<user>`/new'<br />
  Returns new messages sent to the user specified since the last update (i.e. unread messages),
  empty string if no messages are present in the system.
  > curl "http://127.0.0.1:5000/messages/Hellgren/new"
  
  *[POST]* '/messages/`<user>`/write'
  Post a new message to the system from the user specified, either takes plain-text input<br />
  (specifying the reciever with '#' sign) or JSON input, examples shown below.<br />
  > curl -H "Content-type: text/plain; charset=UTF-8" -X POST "http://127.0.0.1:5000/messages/Hellgren/write" -d "#Robin Hej Världen"<br />
  > curl -H "Content-type: application/json" -X POST "http://127.0.0.1:5000/messages/Hellgren/write" -d '{"to":"Robin", "content": "Hej världen"}'<br />
  
  *[GET]* '/messages/remove_multiple'<br />
  Removes messages within a range, specified by the arguments 'start_index' and 'end_index' (inclusive),<br />
  returns 'Messages removed' if successful and 'You need to specify which messages to remove' otherwise.<br />
  > curl "http://127.0.0.1:5000/messages/remove_multiple?start_index=0&end_index=3"<br />
