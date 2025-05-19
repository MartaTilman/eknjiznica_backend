from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
import bcrypt
from flask_cors import CORS

app = Flask(__name__)

# Konfiguracija za MongoDB i tajni ključ
app.config["MONGO_URI"] = "mongodb://localhost:27017/eknjiznica"
app.secret_key = 'tajni_kljuc'

# Omogućavanje CORS-a za frontend (localhost:8080)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

# Inicijalizacija MongoDB
mongo = PyMongo(app)

@app.route('/')
def home():
    return 'Dobrodošli u e-Knjižnicu!'

# Registracija korisnika
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # Provjera postoji li korisnik
    existing_user = mongo.db.users.find_one({'email': email})
    if existing_user:
        return jsonify({"message": "Korisnik s tim emailom već postoji."}), 400

    # Hashiranje lozinke i spremanje korisnika
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Debugging: Provjeri ispravno pohranjenu lozinku
    print(f"Hashirana lozinka: {hashed_password}")

    mongo.db.users.insert_one({
        'username': username,
        'email': email,
        'password': hashed_password
    })

    return jsonify({"message": "Korisnik uspješno registriran."}), 201

# Prijava korisnika
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    print(f"Primljeni podaci: Email={email}, Password={password}")  # Za debugging

    # Provjera postoji li korisnik u bazi
    user = mongo.db.users.find_one({'email': email})
    if user:
        # Provjeri hash lozinke
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            return jsonify({"message": "Uspješno prijavljeni!"}), 200
        else:
            return jsonify({"message": "Pogrešni podaci!"}), 400
    else:
        return jsonify({"message": "Pogrešni podaci!"}), 400

# Odjava korisnika
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Uspješno ste se odjavili!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
