import sqlite3
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

class DBConnection:

	def get_connection(self):
		connection = sqlite3.connect('database/vinaudit.db')
		return connection

	def fetch_data(self, query, params):
		with self.get_connection() as conn:
			df = pd.read_sql(query, conn, params=(params,))
			return df

class ValueEstimator:

	def calculate_estimate_with_mileage(self, df, mileage):
		if not len(df):
			return None

		X = df['Mileage'].values.reshape(-1, 1)  # Reshape to a 2D array as required by scikit-learn
		Y = df['Price'].values  # Negate the Y values for negative linear regression
		model = LinearRegression()

		# Fit the model to the data
		model.fit(X, Y)
			
		# Get the slope and intercept from the model
		intercept = model.intercept_
		slope = model.coef_[0]

		# Calculating estimated value 
		estimated_value = slope * mileage + intercept

		# Rounding off to 2 decimal places
		estimated_value = estimated_value.round(2)

		return estimated_value


	def calculate_estimate_without_mileage(self, df):
		if not len(df):
			return None

		# Calculating estimated value as mean of all prices in dataframe if mileage is not provided
		estimated_value = df["Price"].mean()

		# Rounding off to 2 decimal places
		estimated_value = estimated_value.round(2)

		return estimated_value 

	def process_dataframe(self, df):
		# Processing dataframe 
		df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
		df['Price'] = df['Price'].replace(np.nan, 0)
		df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
		df['Mileage'] = df['Mileage'].replace(np.nan, 0)

		return df


	def return_estimate(self, vehicle, mileage):
		vehicle = " ".join(vehicle.split())
		query = """ SELECT vehicle as Vehicle, listing_price as Price, listing_mileage as Mileage, 
					location as Location from VINAUDIT where vehicle like ?;"""
		df = DBConnection().fetch_data(query, vehicle)

		context_data = self.process_dataframe(df)
		if not len(context_data):
			return {"estimated_value": None, "listings": []}

		if mileage:
			# Filtering dataframe to only non-zero mileage and non-zero price
			context_data = context_data.loc[(context_data["Mileage"]!=0) & (context_data["Price"]!=0)]
			estimated_value = self.calculate_estimate_with_mileage(context_data, mileage)
		else:
			# Filtering dataframe to only non non-zero price
			context_data = context_data.loc[context_data["Price"]!=0]
			estimated_value = self.calculate_estimate_without_mileage(context_data)

		# Formatting data to be returned
		columns = context_data.columns.tolist()
		top_100 = context_data.head(100).values.tolist()
		listings = [columns] + top_100

		return {"estimated_value": estimated_value, "listings": listings}