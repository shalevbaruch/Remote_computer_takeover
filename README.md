# Remote_computer_takeover

This project is an implementation of taking over a computer remotely.
Details:
The server will be the controlling party, and the client will be the controlled party.
The project consists of three main parts:

1. The client sends screenshots to the server in a loop. The server gets the screenshots and opens them using a GUI.

2. The server listens to every event on his keyboard. 
Once he gets one, he sends the event information to the client, who receives it and does what it says.

3.The server listens to every event on his mouse, and once he gets one, he and the client do the same thing us part two.


Note: I used the SSL module so that the transfer of information between each of the parties would be secure.
For this purpose, I created a private key on the side of the server as well as a certificate for the SSL protocol.

