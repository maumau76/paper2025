from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from src.models.database import db, Sale, SaleItem, Product

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('', methods=['GET'])
@jwt_required()
def get_sales():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        sales = Sale.query.order_by(Sale.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'sales': [sale.to_dict() for sale in sales.items],
            'total': sales.total,
            'pages': sales.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/<int:sale_id>', methods=['GET'])
@jwt_required()
def get_sale(sale_id):
    try:
        sale = Sale.query.get(sale_id)
        if not sale:
            return jsonify({'error': 'Venda não encontrada'}), 404
        
        return jsonify(sale.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('', methods=['POST'])
@jwt_required()
def create_sale():
    try:
        data = request.get_json()
        
        required_fields = ['sale_date', 'payment_method', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        if not data['items']:
            return jsonify({'error': 'Venda deve ter pelo menos um item'}), 400
        
        # Verificar estoque dos produtos
        for item_data in data['items']:
            product = Product.query.get(item_data['product_id'])
            if not product:
                return jsonify({'error': f'Produto {item_data["product_id"]} não encontrado'}), 404
            
            if product.stock_quantity < item_data['quantity']:
                return jsonify({
                    'error': f'Estoque insuficiente do produto {product.name}. '
                            f'Disponível: {product.stock_quantity}, Solicitado: {item_data["quantity"]}'
                }), 400
        
        # Calcular total da venda
        total_amount = 0
        for item_data in data['items']:
            unit_price = item_data.get('unit_price')
            if not unit_price:
                product = Product.query.get(item_data['product_id'])
                unit_price = float(product.final_price) if product.final_price else product.calculate_final_price()
            
            total_amount += unit_price * item_data['quantity']
        
        # Criar venda
        sale = Sale(
            customer_id=data.get('customer_id'),
            sale_date=datetime.strptime(data['sale_date'], '%Y-%m-%d').date(),
            payment_method=data['payment_method'],
            total_amount=total_amount,
            notes=data.get('notes')
        )
        
        db.session.add(sale)
        db.session.flush()  # Para obter o ID da venda
        
        # Criar itens da venda e atualizar estoque
        for item_data in data['items']:
            product = Product.query.get(item_data['product_id'])
            unit_price = item_data.get('unit_price')
            if not unit_price:
                unit_price = float(product.final_price) if product.final_price else product.calculate_final_price()
            
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=unit_price,
                total_price=unit_price * item_data['quantity']
            )
            
            # Atualizar estoque do produto
            product.stock_quantity -= item_data['quantity']
            
            db.session.add(sale_item)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Venda registrada com sucesso',
            'sale': sale.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/<int:sale_id>', methods=['DELETE'])
@jwt_required()
def delete_sale(sale_id):
    try:
        sale = Sale.query.get(sale_id)
        if not sale:
            return jsonify({'error': 'Venda não encontrada'}), 404
        
        # Reverter estoque dos produtos
        for item in sale.sale_items:
            item.product.stock_quantity += item.quantity
        
        db.session.delete(sale)
        db.session.commit()
        
        return jsonify({'message': 'Venda deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_sales_reports():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Sale.query
        
        if start_date:
            query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        sales = query.all()
        
        # Calcular estatísticas
        total_sales = len(sales)
        total_revenue = sum(float(sale.total_amount) for sale in sales)
        
        # Produtos mais vendidos
        product_sales = {}
        for sale in sales:
            for item in sale.sale_items:
                product_name = item.product.name
                if product_name not in product_sales:
                    product_sales[product_name] = {'quantity': 0, 'revenue': 0}
                product_sales[product_name]['quantity'] += item.quantity
                product_sales[product_name]['revenue'] += float(item.total_price)
        
        top_products = sorted(
            product_sales.items(),
            key=lambda x: x[1]['quantity'],
            reverse=True
        )[:10]
        
        return jsonify({
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'top_products': [{'name': name, **data} for name, data in top_products],
            'sales': [sale.to_dict() for sale in sales]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

