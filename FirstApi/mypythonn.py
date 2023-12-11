from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd
#from datetime import datetime
app = Flask(__name__)
api = Api(app)

class Users(Resource):
	def get(self):
		try:
			data = pd.read_csv('myuser.csv')
			data = data.to_dict('records')
			return {'data' : data} , 200
		except Exception as e:
			return {'message' : 'Error {str(e)}'},500

	def delete(self):
		name = request.args['name']
		data = pd.read_csv('myuser.csv')

		if name in data['name'].values:
			data = data[data['name'] != name]
			data.to_csv('myuser.csv', index = False)
			return {'message' : 'Record succesfully deleted.'}, 200
		else:
			return {'message' : ' Record not found.'}, 404 


	def post(self):
		try:
			data = request.get_json()
			print(data)
			name = data.get('name')
			city = data.get('city')
			birth = data.get('birth')

			req_data = pd.DataFrame({
				'name' : [name],
				'city' : [city],
				'birth': [birth]
			})
			data = pd.read_csv('myuser.csv')
			data = data.append(req_data , ignore_index = True)
			data.to_csv('myuser.csv', index = False)
			return {'message' : 'Record successfully added.'}, 200
		except Exception as e:
			return {'message' : 'Error: {str(e)}'}, 500

class Name(Resource):
	def get(self,name):
		data = pd.read_csv('myuser.csv')
		data = data.to_dict('records')
		for entry in data:
			if entry ['name'] == name:
				return {'data' : entry}, 200
		return {'message' : 'No entry found with this name'} , 404

class Birth(Resource):
	def get(self,name):
		data = pd.read_csv('myuser.csv')
		data = data.to_dict('records')
		current_year = 2023

		for entry in data:
			if entry['name'] == name:
				age = current_year - int(entry['birth'])
				entry['age'] = age
				return {'data' : entry}, 200
		return {'message' : 'No entry found with this name'} , 404

class Cities(Resource):
	def get(self):
		data = pd.read_csv('myuser.csv')
		data = data.to_dict('records')
		return {'data' : data} , 200

api.add_resource(Birth , '/birth/<string:name>')
api.add_resource(Name , '/<string:name>')
api.add_resource(Users , '/users')
api.add_resource(Cities , '/cities')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=6767)
	app.run(debug= True)
