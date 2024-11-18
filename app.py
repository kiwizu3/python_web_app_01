from flask import Flask, render_template, request

app = Flask(__name__)

# Route for the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    location = request.form.get('location')

    # Save the data to a text file
    with open("citizen_data.txt", "a") as file:
        file.write(f"{full_name},{email},{phone},{location}\n")

    return "Data submitted successfully! <a href='/view'>View Data</a>"

# Route to display the submitted data
@app.route('/view')
def view():
    try:
        # Read the text file and split each line into fields
        with open("citizen_data.txt", "r") as file:
            lines = file.readlines()
        data = [
            {
                "id": index + 1,
                "name": line.split(",")[0].strip(),
                "email": line.split(",")[1].strip(),
                "phone": line.split(",")[2].strip(),
                "location": line.split(",")[3].strip(),
            }
            for index, line in enumerate(lines)
        ]
    except FileNotFoundError:
        data = []  # Handle case where file doesn't exist

    return render_template('view.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
