from main import predict
from flask import Flask, Response,jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route('/')
def getData():
    result = predict()
    return Response(result)

if __name__ == '__main__':
    app.run(debug=True)