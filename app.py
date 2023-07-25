from flask import Flask, render_template, request
from flask_restful import Api
from flask_cors import CORS
from apis import EstimateValueResource

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('frontend.html')

api = Api(app)

""" API Routes """
api.add_resource(EstimateValueResource, '/api/estimate_value')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=False)