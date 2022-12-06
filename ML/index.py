# -*- coding: utf-8 -*-

#importing libraries
import joblib
import inputScript

#load the pickle file
classifier = joblib.load('rf_final.pkl')

#input url
urls=["https://github.com/","https://www.google.com/","https://stackoverflow.com/","https://eg.iitjammu.ac.in/"]

#checking and predicting
for url in urls:
    checkprediction = inputScript.main(url)
    prediction = classifier.predict(checkprediction)
    print("Prediction is",prediction[0])
