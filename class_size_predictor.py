import statsmodels.api as sm 
import pandas as pd 
from patsy import dmatrices
import json


# Fill gaps between terms in the DataFrame
def fillGaps(df):
    # Add data points between each term (e.g. between 2019-09 and 2020-01, add 2019-10, 2019-11, 2019-12)
    for i in range(df.shape[0] - 1):
        # Get the current semester and the next semester
        current_semester = df['semester'].iloc[i]
        next_semester = df['semester'].iloc[i + 1]

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
            df = df.append(filled_df, ignore_index=True)

    # Sort the DataFrame by 'semester' column
    df.sort_values('semester', inplace=True)

    # Reset the index to normalize the order
    df.reset_index(drop=True, inplace=True)
    return df


def classSizePredictor(data, semesters_to_predict, order, seasonal_order):

    # Extract past enrollment data
    pastEnrollmentData = data["pastEnrol"]

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(pastEnrollmentData)

    # Prepare data for time series model
    df['term'] = df['term'].astype(int)
    df['semester'] = pd.to_datetime(df['year'].astype(str) + '-' + df['term'].astype(str), format='%Y-%m').dt.strftime('%Y-%m')

    # Sort the DataFrame by 'semester' column
    df.sort_values('semester', inplace=True)

    # Create a DataFrame for the next terms to predict
    next_terms_df = pd.DataFrame({'semester': pd.to_datetime(semesters_to_predict)})
    # Set term column to month of semester
    next_terms_df['term'] = next_terms_df['semester'].dt.month
    next_terms_df['year'] = next_terms_df['semester'].dt.year
    next_terms_df['size'] = 0
    next_terms_df['semester'] = next_terms_df['semester'].dt.strftime('%Y-%m')

    # Concatenate the next_terms_df to the df
    df = pd.concat([df, next_terms_df], ignore_index=True)

    # Fill gaps between terms in the DataFrame
    df = fillGaps(df)

    # Create monthly trend indicators as exogenous variables
    df['month'] = pd.to_datetime(df['semester']).dt.month
    exog = pd.get_dummies(df['month'], prefix='month', drop_first=True)

    # Create a SARIMAX time series model with exogenous variables
    trend = 'n'
    endog = df['size']
    res = sm.tsa.statespace.SARIMAX(endog=endog, exog=exog, order=order, seasonal_order=seasonal_order, trend=trend)
    res = res.fit(disp=False, maxiter=1000)

    # Get the start and end dates indexes in df for prediction
    start_index = df[df['semester'] == semesters_to_predict[0]].index[0]
    end_index = df[df['semester'] == semesters_to_predict[-1]].index[0]

    # Predict the class size for the terms in next_terms_df
    predicted_values = res.predict(start=start_index, end=end_index, exog=exog[start_index:end_index+1])
    
    # Add the predicted values to the DataFrame
    df.loc[start_index:end_index, 'size'] = predicted_values

    # Create a DataFrame to hold the final predictions
    predictions_df = pd.DataFrame({'semester': semesters_to_predict, 'size': 0})
    # Set the size for the given semesters_to_predict using the average of the predicted values on that semester (e.g. 2020-01, 2020-02, 2020-03, 2020-04)
    for semester in semesters_to_predict:
        # Get the index of the given semester
        index = df[df['semester'] == semester].index[0]
        
        if int(df.loc[index, 'size']) == 0:
            average = df.loc[index+1:index+3, 'size'].mean()
        elif index == df.shape[0] - 1:
            average = df.loc[index, 'size']
        else:
            # Get the average of the predicted values on that semester
            average = df.loc[index:index+3, 'size'].mean()

        # Save the average to the DataFrame
        predictions_df.loc[predictions_df['semester'] == semester, 'size'] = int(average)
    
    # Return the predicted sizes for the given semesters_to_predict 
    return predictions_df

# Convert predictions_df to JSON
# JSON data should be in the following format: list of JSON
# [{ course: string, size: int, term: int}]
def convertToJSON(predictions_df, course):
    # Create a list to hold the JSON data
    json_data = []
    # Create a dictionary to hold the JSON data for each semester
    json_dict = {}
    # Create a list to hold the terms
    terms = []
    # Create a list to hold the sizes
    sizes = []

    # Get the terms and sizes from the predictions_df
    for index, row in predictions_df.iterrows():
        terms.append(row['semester'])
        sizes.append(row['size'])
    
    # Add the terms and sizes to the json_dict
    json_dict['terms'] = terms
    json_dict['sizes'] = sizes
    json_dict['course'] = course

    # Add the json_dict to the json_data
    json_data.append(json_dict)

    # Return the JSON data
    return json_data

def returnClassSize():
    semesters_to_predict = ['2023-09', '2024-01', '2024-05']
    with open('test/data/one_class.json') as data:
        # Load the JSON data
        data = json.load(data)
        predictions = classSizePredictor(data, semesters_to_predict, order = (0, 0, 0), seasonal_order=(0, 0, 0, 0))
        predictions_json = convertToJSON(predictions, data['course'])

        return predictions_json

    