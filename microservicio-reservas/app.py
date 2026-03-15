import os
import logging
from dotenv import load_dotenv

# Use absolute path for .env to avoid issues
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))


# Configure logging to both console and file
log_formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

# File Handler
file_handler = logging.FileHandler(os.path.abspath(os.path.join(os.path.dirname(__file__), '../reservation.log')))
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

logger = logging.getLogger("reservas-service")

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import db, Reserva
from vistas import VistaReservas, VistaReserva
from cryptography.fernet import Fernet

def create_app():
    app = Flask(__name__)
    # Default to absolute path for DB
    db_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../reservations.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f"sqlite:///{db_abs_path}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'secret-key')
    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    CORS(app)
    db.init_app(app)
    JWTManager(app)
    
    api = Api(app)
    api.add_resource(VistaReservas, '/reservas')
    api.add_resource(VistaReserva, '/reservas/<int:id_reserva>')
    
    return app

app = create_app()

FERNET_KEY = os.getenv("FERNET_KEY", "default-fernet-key").encode()
cipher_suite = Fernet(FERNET_KEY)

def encrypt_field(value: str) -> str:
    return cipher_suite.encrypt(value.encode()).decode()

with app.app_context():
    db.create_all()
    if Reserva.query.count() == 0:
        db.session.add(Reserva(pais="AR", estado="PENDING",    email_cifrado=encrypt_field("user_ar@example.com"),    telefono_cifrado=encrypt_field("111111111")))
        db.session.add(Reserva(pais="AR", estado="CONFIRMED",  email_cifrado=encrypt_field("admin_ar@example.com"),   telefono_cifrado=encrypt_field("222222222")))
        db.session.add(Reserva(pais="CO", estado="PENDING",    email_cifrado=encrypt_field("user_co@example.com"),    telefono_cifrado=encrypt_field("333333333")))
        db.session.add(Reserva(pais="CO", estado="CONFIRMED",  email_cifrado=encrypt_field("admin_co@example.com"),   telefono_cifrado=encrypt_field("444444444")))
        db.session.commit()
    logger.info("RESERVAS_SERVICE_STARTED | port=8002 | data_populated")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8002)), debug=False)
