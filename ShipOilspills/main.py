import os
import django
import asyncio
import websockets
import json
import logging
from datetime import datetime, timezone, timedelta
from django.db import transaction
from concurrent.futures import ThreadPoolExecutor

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShipOilspills.settings')  # Replace with your project's settings module
django.setup()

from Ships.models import PositionReport

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a ThreadPoolExecutor for synchronous database operations
executor = ThreadPoolExecutor()

async def connect_ais_stream():
    try:
        async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
            subscribe_message = {
                "APIKey": "d342630bda87c80c11f0cf6a34825d44e411dc36",
                "BoundingBoxes": [[[-11, 178], [30, 74]]]
            }
            await websocket.send(json.dumps(subscribe_message))

            async for message_json in websocket:
                try:
                    message = json.loads(message_json)
                    message_type = message.get("MessageType", "")

                    if message_type == "PositionReport":
                        ais_message = message['Message']['PositionReport']

                        # Save the message to the database asynchronously
                        await asyncio.get_event_loop().run_in_executor(
                            executor, 
                            save_position_report, 
                            ais_message
                        )

                        logging.info(
                            f"ShipId: {ais_message['UserID']} Name: {ais_message.get('ShipName', 'NIL')} "
                            f"CargoType: {ais_message.get('Cog', '0.0')} Latitude: {ais_message['Latitude']} "
                            f"Longitude: {ais_message['Longitude']} Speed: {ais_message.get('Sog', 0.0)}"
                        )
                    else:
                        logging.warning(f"Unexpected message type: {message_type} - {message}")

                except json.JSONDecodeError as e:
                    logging.error(f"Failed to decode message: {e}")
                except KeyError as e:
                    logging.error(f"Missing expected key: {e}")

    except websockets.ConnectionClosedError as e:
        logging.error(f"Connection closed: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

async def cleanup_old_records():
    # Calculate the cutoff date
    one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)

    # Perform deletion within an atomic transaction
    await asyncio.get_event_loop().run_in_executor(
        executor, 
        delete_old_records, 
        one_month_ago
    )

def delete_old_records(one_month_ago):
    with transaction.atomic():
        old_records_count, _ = PositionReport.objects.filter(timestamp__lt=one_month_ago).delete()

    logging.info(f"Deleted {old_records_count} old records from the database.")

def save_position_report(ais_message):
    with transaction.atomic():
        PositionReport.objects.create(
            ship_id=ais_message['UserID'],
            latitude=ais_message['Latitude'],
            longitude=ais_message['Longitude'],
            name=ais_message.get('Name', 'NIL'),  # Use default value if not present
            cargo_type=ais_message.get('CargoType', 'NIL'),  # Use default value if not present
            speed=ais_message.get('Sog', 0.0)  # Use default value if not present
        )

if __name__ == "__main__":
    # Run the cleanup before starting the WebSocket connection
    try:
        asyncio.run(cleanup_old_records())
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")

    asyncio.run(connect_ais_stream())
