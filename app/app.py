from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from flask_restx import fields, Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)

# Flask RESTX configurations
api = Api(app=app,
          version="1.0",
          title="Flask MySQL Docker",
          description="Test Run Flask and MYSQL in Docker")

# CORS configurations
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@api.route('/')
class Index(Resource):
    @cross_origin()
    def get(self):
        return jsonify({'message': 'Hello world!!!'})


@api.route('/initdb')
class Index(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Internal Server Error'})
    @cross_origin()
    def post(self):
        connection = mysql.connector.connect(
            user="root", password="root", host="db", port="3306", database="practice")
        cursor = connection.cursor()
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS practice;")
        cursor.execute("USE practice;")

        # Drop table if it exists
        cursor.execute("DROP TABLE IF EXISTS user;")

        # Create user table
        cursor.execute("CREATE TABLE user (id INT UNSIGNED NOT NULL AUTO_INCREMENT, name VARCHAR(50) NOT NULL, email varchar(100) NOT NULL, phone INT UNSIGNED NOT NULL, address varchar(250) NOT NULL, PRIMARY KEY (id));")

        # Insert data into the user table
        cursor.execute("INSERT INTO user (id, name, email, phone, address) VALUES (1, 'Bruce Wayne', 'brucewayne@gmail.com', 218928398, 'Earth'), (2, 'Barry Allen', 'barryallen@gmail.com', 423234324, 'Earth');")

        # Commit the changes
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()
        return 'DB initialized'


users_namespace = api.namespace(
    'users', description='To get users data'
)


@users_namespace.route('')
class Users(Resource):
    @users_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Internal Server Error'})
    @cross_origin()
    def get(self):
        connection = mysql.connector.connect(
            user="root", password="root", host="db", port="3306", database="practice")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user")
        data = cursor.fetchall()
        results = [{'id': id,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'address': address} for (id, name, email, phone, address) in data]
        cursor.close()
        connection.close()
        return jsonify({'users': results})


@users_namespace.route('/<int:id>')
class GetUser(Resource):
    @users_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Internal Server Error'}, params={'id': {'description': 'The ID of the person', 'type': 'int', 'required': False}})
    @cross_origin()
    def get(self, id):
        #parser = reqparse.RequestParser()
        #parser.add_argument('id',  required=False, default=None)
        #args = parser.parse_args()

        #person_id = args['id'] or None
        person_id = id

        connection = mysql.connector.connect(
            user="root", password="root", host="db", port="3306", database="practice")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE id = {};".format(person_id))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(data)


@users_namespace.route('/add-user')
class AddUser(Resource):
    @users_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Internal Server Error'}, params={'name': {'description': 'The name of the person', 'type': 'String', 'required': False}, 'email': {'description': 'The email of the person', 'type': 'String', 'required': False},
                                                                                                               'phone': {'description': 'The phone number of the person', 'type': 'int', 'required': False}, 'address': {'description': 'The address of the person', 'type': 'String', 'required': False}})
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False, default=None)
        parser.add_argument('email', required=False, default=None)
        parser.add_argument('phone', type=int, required=False, default=None)
        parser.add_argument('address', required=False, default=None)
        args = parser.parse_args()

        person_name = args['name'] or None
        person_email = args['email'] or None
        person_phone = args['phone'] or None
        person_address = args['address'] or None

        connection = mysql.connector.connect(
            user="root", password="root", host="db", port="3306", database="practice")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (name, email, phone, address) VALUES ('{}', '{}', {}, '{}');".format(
            person_name, person_email, str(person_phone), person_address))
        connection.commit()
        cursor.close()
        connection.close()
        return 'User added'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
