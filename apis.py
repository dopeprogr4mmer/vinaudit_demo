from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, reqparse
from utils import ValueEstimator
import sys
import traceback

class EstimateValueResource(Resource):
    def post( self ):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('vehicle', type=str, required=True)
            parser.add_argument('mileage', type=str, required=False, default='0')
            args = parser.parse_args(strict=True)
            print(args)
            vehicle = args['vehicle']
            mileage = args['mileage']
            mileage = 0 if mileage=="" else int(mileage)
            # mileage = int(args['mileage'])
            estimated_data = ValueEstimator().return_estimate(vehicle, mileage)

            resp = {"estimated_value": estimated_data["estimated_value"], "listings": estimated_data["listings"]}

            if not len(estimated_data['listings']):
                resp["message"] = "No Data Found"
                resp["status"] = False
            else:
                resp["message"] = "Estimated Data retuned" 
                resp["status"] = True

            return resp, 200

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            traceback.print_exc()
            return {"status": False, 'message': error_message}, 400