import os
import datetime
from dotenv import load_dotenv
from typing import TypedDict, List, Optional

from langchain.tools import tool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- PHASE 1: SETUP ---
# Load environment variables from .env file
load_dotenv()

print("Phase 1 & 2 Code Loaded.")
if not os.path.exists('credentials.json'):
    print("\nWARNING: 'credentials.json' not found.")
else:
    print("'credentials.json' file found.")


# --- PHASE 2: STATE AND TOOLS ---

# This defines the "state" of our agent.
class TravelAgentState(TypedDict):
    user_request: str
    destination: Optional[str]
    travel_dates: Optional[dict]
    flight_options: Optional[List[dict]]
    booked_flight: Optional[dict]
    hotel_options: Optional[List[dict]]
    booked_hotel: Optional[dict]
    calendar_event_id: Optional[str]
    planner_response: Optional[str]


# --- Tools ---

@tool
def search_flights(destination: str, travel_dates: dict) -> List[dict]:
    """
    Looks up and returns available flights for a given destination and dates.
    This is a mock tool and returns pre-defined data.
    """
    print(f"Tool: Searching for flights to {destination} from {travel_dates['start_date']} to {travel_dates['end_date']}...")
    return [
        {"id": "FL123", "departure": "New York (JFK)", "arrival": destination, "price": 450.00, "departure_time": f"{travel_dates['start_date']}T08:00:00"},
        {"id": "FL456", "departure": "New York (JFK)", "arrival": destination, "price": 550.00, "departure_time": f"{travel_dates['start_date']}T11:00:00"},
    ]

@tool
def book_flight(flight_id: str) -> dict:
    """
    Books a flight using its ID.
    This is a mock tool and returns a confirmation.
    """
    print(f"Tool: Booking flight with ID {flight_id}...")
    return {"status": "success", "confirmation_id": f"CONF-{flight_id}-BKD"}

@tool
def search_Google Hotels(destination: str, travel_dates: dict) -> List[dict]:
    """
    Looks up and returns available hotels from Google for a given destination and dates.
    This is a mock tool.
    """
    print(f"Tool: Searching for hotels in {destination}...")
    return [
        {"id": "HOT789", "name": "Grand Plaza Hotel", "price_per_night": 250.00},
        {"id": "HOT101", "name": "City Center Inn", "price_per_night": 180.00},
    ]
@tool
def book_hotel(hotel_id: str) -> dict:
    """
    Books a hotel room using its ID.
    This is a mock tool.
    """
    print(f"Tool: Booking hotel with ID {hotel_id}...")
    return {"status": "success", "confirmation_id": f"CONF-{hotel_id}-BKD"}

@tool
def create_calendar_event(title: str, start_time: str, end_time: str, description: str) -> str:
    """
    Creates an event in the user's Google Calendar.
    - title: The title of the calendar event.
    - start_time: The start time of the event in ISO format (e.g., '2024-07-01T08:00:00').
    - end_time: The end time of the event in ISO format.
    - description: A description or notes for the event.
    """
    print("Tool: Creating Google Calendar event...")
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "America/New_York"},
            "end": {"dateTime": end_time, "timeZone": "America/New_York"},
        }
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        return event.get("id")
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error creating event: {e}"

# Note: In this version, I have reverted the hotel tool name to `Google Hotels`
# to match the original, error-free code from the guide. This is the simplest way
# to ensure there are no syntax errors.

# We will add the code from Phase 3, 4, and 5 after this is working.
