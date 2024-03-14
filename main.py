from flask import Flask
import requests
import json
import threading
import time
import warnings
import logging
from rich.console import Console
from rich.table import Table
from rich.live import Live
import os
import sys

app = Flask(__name__)
console = Console()

logging.getLogger('werkzeug').setLevel(logging.WARNING)

current_zone_name_global = "Initializing..."
next_zone_name_global = "Initializing..."
live_display = None

def start_live_display():
    global live_display
    table = Table(show_header=False, box=None)
    table.add_row("Checking for updates...", style="red")
    live_display = Live(table, console=console, refresh_per_second=10)
    live_display.start()

@app.route('/')
def home():
    return """
    <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Inter', sans-serif;
                    font-size: 1.5rem;
                    color: #FFFFFF;
                    text-transform: uppercase;
                    font-weight: 600;
                }
                .zone-header {
                    text-transform: uppercase;
                    margin-bottom: 0;
                }
                .current-zone, .next-zone {
                    display: block;
                    margin: 10px 0;
                }
                .current-zone {
                    color: #4cd137;
                }
                .next-zone {
                    color: #fbc531;
                }
            </style>
        </head>
        <body>
            <div class="zone-container">
                <span class="zone-header current-zone">Current Zone:</span>
                <span id="currentZone">{current_zone_name_global}</span>
                <span class="zone-header next-zone">Next Zone:</span>
                <span id="nextZone">{next_zone_name_global}</span>
            </div>

            <script>
                function fetchData() {
                    fetch('/update').then(response => response.json()).then(data => {
                        document.getElementById('currentZone').textContent = data.current_zone_name;
                        document.getElementById('nextZone').textContent = data.next_zone_name;
                    });
                }
                setInterval(fetchData, 60000);
                fetchData();
            </script>
        </body>
    </html>
    """

@app.route('/update')
def update():
    return {
        "current_zone_name": current_zone_name_global,
        "next_zone_name": next_zone_name_global
    }

def load_zone_mappings():
    with open("zones.json", "r") as file:
        return json.load(file)

zone_mapping = load_zone_mappings()

def fetch_terror_zone_data():
    url = 'https://www.d2emu.com/api/v1/tz'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        def get_zone_data_from_ids(ids_list):
            for zone_id in ids_list:
                zone_data = zone_mapping.get(zone_id)
                if zone_data:
                    return zone_data
            return {"location": f"Zone {ids_list[0]}"}

        current_zone_data = get_zone_data_from_ids(data['current'])
        next_zone_data = get_zone_data_from_ids(data['next'])

        global current_zone_name_global
        global next_zone_name_global
        current_zone_name_global = current_zone_data.get("location")
        next_zone_name_global = next_zone_data.get("location")

        table = Table(show_header=False, box=None)
        table.add_row("Current Zone:", current_zone_name_global, style="green")
        table.add_row("Next Zone:", next_zone_name_global, style="yellow")
        if live_display:
            live_display.update(table)

    except requests.exceptions.RequestException as e:
        console.log(f"Error fetching terror zone data: {e}")

def main_loop():
    start_live_display()
    while True:
        fetch_terror_zone_data()
        time.sleep(60)  # Fetch data every minute

# Run the main loop in a separate thread to avoid blocking Flask
thread = threading.Thread(target=main_loop)
thread.start()

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=6060)

