from flask import Flask, render_template, request

app = Flask(__name__)

# Route for the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Collect submitted data
    data = request.form.get('user_input')
    # Append data to the text file
    with open("data.txt", "a") as file:
        file.write(data + "\n")
    return "Data submitted successfully! <a href='/view'>View Data</a>"

# Route to display the submitted data
@app.route('/view')
def view():
    try:
        # Read all lines from the text file
        with open("data.txt", "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        data = []  # Handle the case where the file doesn't exist
    return render_template('view.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
