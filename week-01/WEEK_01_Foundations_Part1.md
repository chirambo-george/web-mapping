# WEEK 1: Flask Basics & Folium Introduction

**Phase:** Foundations (Days 1–20)  
**Target Hours:** 15–20 hrs/week  
**Focus:** Set up development environment, learn Flask fundamentals, create first Folium map

---

## Daily Breakdown

### Day 1: Environment Setup + Flask "Hello World"

**Morning (2–3 hrs):**
- [ ] Create virtual environment
- [ ] Install dependencies (Flask, Folium, Pandas, GeoPandas)
- [ ] Create project directory structure
- [ ] Initialize Git repo + first commit

**Code:**
```bash
python -m venv geo_web
source geo_web/bin/activate  # macOS/Linux
pip install flask folium pandas geopandas shapely

mkdir geo-web-mapping
cd geo-web-mapping
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

**Afternoon (2–3 hrs):**
- [ ] Create `app.py` with Flask "Hello World"
- [ ] Create `templates/` directory
- [ ] Create simple `index.html`
- [ ] Run Flask development server locally
- [ ] Test: navigate to `http://localhost:5000`

**Code (`app.py`):**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Home')

if __name__ == '__main__':
    app.run(debug=True)
```

**Code (`templates/index.html`):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>Welcome to Geospatial Web Mapping</h1>
    <p>This is your first Flask app.</p>
</body>
</html>
```

**End of Day 1:**
- [ ] Commit to GitHub: "Initial Flask setup"
- [ ] Record time spent
- [ ] Note any blockers

---

### Day 2: Folium Basics & First Map

**Morning (2–3 hrs):**
- [ ] Read Folium documentation (chapters 1–2): https://python-visualization.github.io/folium/
- [ ] Understand: map tiles, center coordinates, zoom levels, markers

**Topics to cover:**
- Creating a basic map object
- Setting location (latitude, longitude)
- Choosing map tiles (OpenStreetMap, Stamen, etc.)
- Adding markers with popups
- Saving map to HTML

**Code Walkthrough (create `test_folium.py`):**
```python
import folium

# Create a map centered on Malawi
map_malawi = folium.Map(
    location=[-13.3, 34.3],  # Center of Malawi
    zoom_start=7,
    tiles='OpenStreetMap'
)

# Add a marker
folium.Marker(
    location=[-13.9626, 33.7741],
    popup='Lilongwe',
    tooltip='Capital of Malawi'
).add_to(map_malawi)

# Save to HTML file
map_malawi.save('test_map.html')
print("Map saved to test_map.html")
```

**Run locally:**
```bash
python test_folium.py
# Open test_map.html in browser
```

**Afternoon (2–3 hrs):**
- [ ] Integrate Folium into Flask app
- [ ] Create new route: `/map` that serves Folium map
- [ ] Create `templates/map.html` with Folium output
- [ ] Test locally

**Code (`app.py` updated):**
```python
from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
def map_view():
    # Create map
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add a marker
    folium.Marker(
        location=[-13.9626, 33.7741],
        popup='Lilongwe',
        tooltip='Capital of Malawi'
    ).add_to(m)
    
    # Convert to HTML
    map_html = m._repr_html_()
    
    return render_template('map.html', map=map_html)
```

**Code (`templates/map.html`):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Map</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
</head>
<body>
    <h1>Malawi Map</h1>
    <div style="height: 600px;">
        {{ map | safe }}
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
</body>
</html>
```

**End of Day 2:**
- [ ] Commit to GitHub: "Add Folium map to Flask app"
- [ ] Verify map loads at `http://localhost:5000/map`

---

### Day 3: Multiple Markers & Popups

**Morning (2–3 hrs):**
- [ ] Create sample data file: `data/cities.csv` with Malawi cities
- [ ] Learn to read CSV with Pandas
- [ ] Loop through data, add markers to map

**Code (create `data/cities.csv`):**
```
city,latitude,longitude,population
Lilongwe,-13.9626,33.7741,989318
Blantyre,-15.7848,35.0081,723000
Mzuzu,-11.4658,34.3668,128000
Zomba,-15.3875,35.3254,133000
Kasungu,-13.0233,33.4833,40000
```

**Code (`app.py` updated):**
```python
from flask import Flask, render_template
import folium
import pandas as pd

app = Flask(__name__)

@app.route('/map')
def map_view():
    # Load cities data
    cities_df = pd.read_csv('data/cities.csv')
    
    # Create map
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add markers from data
    for idx, row in cities_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['city']}<br>Pop: {row['population']:,}",
            tooltip=row['city'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    
    map_html = m._repr_html_()
    return render_template('map.html', map=map_html)
```

**Afternoon (2–3 hrs):**
- [ ] Add more marker customization (different colors for different regions)
- [ ] Add popup with formatted information
- [ ] Test with real Malawi city data

**Code enhancement:**
```python
# Color code by region
region_colors = {
    'North': 'green',
    'Central': 'blue',
    'South': 'red'
}

# In loop:
color = region_colors.get(row.get('region', 'Central'), 'gray')
folium.Marker(
    location=[row['latitude'], row['longitude']],
    popup=folium.Popup(
        f"""
        <b>{row['city']}</b><br>
        Region: {row.get('region', 'N/A')}<br>
        Population: {row['population']:,}
        """,
        max_width=250
    ),
    tooltip=row['city'],
    icon=folium.Icon(color=color, icon='info-sign')
).add_to(m)
```

**End of Day 3:**
- [ ] Commit to GitHub: "Add dynamic markers from CSV"
- [ ] Verify map displays all cities correctly
- [ ] Popups show correct information

---

### Day 4: Layer Control & Basic Navigation

**Morning (2–3 hrs):**
- [ ] Learn about layer control in Folium
- [ ] Add multiple basemap options (OpenStreetMap, Satellite, Terrain)
- [ ] Test switching between layers

**Code:**
```python
# Instead of single tiles parameter, use FeatureGroup
m = folium.Map(
    location=[-13.3, 34.3],
    zoom_start=7
)

# Add different tile options
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('Stamen Terrain').add_to(m)
folium.TileLayer('Stamen TonerLite').add_to(m)

# Add layer control
folium.LayerControl().add_to(m)
```

**Afternoon (2–3 hrs):**
- [ ] Create navbar/header for your Flask app
- [ ] Add navigation links (Home, Map, etc.)
- [ ] Create `templates/base.html` (template inheritance)
- [ ] Update `index.html` and `map.html` to extend base

**Code (`templates/base.html`):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Geospatial Web Mapping{% endblock %}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <style>
        body { margin: 0; font-family: Arial, sans-serif; }
        nav { background: #333; padding: 15px; }
        nav a { color: white; text-decoration: none; margin-right: 20px; }
        .container { padding: 20px; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/map">Map</a>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**Code (`templates/index.html` updated):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Welcome to Geospatial Web Mapping</h1>
<p>Learn to build interactive maps with Flask and Folium.</p>
<a href="/map">View Map</a>
{% endblock %}
```

**Code (`templates/map.html` updated):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Interactive Map</h1>
<div style="height: 600px;">
    {{ map | safe }}
</div>
{% endblock %}
```

**End of Day 4:**
- [ ] Commit to GitHub: "Add base template + layer control"
- [ ] Navigation working across pages

---

### Day 5: GitHub Deploy + Week Review

**Morning (2–3 hrs):**
- [ ] Ensure all code is committed to GitHub
- [ ] Create detailed `README.md` for your repo
- [ ] Document project structure and how to run locally

**Code (`README.md`):**
```markdown
# Geospatial Web Mapping with Flask + Folium

## Overview
An interactive map application displaying Malawi cities using Flask backend and Folium for mapping.

## Setup

```bash
python -m venv geo_web
source geo_web/bin/activate
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## Features
- Display cities on interactive map
- Multiple basemap options
- Popups with city information
- Layer control

## Project Structure
- `app.py` - Main Flask application
- `templates/` - HTML templates
- `data/` - CSV data files
- `requirements.txt` - Python dependencies

## Next Steps
- Add GeoJSON file support
- Connect to PostGIS database
- Add spatial analysis features
```

**Afternoon (2–3 hrs):**
- [ ] Deploy to free tier (Heroku, Railway, or PythonAnywhere)
- [ ] Document deployment process
- [ ] Test live app
- [ ] Share live URL

**Deployment Step-by-Step (Heroku example):**
```bash
# Install Heroku CLI
pip install gunicorn
echo "gunicorn==20.1.0" >> requirements.txt

# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create Heroku app
heroku login
heroku create geo-web-mapping-yourname
git push heroku main

# View live app
heroku open
```

**End of Day 5:**
- [ ] Commit final code
- [ ] Live app deployed (record URL: ________________)
- [ ] README updated with deployment info

---

## Week 1 Checklist

- [ ] Virtual environment created + dependencies installed
- [ ] Flask "Hello World" working locally
- [ ] Folium map created + displayed in Flask
- [ ] CSV data loaded + markers added to map
- [ ] Base template (Jinja2) implemented
- [ ] Navigation between pages working
- [ ] Layer control implemented
- [ ] App deployed to free tier (live URL recorded)
- [ ] GitHub repo with clean commits
- [ ] README with setup instructions

---

## Week 1 Summary

**Skills Gained:**
- Flask routing and templating
- Folium map creation and markers
- Pandas data loading
- Template inheritance (Jinja2)
- Basic web deployment

**Code Created:**
- `app.py` (Flask application)
- `templates/base.html`, `index.html`, `map.html`
- `data/cities.csv` (sample data)
- `README.md`, `.gitignore`

**Deliverable:**
- Live Flask + Folium app with Malawi cities displayed

**Time Spent:** _____ hours

**Blockers Encountered:**
_________________________________________________________________

**Next Week Preview:**
Week 2 will focus on loading GeoJSON files, filtering data by region, and adding more interactivity (zooming to features, layer organization).

---

## Resources Used This Week

- Flask Official Docs: https://flask.palletsprojects.com/
- Folium Docs: https://python-visualization.github.io/folium/
- Jinja2 Templates: https://jinja.palletsprojects.com/
- Leaflet.js (underlying library): https://leafletjs.com/

**Questions to explore next week:**
- How do I load and display shapefiles?
- How do I make popups more interactive?
- How do I optimize map performance with many features?
