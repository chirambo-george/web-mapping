# 90-Day Geospatial Web Mapping Roadmap
## Folium + Flask/Django Stack | Portfolio + Freelance Ready

**Target:** Build production-grade geospatial web applications using Python backend, Folium maps, and Flask/Django. Ship 2–3 portfolio projects + 1–2 freelance micro-deliverables.

---

## PHASE 1: FOUNDATIONS (Days 1–20)
### Goal: Core web mapping concepts + minimal viable tech stack

#### Week 1–2: Web Dev + Folium Basics
**Topics:**
- Flask fundamentals (routing, templates, static files)
- Folium basics (map creation, markers, popups, layers)
- GeoJSON + spatial data in web context
- HTML/Jinja2 templating (you know HTML, focus on template logic)

**Deliverables:**
1. **Simple Flask app** serving a single Folium map (hardcoded GeoJSON)
   - Route: `/` → renders map.html with a Leaflet-based Folium map
   - Include 3–5 markers with popups
   - Deploy locally + document setup steps
   
2. **Learning artifact:** Markdown doc on "Folium for GIS Professionals"
   - Compare Folium vs ArcGIS JS, Mapbox, Leaflet
   - Code snippets: basic map, marker clusters, choropleth
   - Store on GitHub (public repo)

**Resources:**
- Folium official docs: https://python-visualization.github.io/folium/
- Flask mega-tutorial (Miguel Grinberg) — read chapters 1–3
- Real Python: "Building Web Applications with Flask"

**Time estimate:** 15–20 hours

---

#### Week 3: Dynamic Data + Backend Logic
**Topics:**
- Reading spatial data files (GeoJSON, Shapefile, GeoPackage) in Python
- Pandas + GeoPandas for spatial data wrangling
- Connecting Flask routes to data pipelines
- Serving dynamic maps based on URL parameters

**Deliverables:**
1. **Flask app with data pipeline**
   - Load a shapefile or GeoJSON from disk
   - Route: `/map/<region>` → filters data + serves thematic map
   - Example: Malawi EA boundaries → select by region
   - Include layer control (toggle admin levels)

2. **Code repo structure:**
   - `app.py` (Flask app)
   - `data/` (shapefiles, GeoJSON)
   - `templates/` (map.html, base.html)
   - `static/` (CSS, JS)
   - `README.md` with setup + example queries

**Resources:**
- GeoPandas documentation: https://geopandas.org/
- Flask blueprints (optional, but clean for larger apps)
- Folium + GeoPandas integration examples

**Time estimate:** 15–18 hours

---

## PHASE 2: INTERMEDIATE SKILLS (Days 21–50)
### Goal: Spatial analysis in backend + interactive frontend

#### Week 4–5: Spatial Analysis + Thematic Mapping
**Topics:**
- Spatial joins, buffers, intersections in GeoPandas
- Choropleth maps (color by attribute)
- Heatmaps + cluster maps in Folium
- User filtering + aggregation

**Deliverables:**
1. **Project: Census Data Explorer**
   - Load Malawi census EA + TA + region boundaries
   - Backend: GeoPandas spatial joins + aggregation
   - Frontend: 
     - Map with choropleth (color by population density, literacy, etc.)
     - Dropdown: select indicator
     - Sidebar: summary statistics for selected area
   - Route: `/census/<region>?indicator=population_density`
   - Interactive popup: click polygon → show detailed stats

2. **Code structure:**
   - `app.py` with routes for data filtering
   - `geo_utils.py` (spatial functions: buffer, intersect, aggregate)
   - GeoJSON served dynamically from backend
   - Folium choropleth + layer toggle

**Resources:**
- GeoPandas spatial operations: https://geopandas.org/docs/user_guide/geometric_operations.html
- Folium choropleth example
- Plotly + Folium integration (optional, for advanced visuals)

**Time estimate:** 20–25 hours

---

#### Week 6: Database + Scalability
**Topics:**
- PostGIS basics (you may have touched this; deepen it)
- SQLAlchemy ORM (not required, but good to know)
- Serving large datasets efficiently
- Caching strategies (Flask-Caching)

**Deliverables:**
1. **PostGIS setup (local or cloud)**
   - Load Malawi shapefiles → PostGIS database
   - Query from Flask using sqlalchemy-gis or PostGIS raw SQL
   - Test performance: 1000+ features map load time < 2s

2. **Enhanced Census Explorer**
   - Backend now reads from PostGIS instead of files
   - Add spatial query: `SELECT * FROM admin_boundaries WHERE ST_DWithin(geom, point, 10000)`
   - Cache tile layers for faster loads

3. **Documentation:**
   - PostGIS setup script
   - Query optimization notes
   - Load time benchmarks (before/after caching)

**Resources:**
- PostGIS documentation: https://postgis.net/
- SQLAlchemy + GeoAlchemy2
- Flask-Caching tutorial

**Time estimate:** 15–18 hours

---

## PHASE 3: ADVANCED PROJECTS (Days 51–75)
### Goal: Production-ready applications + specialized use cases

#### Week 7: Advanced Interactivity + Frontend
**Topics:**
- Leaflet.js plugins (draw tools, measure, locate)
- Asynchronous data loading (AJAX)
- Custom basemaps + tile servers
- User input validation + spatial queries

**Deliverables:**
1. **Project: Geospatial Query Tool**
   - User draws polygon on map (Leaflet-draw)
   - Backend: Spatial intersection query
   - Returns: all features within polygon (CSV download)
   - Example use: "Select all EAs within district X" → download EA codes

2. **Features:**
   - Leaflet.draw for polygon/circle drawing
   - AJAX POST to Flask backend with GeoJSON geometry
   - GeoPandas intersection in backend
   - CSV + GeoJSON export routes
   - Progress spinner (UX polish)

**Resources:**
- Leaflet.draw: https://leaflet.com/plugins.html
- Fetch API + async/await (JavaScript)
- Flask JSON responses + file downloads

**Time estimate:** 18–22 hours

---

#### Week 8: Production Deployment + Polish
**Topics:**
- Environment variables + secrets management
- Deployment (Heroku, Railway, DigitalOcean, or PythonAnywhere)
- Error handling + logging
- Performance profiling

**Deliverables:**
1. **Deploy one application to production**
   - Choose: Census Explorer OR Geospatial Query Tool
   - Live URL (shareable)
   - SSL certificate (free with Let's Encrypt or cloud provider)

2. **Production checklist:**
   - Gunicorn/Waitress WSGI server
   - Environment config (.env file, not in git)
   - Error logging (log to file or service)
   - Load test: verify map loads < 3s with 1000+ features
   - Custom domain (optional, but polish)

3. **Documentation:**
   - Deployment guide (reproducible)
   - API documentation (if applicable)
   - Known limitations + future improvements

**Resources:**
- Flask deployment guide: https://flask.palletsprojects.com/deploying/
- Heroku + Railway tutorials (free tier available)
- Gunicorn + Nginx setup

**Time estimate:** 12–15 hours

---

## PHASE 4: CAPSTONE + FREELANCE READINESS (Days 76–90)
### Goal: Polished portfolio + market-ready freelance offerings

#### Week 9: Capstone Project
**Choose ONE (or adapt existing project):**

**Option A: Spatial Analysis Dashboard**
- Input: User uploads CSV with lat/lon (e.g., survey respondent locations)
- Backend: Clustering, density mapping, proximity analysis
- Output: Interactive map + summary report
- Real-world use: NGOs, researchers needing quick spatial visualization

**Option B: Multi-layer Thematic Map**
- Combine 3+ datasets (admin boundaries, infrastructure, population, water access)
- Layer toggle + legend
- Search/filter by attribute (e.g., "Show all schools in region X")
- Popup: detailed info card with photos (optional)

**Option C: Real-time Location Tracker**
- Simulate GPS tracking data (or use real data if available)
- Backend: Store points in PostGIS, update at intervals
- Frontend: Animated trace on map, speed/distance stats
- Example: Monitor field teams or drone missions

**Deliverables (Capstone):**
1. Fully functional web app (code on GitHub)
2. Live deployed version (URL)
3. **Marketing materials** (for freelancing):
   - 60-second demo video (screen recording)
   - Feature list & use cases
   - Technical documentation (for buyers)
4. Pricing model (if freelancing)

**Time estimate:** 20–25 hours

---

#### Week 10: Portfolio Finalization + Freelance Launch
**Tasks:**

1. **GitHub portfolio**
   - 3–4 polished repos
   - Each with: README, setup instructions, screenshot/GIF
   - Include: censusExplorer, geospatialQuery, capstone
   - Pinned repos on profile

2. **Professional presence**
   - Portfolio website (1-page): link to projects + brief bio
   - LinkedIn: highlight geospatial + web development skills
   - Medium/Dev.to: publish 2 technical posts (e.g., "Building Spatial Web Apps with Python")

3. **Freelance offerings (Upwork/Fiverr)**
   - Gig #1: "Geospatial Web Mapping Consultation"
     - Advise clients on tech stack, design map UX
     - \$50–100/hr (USD equivalent in Malawi pricing)
   - Gig #2: "Build Custom Folium + Flask Map Application"
     - Tiered: simple ($300), medium ($800), complex ($1500+)
     - Clearly specify: features, deployment, documentation
   - Gig #3: "Spatial Data Analysis + Web Visualization"
     - Load CSV/shapefile → dashboard
     - $200–500 depending on complexity

4. **Polish existing projects**
   - Add dark mode toggle
   - Mobile responsiveness audit
   - Accessibility check (WCAG basics)

**Time estimate:** 12–15 hours

---

## TIMELINE SUMMARY

| Phase | Weeks | Focus | Output |
|-------|-------|-------|--------|
| **1: Foundations** | 1–3 | Flask + Folium basics | Simple map app + learning doc |
| **2: Intermediate** | 4–6 | Spatial analysis + DB | Census explorer with PostGIS |
| **3: Advanced** | 7–8 | Interactivity + deployment | Live production app |
| **4: Capstone** | 9–10 | Polish + freelance | Capstone project + portfolio + gigs live |

---

## RESOURCE STACK (Prioritized)

### Free/Essential
- **Folium:** https://python-visualization.github.io/folium/ (official docs)
- **Flask:** https://flask.palletsprojects.com/ (official docs)
- **GeoPandas:** https://geopandas.org/ (official docs)
- **PostGIS:** https://postgis.net/ + local PostgreSQL (free, open-source)
- **GitHub:** Free public repos (portfolio)
- **Heroku/Railway:** Free tier (deploy early)

### Paid (Optional, High ROI)
- **Real Python courses** ($499/yr, but huge catalog)
  - "Building Web Applications with Flask" (~4 hrs)
  - "Working with Geospatial Data" (~3 hrs)
- **Udemy** ($10–15 courses, sales frequent)
  - "Flask by Example" (Jose Salvatierra)
  - "GIS with Python: GeoPandas" (search for structured courses)

### Recommended Blogs/Tutorials
- Miguel Grinberg (Flask mega-tutorial): https://blog.miguelgrinberg.com/
- Towards Data Science (Folium + Leaflet articles)
- Real Python (GeoPandas + PostGIS posts)

---

## Measurable Success Criteria (End of 90 Days)

✅ **Build-wise:**
- [ ] 3+ GitHub repos with polished code + documentation
- [ ] 1 live, production-deployed web map app
- [ ] Capstone project with demo video

✅ **Skill-wise:**
- [ ] Confident building Flask + Folium apps independently
- [ ] Understand PostGIS basics (spatial queries, indexing)
- [ ] Can optimize map load times (< 3s with 1000+ features)
- [ ] Familiar with Leaflet.js plugin ecosystem

✅ **Freelance-wise:**
- [ ] 3+ gigs live on Upwork/Fiverr with geo-mapping offerings
- [ ] Portfolio website live
- [ ] 2+ technical posts published
- [ ] First micro-client project in pipeline

---

## Weekly Cadence & Study Approach

### Suggested Weekly Structure (15–20 hrs/week)
- **Mon–Wed:** Focused learning + coding (6–7 hrs/day)
- **Thu:** Build mini-project or feature (4–5 hrs)
- **Fri:** Documentation + GitHub push (2–3 hrs)
- **Sat–Sun:** Optional: freelance prospecting, portfolio updates, or rest

### Learning Strategy
1. **Read docs → code along → build own version**
   - Don't just watch videos; hands-on is critical
2. **Git commit early, often**
   - Track progress, make rollback safe
3. **Prototype → refactor → deploy**
   - Get to "working" fast, then optimize
4. **Publish as you build**
   - GitHub repos don't need to be perfect; "works" is enough to build credibility

---

## Potential Pivots & Variations

### If you get ahead of schedule:
- Learn Django (more scalable than Flask for larger apps)
- Explore Streamlit for rapid geospatial dashboards (lower barrier)
- Build a tile server (Mapnik + Tippecanoe) for custom basemaps
- Learn React + Mapbox GL for frontend-heavy projects

### If you get stuck:
- Extend Phase 2 projects; depth > breadth
- Focus on PostGIS optimization (high ROI for freelancing)
- Ship micro-gigs on Fiverr early to build confidence + reviews

### If freelance momentum picks up:
- May compress capstone or pivot to client work
- That's fine — real projects beat portfolio projects
- Use client work to iterate portfolio

---

## Notes for Your Context

**You already have:**
- GIS domain knowledge (huge advantage over web devs)
- Python + R fundamentals
- Census/survey data experience (ready-made portfolio projects)
- Remote work + freelancing ambition

**Leverage:**
- Your NSO experience (census data is relatable to NGOs, researchers, governments)
- Malawi geography (build examples using local data → market credibility)
- Drone + spatial interest (later: integrate drone imagery/tile workflows)

**Timeline Reality:**
- 90 days is tight but achievable with 15–20 hrs/week
- Focus Phase 1–2 heavily; Phase 3–4 builds on that
- If job offers come in, adapt timeline (capstone can be freelance work)

---

## Next Steps (This Week)

1. **Set up environment:**
   ```bash
   python -m venv geo_web
   source geo_web/bin/activate
   pip install flask folium geopandas pandas
   ```

2. **Git repo structure:**
   - Create GitHub repo: `geo-web-mapping`
   - Initialize with README (roadmap link + progress tracker)

3. **First deliverable (days 1–3):**
   - Create simple Flask app with one hardcoded Folium map
   - Push to GitHub
   - Deploy to Heroku (free tier) or PythonAnywhere
   - Share live URL in your portfolio notes

4. **Day 4–5:**
   - Read Folium docs (1 hr)
   - Read Flask quickstart (1 hr)
   - Build second iteration: load GeoJSON from file, add popups

Good luck. Let's build something.
