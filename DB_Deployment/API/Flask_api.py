from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/room', methods=['GET', 'POST'])
    def rooms(roomId):
        
