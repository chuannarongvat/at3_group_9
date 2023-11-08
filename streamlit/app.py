import streamlit as st
from joblib import load
import pandas as pd

model = load('models/lr_model.joblib')
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

def main():
    st.title("USA Flight Fare Predictor")
    st.markdown("""
        Welcome to the USA Flight Fare Predictor! ✈️
        
        Planning your travel within the United States? Use this app to estimate your airfare costs. 
        Simply input your trip details, and we'll provide you with a fare estimate to help you budget your journey.

        Get started by entering your trip information below.
    """)
    
    airport_options = ['ATL', 'BOS', 'CLT', 'DEN', 'DFW', 'DTW', 'EWR', 'IAD', 'JFK', 'LAX', 'LGA', 'MIA', 'OAK', 'ORD', 'PHL', 'SFO']

    starting_airport = st.selectbox("Origin Airport:", airport_options, index=0)
    destination_airport = st.selectbox("Destination Airport:", airport_options, index=1)

    departure_date = st.date_input("Departure Date:")
    departure_time = st.time_input("Departure Time:")
    cabin_type = st.selectbox("Cabin Type:", ['Coach', 'Premium Coach', 'Business', 'First', 'Mix'])

    predict_button = st.button("Predict")

    if predict_button:
        if starting_airport == destination_airport:
            st.error("Origin and Destination airports cannot be the same. Please select different airports.")
            
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
            st.success(
                f"🎉 Your estimated fligt fare for a {cabin_type} class seat from {starting_airport} to {destination_airport} "
                f"on {departure_date} at {departure_time} is approximately: ${predicted_value:,.2f}!"
            )

if __name__ == '__main__':
    main()