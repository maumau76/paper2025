from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.database import db, Material, StockMovement

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('', methods=['GET'])
@jwt_required()
def get_materials():
    try:
        materials = Material.query.all()
        return jsonify([material.to_dict() for material in materials]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@materials_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock_materials():
    try:
        materials = Material.query.filter(Material.stock_quantity <= Material.min_stock_alert).all()
        return jsonify([material.to_dict() for material in materials]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@materials_bp.route('', methods=['POST'])
@jwt_required()
def create_material():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'unit', 'purchase_price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        material = Material(
            name=data['name'],
            unit=data['unit'],
            purchase_price=data['purchase_price'],
            stock_quantity=data.get('stock_quantity', 0),
            min_stock_alert=data.get('min_stock_alert', 0),
            supplier_id=data.get('supplier_id')
        )
        
        db.session.add(material)
        db.session.commit()
        
        return jsonify({
            'message': 'Material criado com sucesso',
            'material': material.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@materials_bp.route('/<int:material_id>', methods=['PUT'])
@jwt_required()
def update_material(material_id):
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error': 'Material não encontrado'}), 404
        
        data = request.get_json()
        
        material.name = data.get('name', material.name)
        material.unit = data.get('unit', material.unit)
        material.purchase_price = data.get('purchase_price', material.purchase_price)
        material.stock_quantity = data.get('stock_quantity', material.stock_quantity)
        material.min_stock_alert = data.get('min_stock_alert', material.min_stock_alert)
        material.supplier_id = data.get('supplier_id', material.supplier_id)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Material atualizado com sucesso',
            'material': material.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@materials_bp.route('/<int:material_id>', methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error': 'Material não encontrado'}), 404
        
        db.session.delete(material)
        db.session.commit()
        
        return jsonify({'message': 'Material deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@materials_bp.route('/<int:material_id>/add-stock', methods=['POST'])
@jwt_required()
def add_stock(material_id):
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error': 'Material não encontrado'}), 404
        
        data = request.get_json()
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')
        description = data.get('description', 'Entrada de estoque')
        
        if not quantity or quantity <= 0:
            return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400
        
        # Atualizar estoque
        material.stock_quantity += quantity
        
        # Registrar movimentação
        movement = StockMovement(
            material_id=material_id,
            movement_type='IN',
            quantity=quantity,
            unit_price=unit_price,
            total_cost=quantity * unit_price if unit_price else None,
            description=description,
            reference_type='purchase'
        )
        
        db.session.add(movement)
        db.session.commit()
        
        return jsonify({
            'message': 'Estoque adicionado com sucesso',
            'material': material.to_dict(),
            'movement': movement.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

