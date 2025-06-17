from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.database import db, Product, ProductMaterial

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        product = Product(
            name=data['name'],
            description=data.get('description'),
            category_id=data.get('category_id'),
            profit_margin=data.get('profit_margin', 0),
            final_price=data.get('final_price'),
            image_url=data.get('image_url'),
            stock_quantity=data.get('stock_quantity', 0)
        )
        
        db.session.add(product)
        db.session.flush()  # Para obter o ID do produto
        
        # Adicionar materiais do produto
        materials = data.get('materials', [])
        for material_data in materials:
            product_material = ProductMaterial(
                product_id=product.id,
                material_id=material_data['material_id'],
                quantity_needed=material_data['quantity_needed']
            )
            db.session.add(product_material)
        
        # Se não foi definido preço final, calcular automaticamente
        if not product.final_price:
            product.final_price = product.calculate_final_price()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Produto criado com sucesso',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        data = request.get_json()
        
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.category_id = data.get('category_id', product.category_id)
        product.profit_margin = data.get('profit_margin', product.profit_margin)
        product.final_price = data.get('final_price', product.final_price)
        product.image_url = data.get('image_url', product.image_url)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        
        # Atualizar materiais se fornecidos
        if 'materials' in data:
            # Remover materiais existentes
            ProductMaterial.query.filter_by(product_id=product_id).delete()
            
            # Adicionar novos materiais
            materials = data['materials']
            for material_data in materials:
                product_material = ProductMaterial(
                    product_id=product.id,
                    material_id=material_data['material_id'],
                    quantity_needed=material_data['quantity_needed']
                )
                db.session.add(product_material)
        
        # Recalcular preço se necessário
        if not product.final_price:
            product.final_price = product.calculate_final_price()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Produto atualizado com sucesso',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Produto deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>/calculate-price', methods=['GET'])
@jwt_required()
def calculate_product_price(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        cost = product.calculate_cost()
        price = product.calculate_final_price()
        
        return jsonify({
            'cost': cost,
            'price': price,
            'profit_margin': float(product.profit_margin)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

