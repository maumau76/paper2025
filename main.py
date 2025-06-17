import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from src.models.database import db
from src.routes.auth import auth_bp
from src.routes.suppliers import suppliers_bp
from src.routes.materials import materials_bp
from src.routes.categories import categories_bp
from src.routes.products import products_bp
from src.routes.stock_movements import stock_movements_bp
from src.routes.productions import productions_bp
from src.routes.customers import customers_bp
from src.routes.sales import sales_bp
from src.routes.expenses import expenses_bp
from src.routes.dashboard import dashboard_bp
from src.routes.reports import reports_bp

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'rm-papel-secret-key-2024')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string-rm-papel')

# Configuração do banco de dados
database_url = os.getenv('DATABASE_URL')
if database_url:
    # Para Railway/PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Para desenvolvimento local com SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(suppliers_bp, url_prefix='/api/suppliers')
app.register_blueprint(materials_bp, url_prefix='/api/materials')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(stock_movements_bp, url_prefix='/api/stock-movements')
app.register_blueprint(productions_bp, url_prefix='/api/productions')
app.register_blueprint(customers_bp, url_prefix='/api/customers')
app.register_blueprint(sales_bp, url_prefix='/api/sales')
app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(reports_bp, url_prefix='/api/reports')

# Criar tabelas
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

