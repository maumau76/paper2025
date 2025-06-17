from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import func
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from src.models.database import db, Sale, Expense, Material, Product, SaleItem

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/financial', methods=['GET'])
@jwt_required()
def get_financial_report():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            # Padrão: último mês
            today = datetime.now().date()
            end_date = today
            start_date = today.replace(day=1)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Vendas no período
        sales = Sale.query.filter(
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        ).all()
        
        total_revenue = sum(float(sale.total_amount) for sale in sales)
        
        # Despesas no período
        expenses = Expense.query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date
        ).all()
        
        total_expenses = sum(float(expense.amount) for expense in expenses)
        
        # Lucro líquido
        net_profit = total_revenue - total_expenses
        
        # Despesas por categoria
        expenses_by_category = {}
        for expense in expenses:
            category = expense.category or 'Sem categoria'
            if category not in expenses_by_category:
                expenses_by_category[category] = 0
            expenses_by_category[category] += float(expense.amount)
        
        return jsonify({
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'sales_count': len(sales),
            'expenses_count': len(expenses),
            'expenses_by_category': expenses_by_category,
            'sales': [sale.to_dict() for sale in sales],
            'expenses': [expense.to_dict() for expense in expenses]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/inventory', methods=['GET'])
@jwt_required()
def get_inventory_report():
    try:
        # Todos os materiais
        materials = Material.query.all()
        
        # Todos os produtos
        products = Product.query.all()
        
        # Materiais com estoque baixo
        low_stock_materials = [m for m in materials if m.stock_quantity <= m.min_stock_alert]
        
        # Valor total do estoque de materiais
        materials_value = sum(float(m.stock_quantity) * float(m.purchase_price) for m in materials)
        
        # Valor total do estoque de produtos
        products_value = sum(p.stock_quantity * (float(p.final_price) if p.final_price else p.calculate_final_price()) for p in products)
        
        return jsonify({
            'materials': [material.to_dict() for material in materials],
            'products': [product.to_dict() for product in products],
            'low_stock_materials': [material.to_dict() for material in low_stock_materials],
            'summary': {
                'total_materials': len(materials),
                'total_products': len(products),
                'low_stock_count': len(low_stock_materials),
                'materials_value': materials_value,
                'products_value': products_value,
                'total_inventory_value': materials_value + products_value
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales_report():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Sale.query
        
        if start_date:
            query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        sales = query.order_by(Sale.sale_date.desc()).all()
        
        # Estatísticas
        total_sales = len(sales)
        total_revenue = sum(float(sale.total_amount) for sale in sales)
        average_sale = total_revenue / total_sales if total_sales > 0 else 0
        
        # Vendas por método de pagamento
        payment_methods = {}
        for sale in sales:
            method = sale.payment_method
            if method not in payment_methods:
                payment_methods[method] = {'count': 0, 'total': 0}
            payment_methods[method]['count'] += 1
            payment_methods[method]['total'] += float(sale.total_amount)
        
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
            'sales': [sale.to_dict() for sale in sales],
            'summary': {
                'total_sales': total_sales,
                'total_revenue': total_revenue,
                'average_sale': average_sale,
                'payment_methods': payment_methods,
                'top_products': [{'name': name, **data} for name, data in top_products]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/export/pdf', methods=['GET'])
@jwt_required()
def export_pdf_report():
    try:
        report_type = request.args.get('type', 'financial')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Criar PDF em memória
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title = Paragraph(f"Relatório {report_type.title()} - RM Papel", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        if report_type == 'financial':
            # Dados financeiros
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            else:
                today = datetime.now().date()
                end_date = today
                start_date = today.replace(day=1)
            
            sales = Sale.query.filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).all()
            
            expenses = Expense.query.filter(
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date
            ).all()
            
            total_revenue = sum(float(sale.total_amount) for sale in sales)
            total_expenses = sum(float(expense.amount) for expense in expenses)
            net_profit = total_revenue - total_expenses
            
            # Período
            period_text = f"Período: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
            story.append(Paragraph(period_text, styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Resumo financeiro
            summary_data = [
                ['Receitas', f'R$ {total_revenue:.2f}'],
                ['Despesas', f'R$ {total_expenses:.2f}'],
                ['Lucro Líquido', f'R$ {net_profit:.2f}']
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
        
        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'relatorio_{report_type}_{datetime.now().strftime("%Y%m%d")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

