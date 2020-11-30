'''
    This will have all I need to return a prediction. 
'''
from surprise import Reader, Dataset, SVD 
from surprise.model_selection.validation import cross_validate

def recommend(userid, df):
    '''A function that will take a userid and predict music based their listen history
    With this database, will only take ids ranging 0-200.
    
    Returns a new column called "Estimate Score" which represents the chance that the
    use will like the music
    
    Score will not be high on average, since users are randomly generated.'''
    
    # First passing through a if statment to make sure 
    # The ID matches the requirements. 
    if userid > 1:
        return "ERROR: User ID too high, must be between 0-1"
    elif userid < 0:
        return "ERROR: User ID too low, must be between 0-1"
    else:
        print("Generating music recommendation...")
    
    # Intantiating my reader and my data
    reader = Reader(rating_scale=(0,50))
    data = Dataset.load_from_df(df[['user', 'track_id', 'rating']],
                           reader)
    # Intatntiating my SVD 
    svd = SVD()
    
    # Running a 5-fold cross-validation 
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5,
                  verbose=True)
    
    # Retraining the model using the entire dataset
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    
    # Model has been trained, time to use for prediction.
    titles = df.copy()

    titles['Estimate_Score'] = titles['track_id'].apply(lambda x: svd.predict(userid, x).est)
    
    # Creating a mask that does not include songs the user already has. 
    mask = titles['user'] != userid
    titles = titles[mask]
    
    # Now returning the top 5 songs for that user.
    titles = titles.sort_values(by=['Estimate_Score'], ascending=False)
    
    titles = titles.head(5)
    
    #titles = [titles.columns.values.tolist()] + titles.values.tolist()
    return titles