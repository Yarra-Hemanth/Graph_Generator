from flask import Flask, render_template, request, jsonify
import pandas as pd
from data_generator import DataGenerator
from graph_generator import GraphGenerator
import json

app = Flask(__name__)

# Generate data on startup
print("Generating sample financial data...")
df = DataGenerator.generate_financial_data(days=365)
print(f"Data generated: {df.shape[0]} rows, {df.shape[1]} columns")

# Get column information
column_info = DataGenerator.get_column_info(df)

@app.route('/')
def index():
    '''Render main page'''
    return render_template('index.html')

@app.route('/api/columns', methods=['GET'])
def get_columns():
    '''Get available columns and their types'''
    columns = []
    for col in df.columns:
        columns.append({
            'name': col,
            'type': column_info[col]['type'],
            'is_numeric': column_info[col]['is_numeric'],
            'is_datetime': column_info[col]['is_datetime'],
            'unique_values': column_info[col]['unique_values']
        })
    return jsonify({'columns': columns})

@app.route('/api/data-preview', methods=['GET'])
def get_data_preview():
    '''Get preview of data'''
    preview = df.head(10).to_dict('records')
    # Convert datetime to string for JSON serialization
    for row in preview:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None
            elif isinstance(value, pd.Timestamp):
                row[key] = value.strftime('%Y-%m-%d')
    return jsonify({
        'preview': preview,
        'total_rows': len(df),
        'columns': list(df.columns)
    })

@app.route('/api/generate-graph', methods=['POST'])
def generate_graph():
    '''Generate graph based on user inputs'''
    try:
        data = request.json
        
        graph_type = data.get('graph_type')
        title = data.get('title')
        x_col = data.get('x_axis')
        y_col = data.get('y_axis')
        group_col = data.get('group_by')
        
        # Validate inputs
        if not graph_type:
            return jsonify({'success': False, 'errors': ['Graph type is required']})
        
        if not title:
            return jsonify({'success': False, 'errors': ['Title is required']})
        
        # Generate graph
        generator = GraphGenerator(df)
        result = generator.generate(graph_type, title, x_col, y_col, group_col)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Server error: {str(e)}']
        })

@app.route('/api/graph-types', methods=['GET'])
def get_graph_types():
    '''Get available graph types'''
    graph_types = [
        {'value': 'line', 'label': 'Line Chart', 'description': 'Show trends over time'},
        {'value': 'bar', 'label': 'Bar Chart', 'description': 'Compare categories'},
        {'value': 'scatter', 'label': 'Scatter Plot', 'description': 'Show correlation'},
        {'value': 'pie', 'label': 'Pie Chart', 'description': 'Show proportions'},
        {'value': 'histogram', 'label': 'Histogram', 'description': 'Show distribution'},
        {'value': 'box', 'label': 'Box Plot', 'description': 'Show statistical distribution'},
        {'value': 'candlestick', 'label': 'Candlestick', 'description': 'Stock price movement'},
        {'value': 'heatmap', 'label': 'Heatmap', 'description': 'Show patterns in matrix'},
        {'value': 'area', 'label': 'Area Chart', 'description': 'Show cumulative trends'},
    ]
    return jsonify({'graph_types': graph_types})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)