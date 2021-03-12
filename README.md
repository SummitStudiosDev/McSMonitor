# McSMonitor

Demonstration: http://173.249.49.122:25583/

MCS Monitor is a player tracker for minecraft servers.

Powered by ChartJS, dinnerbone's mcstatus, and flask, MCS Monitor will create a chart of the number of players on a minecraft server

To setup,
clone this repo in your preferred method.

Then install all required repositories with 
```
pip install -r requirements.txt
```

To setup the server that the program tracks, simply go to **serverip.json** and change the port and server ip to your server.

If you wish to change the port that the monitor runs on, change
```python
app.run(host='0.0.0.0', port=8080)
``` 
in **main.py** to whichever port you want.
Once you are done setting up, simply run

```
python main.py
```
