from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def parse_time(time_str):
    """Parses MM:SS or H:MM:SS string into total seconds."""
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:  # H:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0

def format_time(total_seconds):
    """Formats total seconds into H:MM:SS string."""
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """
    Handles pace conversion. 
    Expects JSON input: {'pace': 'MM:SS', 'unit': 'km' or 'mile'}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400
            
        pace_str = data.get('pace')
        unit = data.get('unit', 'km') # Defaults to km if not provided

        if not pace_str:
            return jsonify({"error": "Pace is required"}), 400

        seconds_per_unit = parse_time(pace_str)

        # Distances in kilometers
        distances = {
            "5K": 5.0,
            "10K": 10.0,
            "Half Marathon": 21.0975,
            "Marathon": 42.195
        }

        # If the input pace was per mile, we adjust the math
        # 1 mile = 1.60934 km
        conversion_factor = 1.0 if unit == 'km' else 0.621371

        results = {}
        for name, dist in distances.items():
            # Calculate total seconds: (seconds/unit) * (units/km) * distance_km
            if unit == 'km':
                total_time = seconds_per_unit * dist
            else:
                # Convert pace per mile to pace per km, then multiply
                total_time = (seconds_per_unit / 1.60934) * dist
                
            results[name] = format_time(total_time)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' makes the server accessible externally
    # port=5000 is the default Flask port
    app.run(debug=True, host='0.0.0.0', port=5000)