def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    institute_type = int(request.form['institute_type'])
    if(institute_type==1):
        institute_type="IIT"
    elif(institute_type==0):
        institute_type="NIT"
    opening_rank = int(request.form['opening_rank'])
    closing_rank = int(request.form['closing_rank'])

    data = read_csv('data_set.csv')

    avg_rank = (opening_rank + closing_rank) / 2

    filtered_colleges = []
    for college in data:
        if college['institute_type'] == institute_type:
            avg_college_rank = (int(college['opening_rank']) + int(college['closing_rank'])) / 2
            if opening_rank <= avg_college_rank <= closing_rank:
                filtered_colleges.append(college)

    return render_template('results.html', colleges=filtered_colleges)

if __name__ == '__main__':
    app.run(debug=True)
