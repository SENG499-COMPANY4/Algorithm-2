import statsmodels.api as sm 
import pandas as pd 
from patsy import dmatrices
import json

"""
    "pastEnrolment": [{
            "year": int,
            "term": int,
            "size": int
        }],

    "term": int,
"""
def classSizePredictor(data, semesters_to_predict):
    # Load JSON data
    jsonData = json.load(data)
    
    # Extract past enrollment data
    pastEnrollmentData = jsonData["pastEnrollment"]

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(pastEnrollmentData)

    # Prepare data for time series model
    df['term'] = df['term'].astype(int)
    df['semester'] = pd.to_datetime(df['year'].astype(str) + '-' + df['term'].astype(str), format='%Y-%m').dt.strftime('%Y-%m')

    # Sort the DataFrame by 'semester' column
    df.sort_values('semester', inplace=True)

    # Interpolate missing values
    mean_size = df['size'].mean()
    # Add missing semesters between last semester and the first semester to predict
    semesters_to_fill = pd.date_range(start=df['semester'].iloc[-1], end=semesters_to_predict[0], freq='4M')[1:]
    filled_df = pd.DataFrame({'semester': semesters_to_fill.strftime('%Y-%m'), 'size': mean_size})

    # Append the filled DataFrame to the original DataFrame
    df = pd.concat([df, filled_df], ignore_index=True)

    print(df)

    for models in sarima_configs():
        
        # Create a SARIMA time series model
        order, seasonal_order, trend = models
        endog, exog = dmatrices('size ~ semester', df, return_type='dataframe')
        try:
            res = sm.tsa.statespace.SARIMAX(endog, exog, order=order, seasonal_order=seasonal_order, trend=trend)
                
            
            start_params = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
            res = res.fit(start_params=start_params, disp=False, maxiter=1000)


            # Predict the class sizes for the next semesters
            next_terms_df = pd.DataFrame({'semester': pd.to_datetime(semesters_to_predict, format='%Y-%m').strftime('%Y-%m')})

            # Forecast the class sizes
            predicted_values = res.predict(start=next_terms_df.index[0], end=next_terms_df.index[-1])

            # Assign the predicted values to the DataFrame
            next_terms_df['predicted_size'] = predicted_values
            if next_terms_df['predicted_size'].isnull().values.any():
                continue

            # if predicted value is less than 50, continue
            if next_terms_df['predicted_size'].values[0] < 50:
                continue
            print(models)
            print(next_terms_df)
        except:
            continue
    # return next_terms_df


def sarima_configs(seasonal=[3]):
    models = list()
    # define config lists
    p_params = [0, 1, 2]
    d_params = [0, 1]
    q_params = [0, 1, 2]
    t_params = ['n','c','t','ct']
    P_params = [0, 1, 2]
    D_params = [0, 1]
    Q_params = [0, 1, 2]
    m_params = seasonal
    # create config instances
    for p in p_params:
        for d in d_params:
            for q in q_params:
                for t in t_params:
                    for P in P_params:
                        for D in D_params:
                            for Q in Q_params:
                                for m in m_params:
                                    cfg = [(p,d,q), (P,D,Q,m), t]
                                    models.append(cfg)
    return models

# import test_data.json
semesters_to_predict = ['2023-09', '2024-01', '2024-05']
with open('test_data.json') as data:
    classSizePredictor(data, semesters_to_predict)
    