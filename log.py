import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Example ship details (you should replace this with your actual data source)
ship_details = {
    535012096: {"name": "Ship A", "cargo_type": "General Cargo"},
    524270798: {"name": "Ship B", "cargo_type": "Oil"},
    # Add other ship details here
}

def log_ship_info(ship_id, latitude, longitude):
    # Get ship info from the dictionary, defaulting to "Unknown" if not found
    ship_info = ship_details.get(ship_id, {"name": "Unknown", "cargo_type": "Unknown"})
    name = ship_info["name"]
    cargo_type = ship_info["cargo_type"]
    
    # Log ship information
    logger.info(f"ShipId: {ship_id} Name: {name} CargoType: {cargo_type} Latitude: {latitude} Longitude: {longitude}")

def log_warning(message_type):
    # Log a warning for unexpected message types
    logger.warning(f"Unexpected message type: {message_type}")

# Example log entries
def main():
    # Example data (you should replace this with actual data processing logic)
    log_ship_info(535012096, 1.27259, 103.81886833333333)
    log_ship_info(524270798, 10.665645, 122.56704833333334)
    log_warning("[REPLACED]")

if __name__ == "__main__":
    main()
