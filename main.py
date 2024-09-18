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
    while True:  # Loop to automatically attempt reconnection
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
                            # Save the position report to the database
                            await asyncio.get_event_loop().run_in_executor(executor, save_position_report, ais_message)

                    except json.JSONDecodeError as e:
                        logging.error(f"Failed to decode message: {e}")
                    except KeyError as e:
                        logging.error(f"Missing expected key: {e}")

        except (websockets.ConnectionClosedError, websockets.ConnectionClosedOK) as e:
            logging.error(f"Connection closed: {e}")
            logging.info("Attempting to reconnect in 5 seconds...")
            await asyncio.sleep(5)  # Wait before trying to reconnect

async def cleanup_old_records():
    """Deletes records older than one day."""
    one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
    await asyncio.get_event_loop().run_in_executor(executor, delete_old_records, one_day_ago)

def delete_old_records(one_day_ago):
    with transaction.atomic():
        old_records_count, _ = PositionReport.objects.filter(timestamp__lt=one_day_ago).delete()
    logging.info(f"Deleted {old_records_count} old records from the database.")

def save_position_report(ais_message):
    with transaction.atomic():
        timestamp = ais_message.get('Timestamp', datetime.now(timezone.utc))

        # Ensure timestamp is in ISO 8601 string format
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        elif not isinstance(timestamp, str):
            timestamp = datetime.now(timezone.utc).isoformat()

        # Create or update the PositionReport in the database
        PositionReport.objects.update_or_create(
            ship_id=ais_message['UserID'],
            defaults={
                'latitude': ais_message['Latitude'],
                'longitude': ais_message['Longitude'],
                'name': ais_message.get('Name', 'NIL'),
                'speed': ais_message.get('Sog', 0.0),
                'Cog': ais_message.get('Cog', 0.0),
                'timestamp': timestamp  # Ensure this is always in ISO 8601 string format
            }
        )

async def periodic_cleanup():
    """Runs the cleanup task periodically."""
    while True:
        try:
            await cleanup_old_records()
        except Exception as e:
            logging.error(f"Error during periodic cleanup: {e}")
        await asyncio.sleep(86400)  # Sleep for 24 hours

async def main():
    # Run the periodic cleanup and WebSocket connection concurrently
    await asyncio.gather(
        periodic_cleanup(),
        connect_ais_stream()
    )

if __name__ == "__main__":
    asyncio.run(main())
