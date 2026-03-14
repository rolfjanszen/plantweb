import sqlite3
from flask import Flask, render_template
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime
from readStoreDb import read_and_store_ads1115, read_sinle_channel
import time
import threading

app = Flask(__name__)
DB_NAME = "../plantweb/ads1115_readings.db"

def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Pulling more data points to fill the graph nicely
    cursor.execute("SELECT timestamp, voltage, channel FROM readings ORDER BY timestamp DESC LIMIT 300")
    data = cursor.fetchall()
    conn.close()
    return data

def get_graphs(channels):
    graphs = []
    for ch_id, val in channels.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=val['x'], 
            y=val['y'], 
            mode='lines', 
            name=f'Channel {ch_id}',
            line=dict(color='blue')
        ))

        # FORMATTING THE X-AXIS
        fig.update_layout(
            title=f'Soil Moisture - Channel {ch_id}',
            xaxis=dict(
                title='Date/Time',
                tickformat='%m/%d %H:%M', # This is the "Month/Day Hour:Minute" format
                nticks=10
            ),
            yaxis_title='Voltage (V)',
            template='plotly_white'
            )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        graphs.append(graphJSON)
    return graphs

def get_chaneels(rows):
    # Initialize 3 channels
    channels = {0: {'x': [], 'y': []}, 1: {'x': [], 'y': []}, 2: {'x': [], 'y': []}}
    
    for row in rows:
        ts, volt, ch = row
        if ch in channels:
            # CONVERSION: Convert Unix timestamp to Python datetime object
            # Assuming ts is in seconds. If it's milliseconds, use ts/1000
            dt_object = datetime.fromtimestamp(ts) 
            channels[ch]['x'].append(dt_object)
            channels[ch]['y'].append(volt)
    return channels

@app.route('/')
def index():
    rows = get_data()
    channels = get_chaneels(rows)
    graphs = get_graphs(channels)

    return render_template('index.html', graphs=graphs)

@app.route('/get_data/<int:channel>', methods=['POST'])
def fetch_new_readings(channel):
    print(f"Fetching new readings for channel {channel}...")
    read_sinle_channel(channel)
    rows = get_data()
    channels = get_chaneels(rows)
    graphs = get_graphs(channels)

    return render_template('index.html', graphs=graphs)

def run_data_collection():
    while True:
        try:
       
            t,v=read_and_store_ads1115()
            
        except Exception as e:
            print(e)
        #refresh page
        time.sleep(1)
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        time.sleep(1800)

if __name__ == '__main__':

    # Start the data collection in a separate thread
    data_thread = threading.Thread(target=run_data_collection, daemon=True)
    data_thread.start()
    

    app.run(debug=True, host='0.0.0.0', port=5000)
