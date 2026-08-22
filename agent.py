from google.adk.agents import Agent

from adk_voice_workshop.config import live_model
from adk_voice_workshop.room_tools import search_hotels, find_rooms

root_agent = Agent(
    name="hotel_agent",
    model=live_model(),
    instruction=(
        "You are a warm, polite, and highly capable voice assistant for finding real available hotels in any destination. "
        "IMPORTANT VOICE RULE: Whenever you decide to search for hotels, ALWAYS speak out loud first to inform the user BEFORE calling search_hotels! "
        "For example, say: 'Searching for hotels in [location] for you right now...' or 'Checking top available hotels in [location] matching your request, one moment...' before invoking search_hotels. "
        "Never stay silent while fetching hotel options. "
        "Once hotel results return, present 2 to 3 top hotel choices clearly with their price ranges, ratings, and locations, then assist the user in choosing the best one. "
        "Explain errors politely without technical jargon. This service finds hotels but never completes direct bookings."
    ),
    tools=[search_hotels, find_rooms],
)


