from flask import Flask, render_template, request, jsonify
import json
import socket
import platform
import uuid

app = Flask(__name__)

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_mac_address():
    mac_address = ':'.join(format(x, '02x') for x in uuid.getnode().to_bytes(6, 'big'))
    return mac_address

def get_hostname():
    hostname = socket.gethostname()
    return hostname

def get_os():
    operating_system = platform.platform()
    return operating_system

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    hostname = get_hostname()
    operating_system = get_os()
    
    with open("users.json", "r") as file:
        users = json.load(file)

    for user in users:
        if user["Username"] == username and user["Password"] == password:
            login_info = {
                "First_name": user["First name"],
                "Last_name": user["Last name"],
                "Username": user["Username"],
                "Password": user["Password"],
                "ip_address": ip_address,
                "mac_address": mac_address,
                "hostname": hostname,
                "operating_system": operating_system
            }            
            with open("login_info.json", "a") as login_file:
                json.dump(login_info, login_file)
                login_file.write("\n")
            return jsonify({"success": True})

    return jsonify({"success": False})

if __name__ == '__main__':
    app.run()