# Flask + Folium Geospatial Web Mapping Template

This is a production-ready project structure to start your first geospatial web app immediately.

---

## Directory Structure

```
geo-web-mapping/
├── app.py                    # Main Flask application
├── config.py                 # Configuration (DB, API keys, etc.)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── data/
│   ├── malawi_boundaries.geojson
│   ├── malawi_ea.shp
│   └── README.md
├── templates/
│   ├── base.html             # Base template (navbar, etc.)
│   ├── index.html            # Landing page
│   └── map.html              # Map page template
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── map_interactions.js
│   └── img/
├── geo_utils/
│   ├── __init__.py
│   ├── spatial_ops.py        # GeoPandas functions
│   └── db_queries.py         # PostGIS queries
└── tests/
    ├── __init__.py
    └── test_spatial_ops.py   # Unit tests
```

---

## Quick Start (Days 1–3)

### 1. Clone & Setup

```bash
# Create and activate virtual environment
python3 -m venv geo_web
source geo_web/bin/activate  # macOS/Linux
# or: geo_web\Scripts\activate  # Windows

# Clone this template (or initialize new repo)
git clone <repo_url> geo-web-mapping
cd geo-web-mapping

# Install dependencies
pip install -r requirements.txt
```

### 2. Copy Environment Template

```bash
cp .env.example .env
# Edit .env with your settings (database URL, debug mode, etc.)
```

### 3. Run Locally

```bash
python app.py
# Visit http://localhost:5000 in browser
```

---

## `requirements.txt`

```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
folium==0.14.0
geopandas==0.13.0
shapely==2.0.1
pandas==2.0.3
requests==2.31.0
python-dotenv==1.0.0
gunicorn==20.1.0
psycopg2-binary==2.9.6  # PostgreSQL adapter
geoalchemy2==0.13.1      # SQLAlchemy + PostGIS
```

---

## `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///geo_dev.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/geo_prod'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

---

## `.env.example`

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database (for development)
DEV_DATABASE_URL=sqlite:///geo_dev.db

# Database (for production)
DATABASE_URL=postgresql://username:password@localhost:5432/geo_prod

# Geospatial data paths
DATA_DIR=./data

# PostGIS (if using)
POSTGIS_HOST=localhost
POSTGIS_PORT=5432
POSTGIS_DB=geo_prod
POSTGIS_USER=postgres
POSTGIS_PASSWORD=postgres
```

---

## `app.py` (Minimal Example)

```python
import os
from flask import Flask, render_template, request, jsonify
from config import config
import geopandas as gpd
import folium
from geo_utils.spatial_ops import create_choropleth_map

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    return app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/map')
def map_view():
    """Serve interactive map"""
    # Load GeoJSON
    geojson_path = os.path.join(app.config['DATA_DIR'], 'malawi_boundaries.geojson')
    gdf = gpd.read_file(geojson_path)
    
    # Create base map (Malawi center)
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add GeoJSON layer
    folium.GeoJson(
        geojson_path,
        name='Admin Boundaries',
        popup=folium.GeoJsonPopup(fields=['NAME_1', 'NAME_2'])
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Save to template variable
    map_html = m._repr_html_()
    
    return render_template('map.html', map_html=map_html)

@app.route('/api/query', methods=['POST'])
def spatial_query():
    """Handle spatial queries (AJAX)"""
    data = request.get_json()
    # geometry = data.get('geometry')  # GeoJSON from frontend
    # results = perform_spatial_query(geometry)
    # return jsonify(results)
    return jsonify({'status': 'ok'})

@app.route('/api/export/<format>')
def export_data(format):
    """Export results as CSV or GeoJSON"""
    if format == 'csv':
        # Generate CSV
        pass
    elif format == 'geojson':
        # Generate GeoJSON
        pass
    return 'Not yet implemented'

if __name__ == '__main__':
    app.run(debug=True)
```

---

## `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Geospatial Web Mapping{% endblock %}</title>
    
    <!-- Folium + Leaflet CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.min.css" />
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="container">
            <h1 class="brand"><a href="/">Geo Web Mapping</a></h1>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/map">Map</a></li>
                <li><a href="/docs">Docs</a></li>
            </ul>
        </div>
    </nav>
    
    <!-- Main content -->
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>
        <p>&copy; 2024 Geospatial Web Mapping | Built with Flask + Folium</p>
    </footer>
    
    <!-- Leaflet + Folium JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.min.js"></script>
    
    <script src="{{ url_for('static', filename='js/map_interactions.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## `templates/map.html`

```html
{% extends "base.html" %}

{% block title %}Map - Geospatial Explorer{% endblock %}

{% block content %}
<div class="map-container">
    <div class="map-sidebar">
        <h2>Controls</h2>
        <label>
            Select Region:
            <select id="region-select">
                <option value="">All</option>
                <option value="north">North</option>
                <option value="central">Central</option>
                <option value="south">South</option>
            </select>
        </label>
        <div id="stats">
            <p>Click a polygon for details.</p>
        </div>
    </div>
    
    <div id="map">
        <!-- Folium map rendered here -->
        {{ map_html | safe }}
    </div>
</div>

<style>
    .map-container {
        display: flex;
        height: calc(100vh - 120px);
    }
    .map-sidebar {
        width: 250px;
        padding: 20px;
        background: #f5f5f5;
        overflow-y: auto;
    }
    #map {
        flex: 1;
    }
</style>

{% endblock %}

{% block extra_js %}
<script>
    // Handle region selection
    document.getElementById('region-select').addEventListener('change', function() {
        let region = this.value;
        // AJAX call to backend to filter map
        fetch('/api/filter_region', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ region: region })
        }).then(r => r.json()).then(data => {
            console.log('Filtered data:', data);
            // Update map (you'd implement this)
        });
    });
</script>
{% endblock %}
```

---

## `geo_utils/spatial_ops.py`

```python
import geopandas as gpd
from shapely.geometry import box
import pandas as pd

def load_geojson(filepath):
    """Load GeoJSON file as GeoDataFrame"""
    return gpd.read_file(filepath)

def spatial_intersect(gdf, geometry):
    """Find all features intersecting a geometry"""
    return gdf[gdf.geometry.intersects(geometry)]

def spatial_buffer(gdf, distance_m):
    """Buffer geometries by distance (meters)"""
    gdf_copy = gdf.copy()
    gdf_copy['geometry'] = gdf.geometry.buffer(distance_m)
    return gdf_copy

def aggregate_by_region(gdf, region_col, agg_col):
    """Aggregate data by region"""
    return gdf.groupby(region_col)[agg_col].sum()

def create_choropleth_map(gdf, column, geom_col='geometry'):
    """Create folium choropleth from GeoDataFrame"""
    import folium
    
    # Get bounds
    bounds = gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
    # Create map
    m = folium.Map(location=center, zoom_start=8)
    
    # Add choropleth
    folium.Choropleth(
        geo_data=gdf,
        columns=['ID', column],
        fill_color='YlOrRd',
        name='Choropleth'
    ).add_to(m)
    
    return m
```

---

## `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Flask
instance/
.webassets-cache

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Database
*.db
*.sqlite
*.sqlite3

# Data (optional)
data/large_files/
*.shp
*.shx
*.dbf
*.prj
```

---

## `README.md` Template

```markdown
# Geospatial Web Mapping with Flask + Folium

A Python web application for interactive geospatial visualization and analysis.

## Features

- Interactive map with Folium + Leaflet
- Spatial queries (buffer, intersect, clip)
- Choropleth mapping
- Data export (CSV, GeoJSON)
- PostGIS integration (optional)

## Prerequisites

- Python 3.8+
- PostgreSQL + PostGIS (optional, for production)

## Installation

```bash
git clone <repo_url>
cd geo-web-mapping
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Running Locally

```bash
python app.py
# Visit http://localhost:5000
```

## Deployment

See `DEPLOYMENT.md` for Heroku/Railway instructions.

## Project Structure

- `app.py` — Main Flask application
- `geo_utils/` — Spatial operations + database queries
- `templates/` — HTML templates
- `static/` — CSS, JavaScript, images
- `data/` — Sample geospatial data

## Contributing

1. Fork this repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/my-feature`
5. Submit PR

## License

MIT License (or your choice)

## Author

George, NSO Malawi | [Portfolio](https://example.com) | [LinkedIn](https://linkedin.com/in/yourprofile)
```

---

## Next Steps

1. **Copy this structure** into a new GitHub repo
2. **Fill in `.env.example`** with your settings
3. **Run `pip install -r requirements.txt`**
4. **Start with `app.py`** and run locally
5. **Commit to GitHub** daily
6. **Deploy to Heroku/Railway** by day 3

---

## Troubleshooting

**Folium map not rendering:**
- Ensure `map_html | safe` in template (Jinja2 must not escape HTML)
- Check browser console for JavaScript errors

**GeoJSON not loading:**
- Verify file path is correct (use `os.path.join()`)
- Ensure GeoJSON is valid (use geojson.io to validate)

**PostGIS connection error:**
- Check `.env` DATABASE_URL format: `postgresql://user:password@host:5432/dbname`
- Verify PostgreSQL service is running

---

**Now start coding. Day 1 goal: Get this running locally + push to GitHub.**
