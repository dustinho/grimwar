grimwar
=======

To run with ui, simply run 'python BoardUI.py' from the TK\_UI folder
Can Currently buy cards and advance turns using the '>' button

For server based play, run 'python Server.py' from the Server folder
To connect clients run 'python TKTestPlayer.py -i [ip] -n [player\_id]' from the TK\_UIv2 folder
Game starts once two clients have been connected

To use the battle simulator, first run python SimulatorServer.py, in the Server folder. Then run
python TKSimulator.py in the Simulator folder.

Tests:
pip install nose
nosetests
