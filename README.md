# 📊 Rule-Based Graph Generator

A Flask web application that generates interactive financial charts using Plotly with built-in validation rules.

## Features

- ✅ **10+ Graph Types**: Line, Bar, Scatter, Pie, Histogram, Box Plot, Candlestick, Heatmap, Area, and more
- ✅ **Smart Validation**: Automatic data validation for each graph type
- ✅ **Interactive Charts**: Powered by Plotly for zoom, pan, and hover interactions
- ✅ **Sample Financial Data**: Built-in random financial dataset for testing
- ✅ **Real-time Feedback**: Instant error messages and warnings
- ✅ **Privacy-First**: All data processing happens locally

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/graph-generator.git
cd graph-generator
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
http://localhost:5000

3. Configure your graph:
   - Enter a title
   - Select graph type
   - Choose X and Y axis columns
   - Click "Generate Graph"

## Supported Graph Types

| Graph Type | Best For | Validation Rules |
|-----------|----------|------------------|
| Line Chart | Time series trends | Numeric Y-axis, ≥3 points |
| Bar Chart | Category comparison | Numeric Y-axis, ≤50 categories |
| Scatter Plot | Correlation analysis | Both axes numeric, ≥5 points |
| Pie Chart | Proportions | Numeric values, 2-8 categories |
| Histogram | Distribution | Numeric data, ≥10 points |
| Box Plot | Statistical spread | Numeric data, ≥5 points per group |
| Candlestick | Stock prices | Requires OHLC columns |
| Heatmap | Pattern analysis | Numeric values in matrix |
| Area Chart | Cumulative trends | Numeric Y-axis |

## Project Structure
graph-generator/
├── app.py                 # Flask routes and API endpoints
├── data_generator.py      # Sample data creation
├── graph_generator.py     # Graph generation and validation logic
├── templates/
│   └── index.html        # Frontend UI
└── static/
└── style.css         # Styling

## API Endpoints

- `GET /` - Main application page
- `GET /api/columns` - Get available data columns
- `GET /api/data-preview` - Get data preview
- `GET /api/graph-types` - Get available graph types
- `POST /api/generate-graph` - Generate graph based on inputs

## Customization

### Using Your Own Data

Replace the data generation in `app.py`:
```python
# Instead of:
df = DataGenerator.generate_financial_data(days=365)

# Use:
df = pd.read_csv('your_data.csv')
```

### Adding New Graph Types

1. Add validation rules in `graph_generator.py` → `GraphValidator.validate()`
2. Add generation method in `graph_generator.py` → `GraphGenerator`
3. Update graph types list in `app.py` → `get_graph_types()`

## Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

## License

MIT License - feel free to use for personal or commercial projects!

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## Author

Hemanth Yarra - AI Engineer