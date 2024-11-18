from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_FILE = "citizen_data.txt"

# Helper function to read citizen data from file
def read_data():
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
        return [
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
        return []

# Helper function to write citizen data to file
def write_data(data):
    with open(DATA_FILE, "w") as file:
        for record in data:
            file.write(f"{record['name']},{record['email']},{record['phone']},{record['location']}\n")

# Route: Get all citizen records
@app.route('/api/citizens', methods=['GET'])
def get_all_citizens():
    data = read_data()
    return jsonify(data)

# Route: Get a specific citizen by ID
@app.route('/api/citizens/<int:citizen_id>', methods=['GET'])
def get_citizen_by_id(citizen_id):
    data = read_data()
    for record in data:
        if record['id'] == citizen_id:
            return jsonify(record)
    return jsonify({"error": "Citizen not found"}), 404

# Route: Add a new citizen
@app.route('/api/citizens', methods=['POST'])
def add_citizen():
    new_citizen = request.json
    data = read_data()

    # Validate input
    if not all(key in new_citizen for key in ("name", "email", "phone", "location")):
        return jsonify({"error": "Invalid data"}), 400

    # Add new citizen
    new_record = {
        "id": len(data) + 1,
        "name": new_citizen['name'],
        "email": new_citizen['email'],
        "phone": new_citizen['phone'],
        "location": new_citizen['location'],
    }
    data.append(new_record)
    write_data(data)

    return jsonify(new_record), 201

# Route: Delete a citizen by ID
@app.route('/api/citizens/<int:citizen_id>', methods=['DELETE'])
def delete_citizen(citizen_id):
    data = read_data()
    updated_data = [record for record in data if record['id'] != citizen_id]

    if len(updated_data) == len(data):  # No record deleted
        return jsonify({"error": "Citizen not found"}), 404

    # Update the IDs after deletion
    for index, record in enumerate(updated_data):
        record['id'] = index + 1

    write_data(updated_data)
    return jsonify({"message": "Citizen deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
