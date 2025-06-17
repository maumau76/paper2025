from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.database import db, StockMovement

stock_movements_bp = Blueprint('stock_movements', __name__)

@stock_movements_bp.route('', methods=['GET'])
@jwt_required()
def get_stock_movements():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        material_id = request.args.get('material_id', type=int)
        
        query = StockMovement.query
        
        if material_id:
            query = query.filter_by(material_id=material_id)
        
        movements = query.order_by(StockMovement.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'movements': [movement.to_dict() for movement in movements.items],
            'total': movements.total,
            'pages': movements.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_movements_bp.route('', methods=['POST'])
@jwt_required()
def create_stock_movement():
    try:
        data = request.get_json()
        
        required_fields = ['material_id', 'movement_type', 'quantity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        if data['movement_type'] not in ['IN', 'OUT']:
            return jsonify({'error': 'Tipo de movimentação deve ser IN ou OUT'}), 400
        
        movement = StockMovement(
            material_id=data['material_id'],
            movement_type=data['movement_type'],
            quantity=data['quantity'],
            unit_price=data.get('unit_price'),
            total_cost=data.get('total_cost'),
            description=data.get('description'),
            reference_id=data.get('reference_id'),
            reference_type=data.get('reference_type')
        )
        
        db.session.add(movement)
        db.session.commit()
        
        return jsonify({
            'message': 'Movimentação registrada com sucesso',
            'movement': movement.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

