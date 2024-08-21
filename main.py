from flask import Flask, jsonify, request
import requests
import time
import json
app = Flask(__name__)


WINDOW_SIZE = 10
TEST_SERVER_URL = "http://20.244.56.144/test/"

window = []

def fetch_numbers(number_id):
    """Fetch numbers from the test server based on the number ID."""
    try:
        start_time = time.time()
        payload = {
"companyName": "affordmedical Pvt Ltd",
"ownerName": "Yash Singh",
"rollNo": "2101320100183",
"ownerEmail": "ys667763@gmail.com",
"clientID":"e51d6fa2-2632-41b3-b601-ea6d6dc0dfa7",
"clientSecret":"PaAuueEVUbVqKlxI"
}
        r=  requests.post("http://20.244.56.144/test/auth",json=payload)
        response_json = r.text

        response_dict = json.loads(response_json)
        access_token = response_dict["access_token"]

        headers = {
    "Authorization": f"Bearer {access_token}"
}

        
        
        response = requests.get(f"http://20.244.56.144/test/primes",headers=headers)
        print(response.text)
        if response.status_code == 200 and (time.time() - start_time) <= 0.5:
            print(response.json().get("numbers", []))
            return response.json().get("numbers", [])
        
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        pass
    return []

def calculate_average(numbers):
    """Calculate the average of the numbers in the window."""
    if numbers:
        return sum(numbers) / len(numbers)
    return 0

@app.route('/numbers/<string:number_id>', methods=['POST'])
def calculate_average_api(number_id):
    global window
    
    fetched_numbers = fetch_numbers(number_id)
    new_numbers = [num for num in fetched_numbers if num not in window]

    if new_numbers:
        window_prev_state = window.copy()
        window.extend(new_numbers)
        if len(window) > WINDOW_SIZE:
            window = window[-WINDOW_SIZE:]
        window_curr_state = window.copy()

        avg = calculate_average(window)
        
        response = {
            "numbers": new_numbers,
            "windowPrevState": window_prev_state,
            "windowCurrState": window_curr_state,
            "avg": round(avg, 2)
        }
    else:
        response = {
            "numbers": [],
            "windowPrevState": window,
            "windowCurrState": window,
            "avg": round(calculate_average(window), 2)
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
