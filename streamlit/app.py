import streamlit as st
from joblib import load
import pandas as pd
import datetime

model = load('models/dt_regressor.joblib')
table = pd.read_csv('table/table.csv')

def preprocess_input(starting_airport, destination_airport, departure_date, departure_time, cabin_type):
    # Map Airports
    airports = {'ATL': 0,
                'BOS': 1,
                'CLT': 2,
                'DEN': 3,
                'DFW': 4,
                'DTW': 5,
                'EWR': 6,
                'IAD': 7,
                'JFK': 8,
                'LAX': 9,
                'LGA': 10,
                'MIA': 11,
                'OAK': 12,
                'ORD': 13,
                'PHL': 14,
                'SFO': 15
                }
    
    mapped_starting_airport = airports.get(starting_airport, None)
    mapped_destination_airport = airports.get(destination_airport, None)
    
    # Map cabin_type
    cabins = {
        'Coach': 0,
        'Premium Coach': 1,
        'Business': 2,
        'First': 3,
        'Mix': 4
    }
    # Business: 1, Coach: 2, First: 3, Premium: 4, Mix: 5
    
    cabin_code = cabins.get(cabin_type, None)
    
    # Transform departure time into bins
    bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    bin_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    
    hours_since_midnight = departure_time.hour + (departure_time.minute / 60)
    
    time_bin = pd.cut([hours_since_midnight], bins=bins, labels=bin_labels, right=False).astype(int)[0]
    
    # Transform departure date into day of the week
    day_of_week = departure_date.weekday()
    # day_of_week = Monday = 1, Tuesday = 2, ..
    
    # Extract Duration and Distance from table
    duration = table[(table['startingAirport'] == mapped_starting_airport) &
                    (table['destinationAirport'] == mapped_destination_airport)]['travelDuration'].values[0]
    distance = table[(table['startingAirport'] == mapped_starting_airport) &
                    (table['destinationAirport'] == mapped_destination_airport)]['totalTravelDistance'].values[0]    
    
    user_input = pd.DataFrame({
        'day_of_week': [day_of_week],
        'departureTime_convert_bins': [time_bin],
        'CabinCode': [cabin_code],
        'startingAirport': [mapped_starting_airport],
        'destinationAirport': [mapped_destination_airport],
        'travelDuration': [duration],
        'totalTravelDistance': [distance]
    }, index=[0])
    
    return user_input

    # flgiht Date UnixTime
    # departure_month

invalid_airport_pairs = {
    ('EWR', 'JFK'),
    ('JFK', 'EWR'),
    ('JFK', 'LGA'),
    ('LGA', 'JFK'),
    ('LGA', 'EWR')
}

def is_valid_route(starting_airport, destination_airport, invalid_pairs):
    return (starting_airport, destination_airport) not in invalid_pairs

def main():
    st.title("🇺🇸USA Flight Fare Predictor")
    
    with st.expander("Brought to you by Group 9"):
            st.text("Team Members (Student IDs):")
            st.markdown("""
        - Marisara Satrulee (24710081)
        - Narongvat Chingpayakmon (14229898)
        - Srusti Pattnayak (14348421)
        - Sudarat Sukjaroen (24667255)
        """)
            
    st.markdown("""
        **Welcome to the USA Flight Fare Predictor! ✈️**
        
        Planning your travel within the United States? Use this app to estimate your airfare costs. 
        Simply input your trip details, and we'll provide you with a fare estimate to help you budget your journey.

        Get started by entering your trip information below.
        
    """)
    
    airport_names = {
    'ATL': 'Atlanta Hartsfield-Jackson, GA (ATL)',
    'BOS': 'Boston Logan International, MA (BOS)',
    'CLT': 'Charlotte Douglas, NC (CLT)',
    'DEN': 'Denver International, CO (DEN)',
    'DFW': 'Dallas Fort Worth International, TX (DFW)',
    'DTW': 'Detroit Wayne County, MI (DTW)',
    'EWR': 'New York Newark, NJ (EWR)',
    'IAD': 'Washington Dulles, VA (IAD)',
    'JFK': 'New York John F. Kennedy, NY (JFK)',
    'LAX': 'Los Angeles International, CA (LAX)',
    'LGA': 'New York LaGuardia, NY (LGA)',
    'MIA': 'Miami International, FL (MIA)',
    'OAK': 'Oakland Metropolitan Oak, CA (OAK)',
    'ORD': "Chicago O'Hare International, IL (ORD)",
    'PHL': 'Philadelphia International, PA (PHL)',
    'SFO': 'San Francisco International, CA (SFO)'
}
    
    st.markdown("<br>", unsafe_allow_html=True)

    starting_airport = st.selectbox(
        "**Origin Airport:**",
        options=list(airport_names.keys()),
        format_func=lambda x: airport_names[x],
        index=0
)

    destination_airport = st.selectbox(
        "**Destination Airport:**",
        options=list(airport_names.keys()),
        format_func=lambda x: airport_names[x],
        index=1
)
    
    departure_date = st.date_input("**Departure Date:**")
    departure_time = st.time_input("**Departure Time:**")
    cabin_type = st.selectbox("**Cabin Type:**", ['Coach', 'Premium Coach', 'Business', 'First', 'Mix'])

    predict_button = st.button("**Predict**")

    if predict_button:
        if starting_airport == destination_airport:
            st.error("❌Origin and Destination airports cannot be the same. Please select different routes.")
        
        elif not is_valid_route(starting_airport, destination_airport, invalid_airport_pairs):
            st.error(f"❌ There is no flight from {starting_airport} to {destination_airport} airport. Please select different routes.")
            
        else:
            processed_input = preprocess_input(
                starting_airport,
                destination_airport,
                departure_date,
                departure_time,
                cabin_type,
            )
            
            prediction = model.predict(processed_input)
            
            predicted_value = prediction[0][0] if prediction.ndim > 1 else prediction[0]
            
            formatted_date = departure_date.strftime("%A, %B %d, %Y") if isinstance(departure_date, datetime.date) else str(departure_date)
            formatted_time = departure_time.strftime("%I:%M %p") if isinstance(departure_time, datetime.time) else str(departure_time) 
            
            st.success(
                f"🎉 Your estimated fligt fare for a {cabin_type} class seat from {starting_airport} to {destination_airport} "
                f"on {formatted_date} at {formatted_time} is: **${predicted_value:,.2f}**!"
            )

if __name__ == '__main__':
    main()