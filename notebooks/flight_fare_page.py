import streamlit as st
import numpy as np
import pandas as pd
from joblib import load
from datetime import datetime



#loading the saved models
loaded_model = load('../../models/model_gb_boost_srusti.joblib')

# creating a function for prediction
def flight_prediction(input_data):
    # turn nested list into a single list
    new_input_data = []
    for element in input_data:
            new_input_data.append(element)

    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(new_input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = loaded_model.predict(input_data_reshaped)
    return 'The estimated flight fare is {:,} rupees.'.format(int(prediction))

# giving a title
st.title('Flight Fare Prediction')
starting_Airport = st.selectbox('Origin Airport:',
                               ['ATL',
                                'BOS',
                                'CLT',
                                'DEN',
                                'DFW',
                                'DTW',
                                'EWR',
                                'IAD',
                                'JFK',
                                'LAX',
                                'LGA',
                                'MIA',
                                'OAK',
                                'ORD',
                                'PHL',
                                'SFO'])
if (starting_Airport == 'ATL'):
    startingAirportNum = 3
elif (starting_Airport == 'BOS'):
    startingAirportNum =4
elif (starting_Airport == 'CLT'):
    startingAirportNum=7
elif (starting_Airport == 'DEN'):
    startingAirportNum=11
elif (starting_Airport == 'DFW'):
    startingAirportNum = 13
elif (starting_Airport == 'DTW'):
    startingAirportNum=15
elif (starting_Airport == 'EWR'):
    startingAirportNum=0
elif (starting_Airport == 'IAD'):
    startingAirportNum=14
elif (starting_Airport == 'JFK'):
    startingAirportNum=1
elif (starting_Airport == 'LAX'):
    startingAirportNum=5
elif (starting_Airport == 'LGA'):
    startingAirportNum=9
elif (starting_Airport == 'MIA'):
    startingAirportNum=12
elif (starting_Airport == 'OAK'):
    startingAirportNum=8
elif (starting_Airport == 'ORD'):
    startingAirportNum=2
elif (starting_Airport == 'PHL'):
    startingAirportNum=10
elif (starting_Airport == 'SFO'):
    startingAirportNum=6
else:
    startingAirport = startingAirport

destination_Airport = st.selectbox('Destination_Airport:',
                                   ['ATL',
                                'BOS',
                                'CLT',
                                'DEN',
                                'DFW',
                                'DTW',
                                'EWR',
                                'IAD',
                                'JFK',
                                'LAX',
                                'LGA',
                                'MIA',
                                'OAK',
                                'ORD',
                                'PHL',
                                'SFO'])

if (destination_Airport == 'ATL'):
    ddestinationAirportNum=0
elif (destination_Airport == 'BOS'):
    destinationAirportNum=1
elif (destination_Airport == 'CLT'):
    destinationAirportNum=2
elif (destination_Airport == 'DEN'):
    destinationAirportNum=3
elif (destination_Airport == 'DFW'):
    destinationAirportNum=4
elif (destination_Airport == 'DTW'):
    destinationAirportNum=5
elif (destination_Airport == 'EWR'):
    destinationAirportNum=14
elif (destination_Airport == 'IAD'):
    destinationAirportNum=6
elif (destination_Airport == 'JFK'):
    destinationAirportNum=15
elif (destination_Airport == 'LAX'):
    destinationAirportNum=7
elif (destination_Airport == 'LGA'):
    destinationAirportNum=13
elif (destination_Airport == 'MIA'):
    destinationAirportNum=8
elif (destination_Airport == 'OAK'):
    destinationAirportNum=9
elif (destination_Airport == 'ORD'):
    destinationAirportNum=10
elif (destination_Airport == 'PHL'):
    destinationAirportNum=11
elif (destination_Airport == 'SFO'):
    destinationAirportNum=12
else:
    destinationAirportNum = destinationAirport

flightDate=st.date_input('Departure_date:')

departure_time = st.time_input("Departure time")

Cabin_type = st.selectbox('Cabin type:', ['coach', 'first', 'premium coach', 'business'])

if (Cabin_type == 'coach'):
    segmentsCabinCodeNum = 0
elif (Cabin_type == 'first'):
    Cabin_type=1
elif (Cabin_type == 'premium coach'):
    segmentsCabinCodeNum='3
elif (Cabin_type == 'business'):
    segmentsCabinCodeNum=2

else:
    segmentsCabinCodeNum = Cabin_type

#st.button('Fare Prediction')

# creating a button for prediction
if st.button('Fare Prediction'):
    Fare = flight_prediction(['startingAirportNum','destinationAirportNum','flightDate','departure_time','segmentsCabinCodeNum'])

#st.success(price)

