from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Collect data from the form
    name = request.form['name']
    age = request.form['age']

    # Write data to a text file
    with open('submitted_data.csv', 'a') as file:
        file.write(f"Name: {name}, Age: {age}\n")

    # Confirmation message
    message = f"Data saved! Hello, {name}, aged {age}."
    return render_template('response.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
