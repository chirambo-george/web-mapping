# WEEK 4: PostGIS Integration & Spatial Queries

**Phase:** Intermediate Skills (Days 21–50)  
**Target Hours:** 15–20 hrs/week  
**Focus:** Set up PostGIS database, load spatial data, query from Flask

---

## Daily Breakdown

### Day 16: PostgreSQL + PostGIS Installation

**Morning (2–3 hrs):**
- [ ] Install PostgreSQL (local or cloud)
- [ ] Install PostGIS extension
- [ ] Create database for Malawi data
- [ ] Verify installation

**Installation Steps (macOS with Homebrew):**
```bash
# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Start PostgreSQL if not auto-started
brew services restart postgresql

# Connect to default database
psql postgres

# Create new database for geodata
CREATE DATABASE malawi_geo;

# Connect to new database
psql malawi_geo

# Install PostGIS extension
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

# Verify installation
SELECT PostGIS_Version();
\q  # Exit psql
```

**Installation (Windows with installer):**
- Download PostgreSQL installer from https://www.postgresql.org/
- During installation, enable PostGIS in "Stack Builder"
- PostGIS extension auto-installed

**Installation (Ubuntu/Linux):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib postgis

sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql

# Inside psql:
CREATE DATABASE malawi_geo;
\c malawi_geo
CREATE EXTENSION postgis;
SELECT PostGIS_Version();
\q
```

**Verification:**
```bash
# Verify PostGIS installed
psql malawi_geo -c "SELECT PostGIS_Version();"
```

**Afternoon (2–3 hrs):**
- [ ] Create spatial tables (admin boundaries, facilities)
- [ ] Plan table structure for Malawi data
- [ ] Create schema document

**Code (`deployment/postgis_setup.sql`):**
```sql
-- Create admin boundaries table
CREATE TABLE admin_boundaries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    level INTEGER,  -- 0=country, 1=region, 2=district
    population INTEGER,
    area_sqkm NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add geometry column
SELECT AddGeometryColumn('admin_boundaries', 'geom', 4326, 'POLYGON', 2);

-- Create index for performance
CREATE INDEX idx_admin_geom ON admin_boundaries USING GIST(geom);

-- Create facilities table
CREATE TABLE facilities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    facility_type VARCHAR(100),  -- Hospital, School, Water Point, etc.
    region VARCHAR(100),
    district VARCHAR(100),
    visits INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add geometry column (point locations)
SELECT AddGeometryColumn('facilities', 'geom', 4326, 'POINT', 2);

-- Create spatial index
CREATE INDEX idx_facilities_geom ON facilities USING GIST(geom);

-- Create EA (Enumeration Area) table
CREATE TABLE enumeration_areas (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE,
    district VARCHAR(100),
    region VARCHAR(100),
    population INTEGER,
    households INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT AddGeometryColumn('enumeration_areas', 'geom', 4326, 'POLYGON', 2);
CREATE INDEX idx_ea_geom ON enumeration_areas USING GIST(geom);

-- Create statistical data table (linked to boundaries)
CREATE TABLE statistics (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER REFERENCES admin_boundaries(id),
    metric_name VARCHAR(100),
    metric_value NUMERIC,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Run setup:**
```bash
psql malawi_geo < deployment/postgis_setup.sql
```

**End of Day 16:**
- [ ] Commit to GitHub: "Add PostGIS database setup script"
- [ ] Database created and verified
- [ ] Tables created with spatial columns

---

### Day 17: Load Shapefiles into PostGIS

**Morning (2–3 hrs):**
- [ ] Install ogr2ogr tool (part of GDAL)
- [ ] Prepare Malawi shapefiles
- [ ] Convert shapefiles to SQL and import

**Installation:**
```bash
# macOS
brew install gdal

# Ubuntu/Linux
sudo apt-get install gdal-bin

# Windows: Download from https://trac.osgeo.org/osgeo4w/
```

**Verify:**
```bash
ogr2ogr --version
```

**Afternoon (2–3 hrs):**
- [ ] Load Malawi admin boundaries
- [ ] Load facility point data
- [ ] Verify data in PostGIS

**Import shapefiles using ogr2ogr:**
```bash
# Import admin boundaries (shapefiles)
# Note: Replace 'path/to/shapefiles' with actual path
ogr2ogr -f PostgreSQL PG:"dbname=malawi_geo user=postgres password=yourpassword" \
  -nln admin_boundaries \
  -overwrite \
  path/to/malawi_districts.shp

# Import facilities
ogr2ogr -f PostgreSQL PG:"dbname=malawi_geo user=postgres password=yourpassword" \
  -nln facilities \
  -overwrite \
  path/to/facilities.shp

# Or import from GeoJSON
ogr2ogr -f PostgreSQL PG:"dbname=malawi_geo user=postgres password=yourpassword" \
  -nln admin_boundaries \
  -overwrite \
  data/malawi_districts.geojson
```

**Verify import in psql:**
```bash
psql malawi_geo

-- Check tables
\dt

-- Check admin_boundaries
SELECT name, ST_AsText(ST_Centroid(geom)) FROM admin_boundaries LIMIT 5;

-- Check geometry type
SELECT ST_GeometryType(geom) FROM admin_boundaries LIMIT 1;

-- Count records
SELECT COUNT(*) FROM admin_boundaries;
SELECT COUNT(*) FROM facilities;

\q
```

**End of Day 17:**
- [ ] Commit to GitHub: "Load Malawi shapefiles into PostGIS"
- [ ] Data verified in database
- [ ] Can query tables from psql

---

### Day 18: Flask + SQLAlchemy Connection

**Morning (2–3 hrs):**
- [ ] Install SQLAlchemy + GeoAlchemy2
- [ ] Create Flask config for database
- [ ] Test database connection

**Install:**
```bash
pip install sqlalchemy geoalchemy2 psycopg2-binary
```

**Code (`config.py` - updated):**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development with SQLite"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///geo_dev.db'

class ProductionConfig(Config):
    """Production with PostGIS"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # DATABASE_URL format: postgresql://user:password@localhost:5432/malawi_geo

class TestingConfig(Config):
    """Testing with SQLite"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

**Code (`models.py` - new file):**
```python
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from datetime import datetime

db = SQLAlchemy()

class AdminBoundary(db.Model):
    """Admin boundary (district, region, etc.)"""
    __tablename__ = 'admin_boundaries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(100))
    level = db.Column(db.Integer)  # 0=country, 1=region, 2=district
    population = db.Column(db.Integer)
    area_sqkm = db.Column(db.Numeric)
    geom = db.Column(Geometry('POLYGON', srid=4326))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'region': self.region,
            'population': self.population,
            'area_sqkm': float(self.area_sqkm) if self.area_sqkm else None
        }

class Facility(db.Model):
    """Facility (hospital, school, water point, etc.)"""
    __tablename__ = 'facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    facility_type = db.Column(db.String(100))
    region = db.Column(db.String(100))
    district = db.Column(db.String(100))
    visits = db.Column(db.Integer, default=0)
    geom = db.Column(Geometry('POINT', srid=4326))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'facility_type': self.facility_type,
            'region': self.region,
            'district': self.district
        }

class EnumerationArea(db.Model):
    """Census enumeration area"""
    __tablename__ = 'enumeration_areas'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    district = db.Column(db.String(100))
    region = db.Column(db.String(100))
    population = db.Column(db.Integer)
    households = db.Column(db.Integer)
    geom = db.Column(Geometry('POLYGON', srid=4326))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'district': self.district,
            'region': self.region,
            'population': self.population
        }
```

**Afternoon (2–3 hrs):**
- [ ] Update Flask app to use SQLAlchemy
- [ ] Test database connection
- [ ] Verify models work

**Code (`app.py` - updated):**
```python
from flask import Flask, render_template, request, jsonify
from config import config
from models import db, AdminBoundary, Facility, EnumerationArea
import os
from geoalchemy2.functions import ST_AsGeoJSON

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load config
    if config_name == 'production':
        app.config.from_object(config['production'])
    else:
        app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/districts')
def get_districts():
    """Get all districts as JSON"""
    districts = AdminBoundary.query.all()
    return jsonify([d.to_dict() for d in districts])

@app.route('/api/district/<int:id>')
def get_district(id):
    """Get specific district"""
    district = AdminBoundary.query.get_or_404(id)
    return jsonify(district.to_dict())

@app.route('/test-db')
def test_db():
    """Test database connection"""
    try:
        count = AdminBoundary.query.count()
        return jsonify({
            'status': 'connected',
            'admin_boundaries_count': count,
            'database': app.config.get('SQLALCHEMY_DATABASE_URI', 'N/A')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

**Update `.env`:**
```bash
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/malawi_geo
DEV_DATABASE_URL=sqlite:///geo_dev.db
```

**Test connection:**
```bash
# Start Flask app
python app.py

# Visit http://localhost:5000/test-db
# Should return: { "status": "connected", "admin_boundaries_count": X }
```

**End of Day 18:**
- [ ] Commit to GitHub: "Add Flask+SQLAlchemy database models"
- [ ] Database connection verified
- [ ] `/test-db` endpoint returns correct data

---

### Day 19: Spatial Queries from Flask

**Morning (2–3 hrs):**
- [ ] Learn PostGIS spatial functions (ST_DWithin, ST_Intersects, ST_Contains, ST_Buffer)
- [ ] Write spatial query functions
- [ ] Test queries in psql first

**PostGIS Query Examples (in psql):**
```sql
-- Find districts with population > 500,000
SELECT name, population FROM admin_boundaries 
WHERE population > 500000;

-- Find facilities within 10km of a point (Lilongwe: 33.7741, -13.9626)
SELECT name, facility_type FROM facilities
WHERE ST_DWithin(
    geom,
    ST_SetSRID(ST_MakePoint(33.7741, -13.9626), 4326),
    10000  -- 10km in meters
);

-- Find all facilities within a district
SELECT f.name, f.facility_type FROM facilities f
WHERE ST_Contains(
    (SELECT geom FROM admin_boundaries WHERE name = 'Lilongwe'),
    f.geom
);

-- Calculate distance between two geometries
SELECT name,
    ST_Distance(
        ST_SetSRID(ST_MakePoint(33.7741, -13.9626), 4326),
        geom
    ) / 1000 AS distance_km
FROM facilities
ORDER BY distance_km
LIMIT 10;
```

**Afternoon (2–3 hrs):**
- [ ] Create query utility functions
- [ ] Add Flask routes for spatial queries
- [ ] Test all queries work

**Code (`geo_utils/db_queries.py` - new file):**
```python
from flask import current_app
from geoalchemy2.functions import ST_AsGeoJSON, ST_DWithin, ST_Contains, ST_Intersects, ST_Distance, ST_Buffer, ST_MakePoint, ST_SetSRID
from sqlalchemy import func, text
from models import AdminBoundary, Facility, EnumerationArea, db
from geoalchemy2 import Geometry

def get_all_districts():
    """Get all administrative districts"""
    return AdminBoundary.query.filter_by(level=2).all()

def get_district_by_name(name):
    """Get district by name"""
    return AdminBoundary.query.filter_by(name=name).first()

def get_district_by_region(region):
    """Get all districts in a region"""
    return AdminBoundary.query.filter_by(region=region).all()

def facilities_near_point(lon, lat, distance_m):
    """Find facilities within distance of a point
    
    Args:
        lon, lat: coordinates
        distance_m: distance in meters
    
    Returns:
        List of facilities
    """
    point = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
    query = Facility.query.filter(
        ST_DWithin(Facility.geom, point, distance_m)
    )
    return query.all()

def facilities_within_district(district_name):
    """Find all facilities within a district
    
    Args:
        district_name: name of district
    
    Returns:
        List of facilities
    """
    district = AdminBoundary.query.filter_by(name=district_name).first()
    if not district:
        return []
    
    query = Facility.query.filter(
        ST_Contains(district.geom, Facility.geom)
    )
    return query.all()

def facilities_within_polygon(geom_geojson):
    """Find all facilities within a polygon
    
    Args:
        geom_geojson: GeoJSON geometry string
    
    Returns:
        List of facilities
    """
    query = text(f"""
        SELECT * FROM facilities
        WHERE ST_Contains(
            ST_GeomFromGeoJSON('{geom_geojson}'),
            geom
        )
    """)
    return db.session.execute(query).fetchall()

def calculate_facility_density(district_name):
    """Calculate facility density (facilities per 1000 km²)
    
    Args:
        district_name: name of district
    
    Returns:
        Density value
    """
    district = AdminBoundary.query.filter_by(name=district_name).first()
    if not district:
        return None
    
    facility_count = Facility.query.filter(
        ST_Contains(district.geom, Facility.geom)
    ).count()
    
    area_sqkm = float(district.area_sqkm) if district.area_sqkm else 1
    density = (facility_count / area_sqkm) * 1000
    
    return density

def distance_between_points(lon1, lat1, lon2, lat2):
    """Calculate distance between two points (in meters)"""
    query = text(f"""
        SELECT ST_Distance(
            ST_SetSRID(ST_MakePoint({lon1}, {lat1}), 4326),
            ST_SetSRID(ST_MakePoint({lon2}, {lat2}), 4326)
        ) AS distance
    """)
    result = db.session.execute(query).fetchone()
    return result[0] if result else None

def get_nearest_facilities(lon, lat, limit=5):
    """Find nearest facilities to a point
    
    Args:
        lon, lat: coordinates
        limit: number of results
    
    Returns:
        List of facilities ordered by distance
    """
    point = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
    query = db.session.query(
        Facility,
        func.ST_Distance(Facility.geom, point).label('distance')
    ).order_by('distance').limit(limit)
    
    return query.all()

def buffer_district(district_name, buffer_m):
    """Get buffered area around district
    
    Args:
        district_name: name of district
        buffer_m: buffer distance in meters
    
    Returns:
        Buffered geometry as GeoJSON
    """
    query = text(f"""
        SELECT ST_AsGeoJSON(
            ST_Buffer(
                (SELECT geom FROM admin_boundaries WHERE name = '{district_name}'),
                {buffer_m}
            )
        ) AS buffered_geom
    """)
    result = db.session.execute(query).fetchone()
    return result[0] if result else None
```

**Flask routes (`app.py` - add these):**
```python
from geo_utils.db_queries import (
    get_all_districts, facilities_near_point, facilities_within_district,
    get_nearest_facilities, calculate_facility_density, distance_between_points
)

@app.route('/api/spatial/nearest-facilities')
def api_nearest_facilities():
    """Find nearest facilities to a point
    
    Query params: lon, lat, limit
    Example: /api/spatial/nearest-facilities?lon=33.7741&lat=-13.9626&limit=5
    """
    try:
        lon = float(request.args.get('lon', 0))
        lat = float(request.args.get('lat', 0))
        limit = int(request.args.get('limit', 5))
        
        facilities = get_nearest_facilities(lon, lat, limit)
        
        return jsonify({
            'status': 'success',
            'count': len(facilities),
            'facilities': [f[0].to_dict() for f in facilities]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/spatial/facilities-in-district')
def api_facilities_in_district():
    """Find all facilities within a district
    
    Query params: district
    Example: /api/spatial/facilities-in-district?district=Lilongwe
    """
    try:
        district = request.args.get('district')
        if not district:
            return jsonify({'status': 'error', 'message': 'District required'}), 400
        
        facilities = facilities_within_district(district)
        
        return jsonify({
            'status': 'success',
            'district': district,
            'count': len(facilities),
            'facilities': [f.to_dict() for f in facilities]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/spatial/facility-density')
def api_facility_density():
    """Calculate facility density for a district
    
    Query params: district
    """
    try:
        district = request.args.get('district')
        if not district:
            return jsonify({'status': 'error', 'message': 'District required'}), 400
        
        density = calculate_facility_density(district)
        
        return jsonify({
            'status': 'success',
            'district': district,
            'density_per_1000sqkm': density
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
```

**End of Day 19:**
- [ ] Commit to GitHub: "Add PostGIS spatial query functions"
- [ ] Test queries: `/api/spatial/nearest-facilities`, `/api/spatial/facilities-in-district`
- [ ] Verify results are correct

---

### Day 20: Census Explorer with PostGIS Backend

**Morning (2–3 hrs):**
- [ ] Build Census Explorer UI
- [ ] Integrate PostGIS queries into Flask routes
- [ ] Load EA (Enumeration Area) data

**Code (`app.py` - add Census Explorer route):**
```python
@app.route('/census-explorer')
def census_explorer():
    """Interactive census data explorer"""
    
    # Get filter parameters
    region = request.args.get('region', '')
    district = request.args.get('district', '')
    
    # Query data
    query = EnumerationArea.query
    
    if region:
        query = query.filter_by(region=region)
    if district:
        query = query.filter_by(district=district)
    
    eas = query.all()
    
    # Calculate statistics
    stats = {
        'total_eas': len(eas),
        'total_population': sum(ea.population for ea in eas),
        'total_households': sum(ea.households for ea in eas) if eas else 0,
        'avg_population': sum(ea.population for ea in eas) / len(eas) if eas else 0,
        'avg_households': sum(ea.households for ea in eas) / len(eas) if eas else 0
    }
    
    # Get unique regions and districts
    all_regions = db.session.query(EnumerationArea.region.distinct()).all()
    regions_list = [r[0] for r in all_regions if r[0]]
    
    all_districts = db.session.query(EnumerationArea.district.distinct()).all()
    districts_list = [d[0] for d in all_districts if d[0]]
    
    # Convert to GeoJSON for Folium
    geojson_data = {
        'type': 'FeatureCollection',
        'features': []
    }
    
    for ea in eas:
        feature = {
            'type': 'Feature',
            'properties': {
                'code': ea.code,
                'region': ea.region,
                'district': ea.district,
                'population': ea.population,
                'households': ea.households
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': []  # Would be populated from PostGIS
            }
        }
        geojson_data['features'].append(feature)
    
    return render_template(
        'census_explorer.html',
        regions=regions_list,
        districts=districts_list,
        selected_region=region,
        selected_district=district,
        stats=stats,
        eas_count=len(eas),
        geojson_data=geojson_data
    )
```

**Template (`templates/census_explorer.html`):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Census Data Explorer</h1>

<div style="display: flex; gap: 20px; margin-bottom: 20px;">
    <!-- Filters -->
    <div style="flex: 0 0 250px;">
        <h3>Filters</h3>
        <form method="GET">
            <label><strong>Region:</strong></label>
            <select name="region" onchange="this.form.submit()">
                <option value="">All Regions</option>
                {% for region in regions %}
                    <option value="{{ region }}" {% if region == selected_region %}selected{% endif %}>
                        {{ region }}
                    </option>
                {% endfor %}
            </select>
            
            <br><br>
            
            <label><strong>District:</strong></label>
            <select name="district" onchange="this.form.submit()">
                <option value="">All Districts</option>
                {% for district in districts %}
                    <option value="{{ district }}" {% if district == selected_district %}selected{% endif %}>
                        {{ district }}
                    </option>
                {% endfor %}
            </select>
        </form>
        
        <hr>
        
        <h4>Statistics</h4>
        <p><strong>Enumeration Areas:</strong> {{ stats.total_eas }}</p>
        <p><strong>Total Population:</strong> {{ "{:,.0f}".format(stats.total_population) }}</p>
        <p><strong>Total Households:</strong> {{ "{:,.0f}".format(stats.total_households) }}</p>
        <p><strong>Avg Pop/EA:</strong> {{ "{:,.0f}".format(stats.avg_population) }}</p>
    </div>
    
    <!-- Map -->
    <div style="flex: 1; min-height: 600px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden;">
        <div id="map" style="height: 100%;"></div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
    // Initialize Leaflet map
    const map = L.map('map').setView([-13.3, 34.3], 7);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
        maxZoom: 19
    }).addTo(map);
    
    // Add geojson data
    const geojson_data = {{ geojson_data | tojson }};
    L.geoJSON(geojson_data, {
        onEachFeature: function(feature, layer) {
            const props = feature.properties;
            layer.bindPopup(`
                <b>${props.code}</b><br>
                Region: ${props.region}<br>
                District: ${props.district}<br>
                Population: ${props.population.toLocaleString()}<br>
                Households: ${props.households.toLocaleString()}
            `);
        }
    }).addTo(map);
</script>

<style>
    select {
        width: 100%;
        padding: 8px;
        margin: 10px 0;
    }
    form { margin-bottom: 10px; }
</style>
{% endblock %}
```

**Afternoon (2–3 hrs):**
- [ ] Test Census Explorer with data
- [ ] Verify filters work
- [ ] Verify statistics calculate correctly
- [ ] Deploy to live app

**End of Day 20:**
- [ ] Commit to GitHub: "Add Census Explorer with PostGIS backend"
- [ ] `/census-explorer` route working
- [ ] Filters functional
- [ ] Live app updated

---

## Week 4 Checklist

- [ ] PostgreSQL + PostGIS installed locally
- [ ] Database `malawi_geo` created
- [ ] Spatial tables created (admin_boundaries, facilities, enumeration_areas)
- [ ] Shapefiles/GeoJSON loaded into PostGIS
- [ ] Data verified in psql
- [ ] SQLAlchemy models created for spatial tables
- [ ] Flask app connected to PostGIS database
- [ ] Database connection tested (`/test-db` endpoint)
- [ ] Spatial query functions created (buffer, intersect, distance, etc.)
- [ ] Spatial query routes added to Flask (`/api/spatial/*`)
- [ ] Census Explorer built and functional
- [ ] All routes tested and working
- [ ] All code committed to GitHub
- [ ] Live app deployed with PostGIS backend

---

## Week 4 Summary

**Skills Gained:**
- PostgreSQL + PostGIS installation and setup
- Loading shapefiles into PostGIS (ogr2ogr)
- SQLAlchemy with GeoAlchemy2
- PostGIS spatial functions (ST_DWithin, ST_Contains, ST_Buffer, etc.)
- Spatial queries from Flask
- Creating spatial indexes for performance

**Code Created:**
- `models.py` (SQLAlchemy spatial models)
- `geo_utils/db_queries.py` (spatial query functions)
- `deployment/postgis_setup.sql` (database setup)
- `templates/census_explorer.html`
- New routes: `/test-db`, `/api/spatial/*`, `/census-explorer`

**Deliverable:**
- Census Explorer with PostGIS backend
- API endpoints for spatial queries
- Live app with database-driven data

**GitHub Commits:**
- "Add PostGIS database setup script"
- "Load Malawi shapefiles into PostGIS"
- "Add Flask+SQLAlchemy database models"
- "Add PostGIS spatial query functions"
- "Add Census Explorer with PostGIS backend"

**Time Spent:** _____ hours

**Blockers Encountered:**
_________________________________________________________________

**Lessons Learned:**
_________________________________________________________________

**Next Week Preview:**
Week 5 will focus on optimizing spatial queries, implementing caching, and handling large datasets efficiently.

---

## Resources Used This Week

- PostGIS Manual: https://postgis.net/docs/
- SQLAlchemy + GeoAlchemy2: https://geoalchemy-2.readthedocs.io/
- GDAL/ogr2ogr: https://gdal.org/
- psql interactive terminal: https://www.postgresql.org/docs/current/app-psql.html

**Questions to explore next week:**
- How do I optimize slow spatial queries?
- How do I add database indexes for performance?
- How do I cache query results?
- How do I handle very large shapefiles?
