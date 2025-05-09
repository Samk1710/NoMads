import streamlit as st
from agents import FlightAgent, HotelAgent, ActivityAgent, ItineraryAgent

st.set_page_config(page_title="Travel Itinerary Generator", layout="wide")

st.title("🧳 Travel Itinerary Planner")

with st.form("travel_form"):
    origin = st.text_input("Origin (e.g., BLR)")
    destination = st.text_input("Destination (e.g., VNO)")
    departure_date = st.date_input("Departure Date")
    return_date = st.date_input("Return Date")
    checkin = st.date_input("Hotel Check-in", value=departure_date)
    checkout = st.date_input("Hotel Check-out", value=return_date)
    days = (checkout - checkin).days
    adults = st.slider("Adults", 1, 5, 1)
    rooms = st.slider("Rooms", 1, 3, 1)
    travel_class = st.selectbox("Travel Class", ["economy", "business"])
    price_range = st.selectbox("Hotel Price Range", ["budget", "mid-range", "luxury"])
    interests = st.multiselect("Interests", ["historical", "cultural", "nature"], default=["historical"])

    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    with st.spinner("Fetching data..."):
        flight_agent = FlightAgent()
        hotel_agent = HotelAgent()
        activity_agent = ActivityAgent()
        itinerary_agent = ItineraryAgent()

        flight_data = flight_agent.execute({
            "origin": origin,
            "destination": destination,
            "departure_date": str(departure_date),
            "return_date": str(return_date),
            "adults": adults,
            "class": travel_class
        })

        hotel_data = hotel_agent.execute({
            "destination": destination,
            "checkin": str(checkin),
            "checkout": str(checkout),
            "adults": adults,
            "rooms": rooms,
            "price_range": price_range
        })

        activity_data = activity_agent.execute({
            "destination": destination,
            "days": days,
            "interests": interests
        })

        context = {
            "flights": flight_data,
            "hotels": hotel_data,
            "activities": activity_data,
            "params": {
                "destination": destination,
                "days": days,
                "adults": adults
            }
        }

        itinerary = itinerary_agent.execute(context)

    st.markdown(itinerary)
