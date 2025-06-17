from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from src.models.database import db, Expense

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('', methods=['GET'])
@jwt_required()
def get_expenses():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        
        query = Expense.query
        
        if category:
            query = query.filter_by(category=category)
        
        expenses = query.order_by(Expense.expense_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'expenses': [expense.to_dict() for expense in expenses.items],
            'total': expenses.total,
            'pages': expenses.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('', methods=['POST'])
@jwt_required()
def create_expense():
    try:
        data = request.get_json()
        
        required_fields = ['description', 'amount', 'expense_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        expense = Expense(
            description=data['description'],
            amount=data['amount'],
            expense_date=datetime.strptime(data['expense_date'], '%Y-%m-%d').date(),
            category=data.get('category')
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'message': 'Despesa registrada com sucesso',
            'expense': expense.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    try:
        expense = Expense.query.get(expense_id)
        if not expense:
            return jsonify({'error': 'Despesa não encontrada'}), 404
        
        data = request.get_json()
        
        expense.description = data.get('description', expense.description)
        expense.amount = data.get('amount', expense.amount)
        if data.get('expense_date'):
            expense.expense_date = datetime.strptime(data['expense_date'], '%Y-%m-%d').date()
        expense.category = data.get('category', expense.category)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Despesa atualizada com sucesso',
            'expense': expense.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    try:
        expense = Expense.query.get(expense_id)
        if not expense:
            return jsonify({'error': 'Despesa não encontrada'}), 404
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'message': 'Despesa deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_expense_categories():
    try:
        categories = db.session.query(Expense.category).distinct().filter(Expense.category.isnot(None)).all()
        return jsonify([category[0] for category in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

