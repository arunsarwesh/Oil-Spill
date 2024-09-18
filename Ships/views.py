from django.shortcuts import render
from Ships.models import PositionReport
import asyncio
import websockets
import json
import main
from datetime import datetime, timezone
from asgiref.sync import async_to_sync

# Define the asynchronous function to connect to AIS stream
async def connect_ais_stream():
    try:
        async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
            subscribe_message = {
                "APIKey": "a5532b9b91f2213057304d612b595a99adbca0a4",  # Required!
                "BoundingBoxes": [[[-90, -180], [90, 180]]]  # Required!
            }

            subscribe_message_json = json.dumps(subscribe_message)
            await websocket.send(subscribe_message_json)

            # Fetch data and process it
            async def fetch_data():
                async for message_json in websocket:
                    await asyncio.sleep(0)  # Add a delay (can be customized)
                    message = json.loads(message_json)
                    message_type = message["MessageType"]

                    if message_type == "PositionReport":
                        ais_message = message['Message']['PositionReport']
                        print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} "
                              f"Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']} ")

            await asyncio.wait_for(fetch_data(), timeout=10)  # Automatically disconnect after 10 seconds
    except asyncio.TimeoutError:
        print("WebSocket disconnected automatically after 10 seconds")

# Django view to handle ship data fetching and rendering it in the template
def AIS(request):
    # Call async function using async_to_sync
    # 
 

    # Fetch all position reports from the database
    reports = PositionReport.objects.all()

    # Render the reports in the 'vesel.html' template
    return render(request, 'vesel.html', {'reports': reports})

# Django view to render the map with the AIS data
def map(request):
    # Since 'main.start' is an async function, you must ensure it's properly executed
    # Here you need to manage it correctly


    # Fetch all position reports from the database
    reports = PositionReport.objects.all()
    
    # Render the map in the 'ships.html' template
    return render(request, 'ships.html', {'reports': reports})
