# PACS Backend prototype

To run the backend you need to change a link to node in `node.py`, constants in `server.py` and `monitor.py`. 
Then install the requirements from `requirements.txt` and start `monitor.py` and then `server.py` scripts.
The `monitor.py` looks for transactions calling a contract in the blockchain and saves them to the database, and the `server.py` allows you to read adds and marks JSON data from this database.
