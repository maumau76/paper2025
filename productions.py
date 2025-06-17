from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from src.models.database import db, Production, Product, Material, StockMovement

productions_bp = Blueprint('productions', __name__)

@productions_bp.route('', methods=['GET'])
@jwt_required()
def get_productions():
    try:
        productions = Production.query.order_by(Production.created_at.desc()).all()
        return jsonify([production.to_dict() for production in productions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productions_bp.route('/<int:production_id>', methods=['GET'])
@jwt_required()
def get_production(production_id):
    try:
        production = Production.query.get(production_id)
        if not production:
            return jsonify({'error': 'Produção não encontrada'}), 404
        
        return jsonify(production.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productions_bp.route('', methods=['POST'])
@jwt_required()
def create_production():
    try:
        data = request.get_json()
        
        required_fields = ['product_id', 'quantity_produced', 'production_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        quantity_produced = data['quantity_produced']
        
        # Verificar se há materiais suficientes
        for product_material in product.product_materials:
            needed_quantity = float(product_material.quantity_needed) * quantity_produced
            if product_material.material.stock_quantity < needed_quantity:
                return jsonify({
                    'error': f'Estoque insuficiente do material {product_material.material.name}. '
                            f'Necessário: {needed_quantity}, Disponível: {product_material.material.stock_quantity}'
                }), 400
        
        # Calcular custo total
        total_cost = product.calculate_cost() * quantity_produced
        
        # Criar produção
        production = Production(
            product_id=data['product_id'],
            quantity_produced=quantity_produced,
            total_cost=total_cost,
            production_date=datetime.strptime(data['production_date'], '%Y-%m-%d').date(),
            notes=data.get('notes')
        )
        
        db.session.add(production)
        db.session.flush()  # Para obter o ID da produção
        
        # Deduzir materiais do estoque e registrar movimentações
        for product_material in product.product_materials:
            needed_quantity = float(product_material.quantity_needed) * quantity_produced
            
            # Atualizar estoque do material
            product_material.material.stock_quantity -= needed_quantity
            
            # Registrar movimentação de saída
            movement = StockMovement(
                material_id=product_material.material_id,
                movement_type='OUT',
                quantity=needed_quantity,
                description=f'Produção de {quantity_produced} unidades de {product.name}',
                reference_id=production.id,
                reference_type='production'
            )
            db.session.add(movement)
        
        # Adicionar produtos ao estoque
        product.stock_quantity += quantity_produced
        
        db.session.commit()
        
        return jsonify({
            'message': 'Produção registrada com sucesso',
            'production': production.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@productions_bp.route('/<int:production_id>', methods=['DELETE'])
@jwt_required()
def delete_production(production_id):
    try:
        production = Production.query.get(production_id)
        if not production:
            return jsonify({'error': 'Produção não encontrada'}), 404
        
        # Reverter movimentações de estoque
        movements = StockMovement.query.filter_by(
            reference_id=production_id,
            reference_type='production'
        ).all()
        
        for movement in movements:
            # Reverter a saída de material
            movement.material.stock_quantity += movement.quantity
            db.session.delete(movement)
        
        # Remover produtos do estoque
        production.product.stock_quantity -= production.quantity_produced
        
        db.session.delete(production)
        db.session.commit()
        
        return jsonify({'message': 'Produção deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

