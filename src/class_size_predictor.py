import statsmodels.api as sm 
import pandas as pd 
from patsy import dmatrices
import json


# Fill gaps between terms in the DataFrame
def fillGaps(df):

    # If there is only one unique term, then add 11 months after each semester
    if df['term'].nunique() == 1:
        for i in range(df.shape[0]):
            # Get the current semester
            current_semester = df['semester'].iloc[i]
            # Add 11 months after the current semester
            semesters_to_fill = pd.date_range(start=current_semester, periods=12, freq='1M')[1:]
            
            # Get size and term of current_semester
            size = df['size'].iloc[i]
            term = df['term'].iloc[i]

            # Create a DataFrame with the filled semesters (year, term, size, semester)
            filled_df = pd.DataFrame({'year': semesters_to_fill.strftime('%Y'),
                                        'term': term,
                                        'semester': semesters_to_fill.strftime('%Y-%m'), 
                                        'size': size})
            
            # Append the filled DataFrame to the original DataFrame if not empty
            if filled_df.shape[0] > 0:
                df = pd.concat([df, filled_df], ignore_index=True)
        
        return df

    # Add data points between each term (e.g. between 2019-09 and 2020-01, add 2019-10, 2019-11, 2019-12)
    for i in range(df.shape[0] - 1):
        # Get the current semester and the next semester
        current_semester = df['semester'].iloc[i]
        next_semester = df['semester'].iloc[i + 1]
        
        year_1 = int(current_semester.split('-')[0])
        year_2 = int(next_semester.split('-')[0])
        month_1 = int(current_semester.split('-')[1])
        month_2 = int(next_semester.split('-')[1])
        # Get the difference in months between the current semester and the next semester
        difference = (year_2 - year_1) * 12 + (month_2 - month_1)
        
        # If the difference is not 4 months, then add the missing months
        if difference > 4:
            continue

        # Add data points between the current semester and the next semester
        semesters_to_fill = pd.date_range(start=current_semester, end=next_semester, freq='1M')[1:]
        
        # Get size and term of current_semester
        size = df['size'].iloc[i]
        term = df['term'].iloc[i]

        # Create a DataFrame with the filled semesters (year, term, size, semester)
        filled_df = pd.DataFrame({'year': semesters_to_fill.strftime('%Y'),
                                    'term': term,
                                    'semester': semesters_to_fill.strftime('%Y-%m'), 
                                    'size': size})
        
        # Append the filled DataFrame to the original DataFrame if not empty
        if filled_df.shape[0] > 0:
            df = pd.concat([df, filled_df], ignore_index=True)

    # Sort the DataFrame by 'semester' column
    df.sort_values('semester', inplace=True)

    # Reset the index to normalize the order
    df.reset_index(drop=True, inplace=True)
    return df


def classSizePredictor(data, semesters_to_predict, order, seasonal_order):

    # Extract past enrollment data
    pastEnrollmentData = data["pastEnrollment"]

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(pastEnrollmentData)

    # Prepare data for time series model
    df['term'] = df['term'].astype(int)
    df['semester'] = pd.to_datetime(df['year'].astype(str) + '-' + df['term'].astype(str), format='%Y-%m').dt.strftime('%Y-%m')

    # Sort the DataFrame by 'semester' column and reset the index
    df.sort_values('semester', inplace=True)

    # Create list of unique terms
    unique_terms = df['term'].unique()

    # Add a semseter on the end of semesters_to_predict to predict the next term
    semesters_to_predict.append((pd.to_datetime(semesters_to_predict[-1], format='%Y-%m') + pd.DateOffset(months=4)).strftime('%Y-%m'))

    # Create a DataFrame to hold the final predictions
    predictions_df = pd.DataFrame({'semester': semesters_to_predict[:-1], 'size': None})
    predictions_df['term'] = pd.to_datetime(predictions_df['semester']).dt.month.astype(int)

    # Sort the DataFrame by 'semester' column
    df.sort_values('semester', inplace=True)

    # Deal with small dataset
    unique_terms = df['term'].unique()
    # Split up dataframe into multiple dataframes based on unique terms
    df_list = [df[df['term'] == term] for term in unique_terms]

    for term in df_list:
        if term.shape[0] < 4:
            # Get the last size in the term
            recent_size = term['size'].iloc[-1]
            new_size = recent_size * 1.0425 # Rate of enrollment growth
            
            # Set new size to the same term in predictions_df
            predictions_df.loc[predictions_df['term'] == term['term'].iloc[0], 'size'] = new_size
        
    # If there are no null values in predictions_df, then return the DataFrame
    if predictions_df['size'].isnull().sum() == 0:
        predictions_df = predictions_df[predictions_df['semester'].isin(semesters_to_predict)]
        return predictions_df

    # Fill gaps between terms in the DataFrame
    df = fillGaps(df)

    # Create monthly trend indicators as exogenous variables
    df['month'] = pd.to_datetime(df['semester']).dt.month
    exog = pd.get_dummies(df['month'], prefix='month')

    # Create a SARIMAX time series model with exogenous variables
    trend = 'n'
    endog = df['size']
    res = sm.tsa.statespace.SARIMAX(endog=endog, exog=exog, order=order, seasonal_order=seasonal_order, trend=trend)
    res = res.fit(disp=False, maxiter=1000)

    # Copy predictions_df to next_terms_df
    next_terms_df = predictions_df.copy()

    # Set term column to month of semester
    # next_terms_df['term'] = next_terms_df['semester'].dt.month
    next_terms_df = fillGaps(next_terms_df)

    # Get the start and end dates indexes in df for prediction
    start_index =  next_terms_df[next_terms_df['semester'] == semesters_to_predict[0]].index[0]
    end_index = next_terms_df[next_terms_df['semester'] == semesters_to_predict[-2]].index[0]

    # Predict the class size for the terms in next_terms_df
    predicted_values = res.predict(start=start_index, end=end_index, exog=exog[start_index:end_index+1])
    
    # Add the predicted values to the DataFrame
    next_terms_df.loc[start_index:end_index, 'size'] = predicted_values

    # Set the size for the given semesters_to_predict using the average of the predicted values on that semester (e.g. 2020-01, 2020-02, 2020-03, 2020-04)
    for semester in semesters_to_predict[:-1]:
        # Get the index of the given semester
        pred_index = predictions_df[predictions_df['semester'] == semester].index[0]
    
        if predictions_df.loc[pred_index, 'size'] is not None:
            continue

        # Get the predicted values for the given semester
        predicted_values = next_terms_df.loc[next_terms_df['semester'] == semester, 'size']
        # Get the average of the predicted values
        average = predicted_values.mean()

        # Save the average to the DataFrame
        predictions_df.loc[predictions_df['semester'] == semester, 'size'] = int(average)
    
    # Remove any rows not in the predicted semesters
    predictions_df = predictions_df[predictions_df['semester'].isin(semesters_to_predict[:-1])]

    # Return the predicted sizes for the given semesters_to_predict 
    return predictions_df

# Convert predictions_df to JSON
# JSON data should be in the following format: list of JSON objects like the following:
# [{ course: string, size: int, term: int}]
def convertToJSON(predictions_df, course):
    # Create a list of JSON objects
    predictions_json = []
    predictions_df = predictions_df.reset_index(drop=True)
    for i in range(predictions_df.shape[0]):
        # Create a JSON object for the current row
        prediction_json = {'course': course, 'size': int(predictions_df.loc[i, 'size']), 'term': int(predictions_df.loc[i, 'term'])}
        # Append the JSON object to the list
        predictions_json.append(prediction_json)

    return predictions_json

def custom_sort_key(element):
    order = {5: 0, 9: 1, 1: 2}  # Define the desired order
    return order.get(element, float('inf'))

def semestersToPredict(course):
    semesters_to_predict = []

    # Get the terms for a given course from the course JSON data
    terms = course['Term']

    # Sort terms to be in [5, 9, 1]
    terms.sort(key=custom_sort_key)

    # Convert terms from 1 to 01, 2 to 02, etc.
    terms = [f'0{term}' if term < 10 else f'{term}' for term in terms]
    
    # Get the year for the given course from the JSON data
    year = int(course['Year'])

    # Create the semesters_to_predict list using terms and year
    for term in terms:
        if term == '01':
            semesters_to_predict.append(f'{year + 1}-{term}')
        else:
            semesters_to_predict.append(f'{year}-{term}')

    return semesters_to_predict

def returnClassSize(data_from_post):
    predictions_json = []

    for course in data_from_post:
        semesters_to_predict = semestersToPredict(course)
        predictions = classSizePredictor(course, semesters_to_predict, order = (0, 0, 0), seasonal_order=(0, 0, 0, 3))
        predictions_json += convertToJSON(predictions, course['course'])
    return predictions_json

