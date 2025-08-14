import os
import datetime
from dotenv import load_dotenv
from typing import TypedDict, List, Optional

# --- LangChain Imports ---
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

# --- Google Calendar Imports ---
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- 1. Load Environment Variables ---
# This loads your OpenAI API key from the .env file
load_dotenv()

# --- 2. Define All Tools ---
# These are the functions the agent can decide to use.

@tool
def search_flights(destination: str, travel_dates: Optional[str] = None) -> List[dict]: # <-- 1. EXPECT A STRING
    """
    Looks up and returns available flights for a given destination and optional dates.
    The travel_dates argument should be a string in the format 'YYYY-MM-DD to YYYY-MM-DD'.
    """
    print(f"\nTOOL USED: Searching for flights to {destination}...")

    # --- 2. NEW LOGIC TO PARSE THE DATE STRING ---
    start_date = (datetime.date.today() + datetime.timedelta(days=28)).strftime("%Y-%m-%d") # Default
    if travel_dates:
        try:
            # Assumes format "YYYY-MM-DD to YYYY-MM-DD"
            start_date_str, end_date_str = travel_dates.split(' to ')
            start_date = datetime.datetime.fromisoformat(start_date_str).strftime("%Y-%m-%d")
            print(f"Using parsed dates: Start - {start_date}, End - {end_date_str}")
        except ValueError:
            print("Could not parse date string, using default dates.")
    else:
        print("No travel dates provided, using default dates.")
    # --- END OF NEW LOGIC ---

    return [
        {"id": "FL123", "departure": "New York (JFK)", "arrival": destination, "price": 450.00, "departure_time": f"{start_date}T08:00:00"},
        {"id": "FL456", "departure": "New York (JFK)", "arrival": destination, "price": 550.00, "departure_time": f"{start_date}T11:00:00"},
    ]

@tool
def book_flight(flight_id: str) -> dict:
    """
    Books a flight using its ID.
    This is a mock tool and returns a confirmation.
    """
    print(f"\nTOOL USED: Booking flight with ID {flight_id}...")
    return {"status": "success", "confirmation_id": f"CONF-{flight_id}-BKD"}

@tool
def Google_Hotels(destination: str, travel_dates: Optional[str] = None) -> List[dict]:
    """
    Looks up and returns available hotels for a given destination and optional dates.
    The travel_dates argument should be a string in the format 'YYYY-MM-DD to YYYY-MM-DD'.
    """
    print(f"\nTOOL USED: Searching for hotels in {destination}...")

    # --- Logic to handle missing or string-formatted dates ---
    if travel_dates:
        try:
            # Assumes format "YYYY-MM-DD to YYYY-MM-DD"
            start_date_str, end_date_str = travel_dates.split(' to ')
            print(f"Using parsed dates for hotel search: Start - {start_date_str}, End - {end_date_str}")
        except ValueError:
            print("Could not parse date string for hotels, proceeding without specific dates.")
    else:
        print("No travel dates provided for hotel search.")
    # --- End of logic ---

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
    print(f"\nTOOL USED: Booking hotel with ID {hotel_id}...")
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
    print("\nTOOL USED: Creating Google Calendar event...")
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
        return f"Successfully created event with ID: {event.get('id')}"
    except Exception as e:
        return f"Error creating event: {e}"

# --- 3. Create the Agent ---

# Initialize the Language Model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create a list of all the tools the agent can use
tools = [search_flights, book_flight, Google_Hotels, book_hotel, create_calendar_event]

# Define the prompt template for the agent
# New, more powerful prompt with memory
agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful travel assistant. Your goal is to help the user book a flight and hotel,
            and then add the trip to their calendar.

            You have access to a conversation history with the user. Use this history to fill in any missing details in the user's latest request.
            For example, if the user already told you the destination is London, you must remember that.

            IMPORTANT: You must gather all necessary information (like destination AND dates for a flight search) from the user's request and the chat history before calling a tool.

            When you have completed all tasks, you must provide a final, comprehensive summary to the user.
            Today's date is {today}.""",
        ),
        # The 'chat_history' will be populated with past messages.
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        # The 'agent_scratchpad' is for the agent's internal thoughts and tool outputs for the current step.
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
).partial(today=datetime.date.today())

# Create the agent itself by combining the LLM, the prompt, and the tools
agent = create_openai_tools_agent(llm, tools, agent_prompt)

# The AgentExecutor is the runtime that makes the agent work.
# It handles the loop of calling the agent, running tools, and feeding the output back to the agent.
# `verbose=True` will print out the agent's thoughts, which is very helpful for seeing how it works.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
