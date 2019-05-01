from flask import Flask
from flask import request
from flask import jsonify

from data import mpg
from data import model

app = Flask(__name__)

@app.route("/", methods=['POST'])
def predict():
    #data = request.get_data()
    data = request.get_json()
    df = mpg.read_cars_from_json(data)
    prediction = model.predict(df)
    data["predicted_mpg"] = prediction[0]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')