# WEEK 2: GeoJSON & Dynamic Map Filtering

**Phase:** Foundations (Days 1–20)  
**Target Hours:** 15–20 hrs/week  
**Focus:** Load GeoJSON files, filter data by region, add dynamic map updates

---

## Daily Breakdown

### Day 6: GeoJSON Basics & Map Display

**Morning (2–3 hrs):**
- [ ] Understand GeoJSON format (features, geometries, properties)
- [ ] Obtain or create sample GeoJSON for Malawi (admin boundaries)
- [ ] Learn to validate GeoJSON (geojson.io)

**Resources:**
- GeoJSON spec: https://geojson.org/
- GeoJSON validator: https://geojson.io/

**Sample GeoJSON structure:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Lilongwe District",
        "region": "Central",
        "population": 2000000
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon, lat], [lon, lat], ...]]
      }
    }
  ]
}
```

**Where to find real Malawi data:**
- OpenStreetMap (osmdata.openstreetmap.de)
- GADM database (gadm.org) — administrative boundaries
- World Bank Open Data (data.worldbank.org)

**Task:**
- [ ] Download Malawi admin-2 (district) boundaries as GeoJSON
- [ ] Save to `data/malawi_districts.geojson`
- [ ] Validate with geojson.io

**Afternoon (2–3 hrs):**
- [ ] Load GeoJSON in Folium
- [ ] Display on map with popups
- [ ] Test interactive features

**Code (`app.py` updated):**
```python
from flask import Flask, render_template
import folium
import json
import os

app = Flask(__name__)

@app.route('/map')
def map_view():
    # Load GeoJSON
    geojson_path = os.path.join('data', 'malawi_districts.geojson')
    
    # Create map
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add GeoJSON layer
    folium.GeoJson(
        geojson_path,
        name='Districts',
        popup=folium.GeoJsonPopup(fields=['name', 'region', 'population']),
        tooltip=folium.GeoJsonTooltip(fields=['name', 'region'])
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    map_html = m._repr_html_()
    return render_template('map.html', map=map_html)
```

**End of Day 6:**
- [ ] Commit to GitHub: "Add GeoJSON layer to map"
- [ ] Verify districts display on map with interactive popups
- [ ] Test on live app

---

### Day 7: Data Filtering & Dynamic Regions

**Morning (2–3 hrs):**
- [ ] Understand URL parameters in Flask (`?region=Central`)
- [ ] Learn to filter data based on URL parameter
- [ ] Implement region filtering logic

**Code (`app.py` updated with filtering):**
```python
from flask import Flask, render_template, request
import folium
import json
import os
import geopandas as gpd

app = Flask(__name__)

@app.route('/map')
def map_view():
    # Get region from URL parameter (default: all regions)
    selected_region = request.args.get('region', '')
    
    # Load GeoJSON as GeoDataFrame
    geojson_path = os.path.join('data', 'malawi_districts.geojson')
    gdf = gpd.read_file(geojson_path)
    
    # Filter by region if selected
    if selected_region:
        gdf = gdf[gdf['region'] == selected_region]
    
    # Create map
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add filtered GeoJSON
    folium.GeoJson(
        gdf.to_json(),
        name='Districts',
        popup=folium.GeoJsonPopup(fields=['name', 'region', 'population']),
        tooltip=folium.GeoJsonTooltip(fields=['name']),
        style_function=lambda x: {
            'fillColor': '#FFD700' if selected_region else '#87CEEB',
            'color': 'black',
            'weight': 1,
            'opacity': 0.8
        }
    ).add_to(m)
    
    # Zoom to filtered region
    if selected_region:
        bounds = gdf.total_bounds
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    folium.LayerControl().add_to(m)
    
    map_html = m._repr_html_()
    
    # Pass regions list to template
    regions = sorted(gdf['region'].unique().tolist())
    
    return render_template(
        'map.html',
        map=map_html,
        selected_region=selected_region,
        regions=regions
    )
```

**Afternoon (2–3 hrs):**
- [ ] Update template to include region selector dropdown
- [ ] Create links to filter by region
- [ ] Test filtering locally

**Code (`templates/map.html` updated):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Malawi Districts Map</h1>

<div style="margin-bottom: 20px;">
    <label for="region-select">Filter by Region:</label>
    <select id="region-select" onchange="filterRegion()">
        <option value="">All Regions</option>
        {% for region in regions %}
            <option value="{{ region }}" {% if region == selected_region %}selected{% endif %}>
                {{ region }}
            </option>
        {% endfor %}
    </select>
</div>

<div style="height: 600px; border: 1px solid #ccc;">
    {{ map | safe }}
</div>

<script>
    function filterRegion() {
        let region = document.getElementById('region-select').value;
        window.location.href = '/map?region=' + region;
    }
</script>
{% endblock %}
```

**End of Day 7:**
- [ ] Commit to GitHub: "Add region filtering dropdown"
- [ ] Test filtering: select different regions, verify map updates
- [ ] Verify map zooms to selected region

---

### Day 8: Sidebar Statistics & Data Display

**Morning (2–3 hrs):**
- [ ] Learn CSS/HTML for sidebar layout
- [ ] Design statistics panel (region name, population, districts, etc.)
- [ ] Calculate aggregate statistics from GeoDataFrame

**Code (`app.py` updated):**
```python
@app.route('/map')
def map_view():
    selected_region = request.args.get('region', '')
    
    # Load data
    geojson_path = os.path.join('data', 'malawi_districts.geojson')
    gdf = gpd.read_file(geojson_path)
    
    # Calculate statistics
    stats = {
        'total_districts': len(gdf),
        'total_population': gdf['population'].sum(),
        'regions': sorted(gdf['region'].unique().tolist())
    }
    
    if selected_region:
        filtered_gdf = gdf[gdf['region'] == selected_region]
        stats['selected_region'] = selected_region
        stats['districts_in_region'] = len(filtered_gdf)
        stats['region_population'] = filtered_gdf['population'].sum()
        stats['avg_district_pop'] = filtered_gdf['population'].mean()
    else:
        filtered_gdf = gdf
    
    # Create map (same as before)
    m = folium.Map(...)
    # ... add GeoJSON, filters, etc.
    
    map_html = m._repr_html_()
    
    return render_template(
        'map.html',
        map=map_html,
        selected_region=selected_region,
        regions=stats['regions'],
        stats=stats
    )
```

**Afternoon (2–3 hrs):**
- [ ] Update template with sidebar layout
- [ ] Display statistics based on selected region
- [ ] Style with CSS (flexbox layout)

**Code (`templates/map.html` updated with sidebar):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Malawi Districts Map</h1>

<div style="display: flex; height: calc(100vh - 200px); gap: 20px;">
    <!-- Sidebar -->
    <div style="width: 280px; background: #f5f5f5; padding: 20px; overflow-y: auto; border-radius: 8px;">
        <h3>Filters & Info</h3>
        
        <label for="region-select"><strong>Select Region:</strong></label>
        <select id="region-select" onchange="filterRegion()" style="width: 100%; padding: 8px; margin-bottom: 20px;">
            <option value="">All Regions</option>
            {% for region in regions %}
                <option value="{{ region }}" {% if region == selected_region %}selected{% endif %}>
                    {{ region }}
                </option>
            {% endfor %}
        </select>
        
        <hr>
        
        <h4>Statistics</h4>
        {% if selected_region %}
            <p><strong>Region:</strong> {{ selected_region }}</p>
            <p><strong>Districts:</strong> {{ stats.districts_in_region }}</p>
            <p><strong>Population:</strong> {{ "{:,.0f}".format(stats.region_population) }}</p>
            <p><strong>Avg per District:</strong> {{ "{:,.0f}".format(stats.avg_district_pop) }}</p>
        {% else %}
            <p><strong>Total Districts:</strong> {{ stats.total_districts }}</p>
            <p><strong>Total Population:</strong> {{ "{:,.0f}".format(stats.total_population) }}</p>
            <p><strong>Regions:</strong> {{ stats.regions | length }}</p>
        {% endif %}
    </div>
    
    <!-- Map -->
    <div style="flex: 1; border: 1px solid #ccc; border-radius: 8px; overflow: hidden;">
        {{ map | safe }}
    </div>
</div>

<script>
    function filterRegion() {
        let region = document.getElementById('region-select').value;
        window.location.href = '/map?region=' + region;
    }
</script>

<style>
    select { font-size: 14px; }
    p { margin: 8px 0; line-height: 1.6; }
</style>
{% endblock %}
```

**End of Day 8:**
- [ ] Commit to GitHub: "Add sidebar with statistics"
- [ ] Test statistics update when region selected
- [ ] Verify layout looks clean (no overlapping elements)

---

### Day 9: Styling & User Experience

**Morning (2–3 hrs):**
- [ ] Create dedicated CSS file for styling
- [ ] Improve visual hierarchy (fonts, colors, spacing)
- [ ] Ensure mobile responsiveness (basic)

**Code (`static/css/style.css`):**
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f9f9f9;
    color: #333;
}

nav {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 15px 30px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

nav a {
    color: white;
    text-decoration: none;
    margin-right: 30px;
    font-weight: 500;
    transition: opacity 0.3s;
}

nav a:hover {
    opacity: 0.8;
}

.container {
    padding: 20px 30px;
    max-width: 1400px;
    margin: 0 auto;
}

h1 {
    color: #333;
    margin-bottom: 20px;
    font-size: 28px;
}

h3, h4 {
    color: #555;
    margin-bottom: 10px;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    background: white;
}

select:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
}

.sidebar {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stats-value {
    font-size: 18px;
    font-weight: 600;
    color: #667eea;
    margin-top: 5px;
}

/* Responsive design */
@media (max-width: 768px) {
    .map-container {
        flex-direction: column;
        height: auto;
    }
    
    .sidebar {
        width: 100% !important;
        margin-bottom: 20px;
    }
    
    nav a {
        display: block;
        margin-bottom: 10px;
    }
}
```

**Update `templates/base.html` to include CSS:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Geospatial Web Mapping{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        <a href="/">🏠 Home</a>
        <a href="/map">🗺️ Map</a>
        <a href="/about">ℹ️ About</a>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
</body>
</html>
```

**Afternoon (2–3 hrs):**
- [ ] Test app in different browsers
- [ ] Test responsiveness (mobile view)
- [ ] Adjust colors/spacing for visual polish
- [ ] Add loading indicator (optional)

**End of Day 9:**
- [ ] Commit to GitHub: "Add CSS styling + responsive design"
- [ ] Test on mobile (use browser dev tools)
- [ ] Verify all UI elements visible and functional

---

### Day 10: Documentation & Week Wrap-up

**Morning (2–3 hrs):**
- [ ] Write detailed project documentation
- [ ] Update README with new features
- [ ] Create code comments for complex functions
- [ ] Document how to use the app

**Code (update `README.md`):**
```markdown
# Geospatial Web Mapping with Flask + Folium

Interactive map application for exploring Malawi administrative boundaries.

## Features (Week 2)
- Display Malawi districts and regions on interactive map
- Filter districts by region
- View statistics (population, district count)
- Responsive sidebar layout
- Multiple basemap options

## Setup & Running

```bash
python -m venv geo_web
source geo_web/bin/activate
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## How to Use

1. **Home Page:** Overview of the application
2. **Map Page:** 
   - Select a region from dropdown to filter
   - Click on districts for more details
   - Switch basemaps using layer control
   - View statistics in sidebar

## Data
- Malawi administrative boundaries (GeoJSON)
- Population data by district
- Source: GADM, OpenStreetMap

## Project Structure
```
geo-web-mapping/
├── app.py                 # Flask application
├── requirements.txt       # Dependencies
├── data/
│   └── malawi_districts.geojson
├── templates/
│   ├── base.html
│   ├── index.html
│   └── map.html
├── static/
│   └── css/style.css
└── README.md
```

## Technologies
- **Backend:** Flask (Python)
- **Mapping:** Folium, Leaflet.js
- **Data:** GeoPandas, Pandas
- **Frontend:** HTML, CSS, Jinja2

## Next Steps
- Connect to PostGIS database
- Add spatial analysis (buffer, intersect)
- Implement data export (CSV, GeoJSON)
- Add more layers (infrastructure, water access, etc.)

## Deployment
Deployed on [Platform]: [URL]

## Author
George, NSO Malawi | [Portfolio](https://example.com)

## License
MIT License
```

**Afternoon (2–3 hrs):**
- [ ] Push final code to GitHub with descriptive commits
- [ ] Verify live app still working
- [ ] Update progress tracker
- [ ] Plan Week 3

**Final commits:**
```bash
git add .
git commit -m "Week 2 complete: GeoJSON filtering, sidebar stats, responsive styling"
git push origin main
```

**End of Day 10:**
- [ ] All code committed to GitHub
- [ ] Live app updated
- [ ] README current and detailed
- [ ] Progress documented

---

## Week 2 Checklist

- [ ] GeoJSON file obtained and validated
- [ ] GeoJSON displayed on Folium map
- [ ] Region filtering working (via URL parameter)
- [ ] GeoDataFrame filtering implemented
- [ ] Sidebar layout created
- [ ] Statistics calculated and displayed
- [ ] CSS styling file created
- [ ] Mobile responsiveness implemented
- [ ] Code documented with comments
- [ ] README updated with new features
- [ ] All changes committed to GitHub
- [ ] Live app tested and working

---

## Week 2 Summary

**Skills Gained:**
- Loading and parsing GeoJSON files
- GeoPandas for spatial data manipulation
- URL parameters in Flask
- Sidebar layout with CSS Flexbox
- Responsive web design basics
- Data aggregation and statistics

**Code Created:**
- GeoJSON layer in Folium
- Region filtering logic
- Statistics calculation
- Sidebar component
- CSS styling file

**Deliverable:**
- Interactive regional map with filtering and statistics

**GitHub Commits:**
- "Add GeoJSON layer to map"
- "Add region filtering dropdown"
- "Add sidebar with statistics"
- "Add CSS styling + responsive design"
- "Week 2 complete: Documentation update"

**Time Spent:** _____ hours

**Blockers Encountered:**
_________________________________________________________________

**Lessons Learned:**
_________________________________________________________________

**Next Week Preview:**
Week 3 will focus on advanced data filtering (time-based, attribute-based), dynamic layer creation, and preparing for database integration.

---

## Resources Used This Week

- Folium Documentation: https://python-visualization.github.io/folium/
- GeoPandas User Guide: https://geopandas.org/
- Flask URL Parameters: https://flask.palletsprojects.com/en/latest/quickstart/#variable-rules
- CSS Flexbox: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout
- GeoJSON Format: https://geojson.org/

**Questions to explore next week:**
- How do I optimize performance with very large GeoJSON files?
- How do I add custom legends to the map?
- How do I implement data export (CSV, GeoJSON) from filtered results?
