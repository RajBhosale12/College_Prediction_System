from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import csv

app = Flask(__name__, static_url_path='/static')

# Load the model
with open('model1.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

@app.route('/')
def index():
    slideshow_images = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jfif','7.jfif','8.jpeg','9.jpg','10.jpg','11.png','12.png']  # List of image filenames
    return render_template('index.html', slideshow_images=slideshow_images)

@app.route('/search', methods=['POST'])
def search():
    institute_type = int(request.form['institute_type'])
    if institute_type == 1:
        institute_type = "IIT"
    elif institute_type == 0:
        institute_type = "NIT"
    opening_rank = int(request.form['opening_rank'])
    
    # Set closing rank to opening rank + 100
    closing_rank = opening_rank + 100

    data = read_csv('data_with_links_updated.csv')

    avg_rank = (opening_rank + closing_rank) / 2

    filtered_colleges = []
    for college in data:
        if college['institute_type'] == institute_type:
            avg_college_rank = (int(college['opening_rank']) + int(college['closing_rank'])) / 2
            if opening_rank <= avg_college_rank <= closing_rank:
                college['city_name'] = college['institute_short'].split('-')[1]  # Extract city name
                filtered_colleges.append(college)

    return render_template('results.html', colleges=filtered_colleges)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input values from the form
    category = int(request.form['category'])
    quota = int(request.form['quota'])
    pool = int(request.form['pool'])
    institute_type = int(request.form['institute_type'])
    round_no = int(request.form['round_no'])
    opening_rank = int(request.form['opening_rank'])
    
    # Set closing rank to opening rank + 100
    closing_rank = opening_rank + 100
    
    # Create a DataFrame from the input values
    input_data = pd.DataFrame({
        'category': [category],
        'quota': [quota],
        'pool': [pool],
        'institute_type': [institute_type],
        'round_no': [round_no],
        'opening_rank': [opening_rank],
        'closing_rank': [closing_rank]
    })
    
    # Make a prediction
    prediction = model.predict(input_data)
    
    # Get the predicted college
    predicted_college = prediction[0]
    
    # Return the prediction result along with the HTML
    return render_template('results.html', prediction_result=predicted_college)

if __name__ == '__main__':
    app.run(debug=True)
