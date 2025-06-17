from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from src.models.database import db, Sale, Product, Material, Expense, SaleItem

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_dashboard_summary():
    try:
        # Data atual
        today = datetime.now().date()
        current_month_start = today.replace(day=1)
        last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        
        # Vendas do mês atual
        current_month_sales = Sale.query.filter(
            Sale.sale_date >= current_month_start
        ).all()
        
        current_month_revenue = sum(float(sale.total_amount) for sale in current_month_sales)
        current_month_sales_count = len(current_month_sales)
        
        # Vendas do mês passado
        last_month_sales = Sale.query.filter(
            Sale.sale_date >= last_month_start,
            Sale.sale_date < current_month_start
        ).all()
        
        last_month_revenue = sum(float(sale.total_amount) for sale in last_month_sales)
        
        # Calcular crescimento
        revenue_growth = 0
        if last_month_revenue > 0:
            revenue_growth = ((current_month_revenue - last_month_revenue) / last_month_revenue) * 100
        
        # Materiais com estoque baixo
        low_stock_materials = Material.query.filter(
            Material.stock_quantity <= Material.min_stock_alert
        ).all()
        
        # Produtos mais vendidos (últimos 30 dias)
        thirty_days_ago = today - timedelta(days=30)
        top_products_query = db.session.query(
            Product.name,
            func.sum(SaleItem.quantity).label('total_sold')
        ).join(SaleItem).join(Sale).filter(
            Sale.sale_date >= thirty_days_ago
        ).group_by(Product.id, Product.name).order_by(
            func.sum(SaleItem.quantity).desc()
        ).limit(5).all()
        
        top_products = [{'name': name, 'quantity': int(quantity)} for name, quantity in top_products_query]
        
        # Despesas do mês atual
        current_month_expenses = Expense.query.filter(
            Expense.expense_date >= current_month_start
        ).all()
        
        current_month_expenses_total = sum(float(expense.amount) for expense in current_month_expenses)
        
        # Saldo atual (receitas - despesas do mês)
        current_balance = current_month_revenue - current_month_expenses_total
        
        # Produções recentes (últimos 7 dias)
        seven_days_ago = today - timedelta(days=7)
        recent_productions = db.session.query(
            func.count().label('count')
        ).select_from(db.session.query().select_from(db.text('productions')).filter(
            db.text('production_date >= :date')
        ).params(date=seven_days_ago)).scalar() or 0
        
        return jsonify({
            'current_month_revenue': current_month_revenue,
            'current_month_sales_count': current_month_sales_count,
            'revenue_growth': round(revenue_growth, 2),
            'current_balance': current_balance,
            'low_stock_materials_count': len(low_stock_materials),
            'low_stock_materials': [material.to_dict() for material in low_stock_materials[:5]],
            'top_products': top_products,
            'current_month_expenses': current_month_expenses_total,
            'recent_productions': recent_productions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/sales-chart', methods=['GET'])
@jwt_required()
def get_sales_chart():
    try:
        # Últimos 12 meses
        today = datetime.now().date()
        twelve_months_ago = today - timedelta(days=365)
        
        # Vendas por mês
        monthly_sales = db.session.query(
            extract('year', Sale.sale_date).label('year'),
            extract('month', Sale.sale_date).label('month'),
            func.sum(Sale.total_amount).label('total_revenue'),
            func.count(Sale.id).label('total_sales')
        ).filter(
            Sale.sale_date >= twelve_months_ago
        ).group_by(
            extract('year', Sale.sale_date),
            extract('month', Sale.sale_date)
        ).order_by(
            extract('year', Sale.sale_date),
            extract('month', Sale.sale_date)
        ).all()
        
        chart_data = []
        for year, month, revenue, sales_count in monthly_sales:
            month_name = datetime(int(year), int(month), 1).strftime('%b %Y')
            chart_data.append({
                'month': month_name,
                'revenue': float(revenue),
                'sales_count': int(sales_count)
            })
        
        return jsonify(chart_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/top-products', methods=['GET'])
@jwt_required()
def get_top_products():
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.now().date() - timedelta(days=days)
        
        top_products = db.session.query(
            Product.name,
            Product.final_price,
            func.sum(SaleItem.quantity).label('total_sold'),
            func.sum(SaleItem.total_price).label('total_revenue')
        ).join(SaleItem).join(Sale).filter(
            Sale.sale_date >= start_date
        ).group_by(
            Product.id, Product.name, Product.final_price
        ).order_by(
            func.sum(SaleItem.quantity).desc()
        ).limit(10).all()
        
        result = []
        for name, price, quantity, revenue in top_products:
            result.append({
                'name': name,
                'price': float(price) if price else 0,
                'quantity_sold': int(quantity),
                'total_revenue': float(revenue)
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

