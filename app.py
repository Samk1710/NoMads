import streamlit as st
from agents.flight_agent import FlightAgent
from agents.hotel_agent import HotelAgent
from agents.itinerary_agent import ItineraryAgent
import os

st.title("AI Travel Planner 🤖✈️")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Where do you want to go?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Initialize Agents
    flight_agent = FlightAgent()
    hotel_agent = HotelAgent()
    itinerary_agent = ItineraryAgent()

    # Get Data
    params = parse_user_input(prompt)  # Implement input parsing
    flights = flight_agent.execute(params)
    hotels = hotel_agent.execute(params)
    activities = get_activities(params)  # Use SerpAPI Places
    
    # Generate Itinerary
    context = {
        "destination": params["to"],
        "days": params["duration"],
        "flights": flights,
        "hotels": hotels,
        "activities": activities
    }
    itinerary = itinerary_agent.execute(context)
    
    # Display
    with st.chat_message("assistant"):
        st.markdown(itinerary)
    st.session_state.messages.append({"role": "assistant", "content": itinerary})