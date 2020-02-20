# This file builds a sentiment analysis model to tell if movie review is.positive or negative.
#
# Sentiment analysis fits a linear classifier on features extracted from the text of the user messages so as to guess
# whether the review is positive or negative.

import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
import time


def doPolarizationAnalysis(review):
    # Put the following in a 'if __name__ == "__main__"' protected block to be able to use a multi-core grid search.
    # if __name__ == "__main__":
    starttime = time.time()
    #  Load movie review dataset.
    movie_reviews_data_folder = 'txt_sentoken'
    dataset = load_files(movie_reviews_data_folder, shuffle=False)
    print("n_samples: %d" % len(dataset.data))

    # Split dataset into training and test set:
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.25, random_state=None)

    # Build a vectorizer / classifier pipeline that filters out tokens that are too rare or too frequent.
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
        ('clf', LinearSVC(C=20)),
    ])

    # Build a grid search to find out whether unigrams or bigrams are more useful.
    # Fit the pipeline on the training set using grid search for the parameters
    parameters = {'vect__ngram_range': [(1, 1), (1, 2)], }
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, cv=5)
    grid_search.fit(docs_train, y_train)

    # Save data in model.file.
    joblib.dump(grid_search.best_estimator_, 'model.file', compress=1)

    # Load model.file.
    CURRENT_DIR = os.path.dirname(__file__)
    model_file = os.path.join(CURRENT_DIR, 'model.file')
    model = joblib.load(model_file)

    # Create view here.
    review = [review]
    result = model.predict(review)
    endtime = time.time()
    print(endtime - starttime, " seconds.")
    if result[0] == 1:
        return 'Your movie review is positive.'
    else:
        return 'Your movie review is negative.'
