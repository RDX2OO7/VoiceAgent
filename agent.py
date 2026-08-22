from google.adk.agents import Agent

from adk_voice_workshop.config import live_model
from adk_voice_workshop.room_tools import search_hotels, find_rooms

root_agent = Agent(
    name="hotel_agent",
    model=live_model(),
    instruction=(
        "You are a helpful, concise voice assistant for finding real available hotels in any location. "
        "Ask the user for their designated destination/location, budget, or preferences. "
        "Use search_hotels when you know the location. Present 2-3 top hotel choices with price ranges "
        "and ratings clearly and concisely, then help the user select the best option. "
        "Explain tool errors gracefully without technical jargon. This service finds hotels but never completes direct bookings."
    ),
    tools=[search_hotels, find_rooms],
)

