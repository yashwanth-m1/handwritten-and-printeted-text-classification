# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import confusion_matrix
# from joblib import dump, load
# import pickle

# import pdb

# clf = load("data.joblib")
# mpred = [[40,113,0.353982300884956,	0.453097345132743,	0.008849557522124]]
# mpred2 = [20,62,0.32258064516129,0.237096774193548,0.015322580645161]

# pred = clf.predict(mpred2)
# print(pred[0])

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.externals import joblib

# Load the trained classifier
clf = joblib.load("data.joblib")

# Define the input data for prediction
mpred = [[40, 113, 0.353982300884956, 0.453097345132743, 0.008849557522124]]
mpred2 = np.array([20, 62, 0.32258064516129, 0.237096774193548, 0.015322580645161]).reshape(1, -1)

# Perform prediction
pred = clf.predict(mpred2)
print(f"The output is:{pred[0]}")
