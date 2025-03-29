from flask import Flask, render_template, request
import numpy as np
from feature import FeatureExtraction  # Import your feature extraction class
import pickle  # Load your trained model

app = Flask(__name__, static_folder='static')

# Load your trained model (ensure the path is correct)
file=open("pickle/model.pkl","rb")
bagging_model=pickle.load(file)
file.close()

@app.route('/')
def home():
    return render_template('Home_Before.html')  # First page
@app.route('/home_after')
def home_after():
    return render_template('Home_After.html')

@app.route('/header')
def header():
    return render_template('header.html') 

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('ContactUs.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        url = request.form.get('url')  # Get the URL from form input
        obj = FeatureExtraction(url)
        x = np.array(obj.get_features_list()).reshape(1, -1)
        
    
        y_pred =bagging_model.predict(x)[0]
        y_pro_phishing = bagging_model.predict_proba(x)[0,0]
        y_pro_non_phishing = bagging_model.predict_proba(x)[0,1]
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('Home_After.html',xx =round(y_pro_non_phishing,2),url=url )
    return render_template("Home_After.html", xx =-1)


if __name__ == '__main__':
    app.run(debug=True)
