# Chat-Application-in-Python
This is a chat application in python where users will be able to send both unicast and broadcast message. Users can have a temporary login credentials and chat with that username with others and also send broadcast message.

Usage:
To register: register:<username> (only alphabets and numbers without white spaces are valid)
To send unicast message: @<username>:<message content> 
To send braodcast message: @all:<broadcast message>


Error checks avialble for:
1) Performing any operation at start without registration.
2) Malformed usernmae
3) Not sending message in desired format
4) Sending messgae to unregistered user
5) Sending message to offline user
6) Error in content length of message during transmission
7) Error in broadcasting even if one registered client is offline. 

  If you face any issue, contact me at magicianabesh123@gmail.com
