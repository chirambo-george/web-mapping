# 90-Day Geospatial Web Mapping Roadmap - Master Schedule

**Timeline:** 10 weeks × ~15–20 hours/week  
**Final Goal:** Production-ready geospatial web apps + 3+ freelance gigs live

---

## PHASE BREAKDOWN

### PHASE 1: FOUNDATIONS (Weeks 1–3, Days 1–20)
Learn Flask/Folium basics, load spatial data, create dynamic maps

| Week | Focus | Deliverable |
|------|-------|-------------|
| **1** | Flask setup, Folium basics, first map | Simple Flask+Folium app with cities |
| **2** | GeoJSON, data filtering, sidebar stats | Interactive regional map with filtering |
| **3** | Spatial analysis, choropleth, heatmaps | 4 visualization types (choropleth, heat, cluster, districts) |

---

### PHASE 2: INTERMEDIATE SKILLS (Weeks 4–6, Days 21–50)
Spatial operations, database integration, performance optimization

| Week | Focus | Deliverable |
|------|-------|-------------|
| **4** | PostGIS setup, spatial queries, database layer | Census explorer querying PostGIS |
| **5** | Advanced spatial joins, aggregations, caching | Optimized app with sub-2s load times |
| **6** | Data export, API endpoints, documentation | CSV/GeoJSON export routes, API docs |

---

### PHASE 3: ADVANCED PROJECTS (Weeks 7–8, Days 51–75)
Interactivity, production deployment, performance tuning

| Week | Focus | Deliverable |
|------|-------|-------------|
| **7** | Leaflet.draw (user drawing), AJAX queries | Geospatial query tool (draw polygon → get results) |
| **8** | Production deployment, error handling, monitoring | Live app on production server with custom domain |

---

### PHASE 4: CAPSTONE + FREELANCE (Weeks 9–10, Days 76–90)
Capstone project, portfolio polish, freelance launch

| Week | Focus | Deliverable |
|------|-------|-------------|
| **9** | Capstone project (choose option) | Fully functional capstone + demo video |
| **10** | Portfolio polish, freelance launch, documentation | 3+ gigs live, portfolio website, 2 blog posts |

---

## WEEK-BY-WEEK ACTIVITY CHUNKS

### WEEK 1: Flask Basics & Folium Introduction
**Duration:** Days 1–5 (Mon–Fri)  
**Hours Target:** 15–20  
**Outcome:** Live Flask+Folium app showing Malawi cities

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 1 | Environment + Flask | Setup venv, Flask "Hello World", Git init | Working Flask app locally |
| 2 | Folium Basics | Create first Folium map, markers, popups | Map with Lilongwe marker |
| 3 | CSV Data + Markers | Load CSV, loop markers from data | 5+ Malawi cities on map |
| 4 | Layer Control + Nav | Template inheritance, multiple basemaps | Navigation menu, layer switching |
| 5 | Deploy + Documentation | Deploy to Heroku/Railway, write README | Live URL + GitHub repo |

**GitHub Commits:**
- Initial Flask setup
- Add Folium map to Flask app
- Add dynamic markers from CSV
- Add base template + layer control
- Deploy to production (live URL)

**Files Created:**
- `app.py`, `templates/base.html`, `index.html`, `map.html`
- `data/cities.csv`, `requirements.txt`, `README.md`, `.gitignore`

---

### WEEK 2: GeoJSON & Dynamic Map Filtering
**Duration:** Days 6–10 (Mon–Fri)  
**Hours Target:** 15–20  
**Outcome:** Interactive regional map with statistics sidebar

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 6 | GeoJSON Format | Load GeoJSON, validate, understand structure | Malawi districts GeoJSON loaded |
| 7 | Data Filtering | URL parameter filtering (?region=Central), GeoPandas filter | Region selector dropdown working |
| 8 | Sidebar Stats | Calculate aggregations (sum, count, mean), display stats | Sidebar showing region population, district count |
| 9 | Styling + Responsive | CSS file, flexbox layout, mobile view | Polished UI, works on mobile |
| 10 | Documentation | Update README, code comments, commit | Final docs, all code committed |

**GitHub Commits:**
- Add GeoJSON layer to map
- Add region filtering dropdown
- Add sidebar with statistics
- Add CSS styling + responsive design
- Week 2 complete: Documentation update

**Files Created:**
- `data/malawi_districts.geojson`, `static/css/style.css`
- Updated `app.py`, `templates/map.html`

---

### WEEK 3: Spatial Analysis & Choropleth Mapping
**Duration:** Days 11–15 (Mon–Fri)  
**Hours Target:** 15–20  
**Outcome:** 4 visualization types (choropleth, heatmap, clusters, districts)

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 11 | Spatial Ops | Learn buffer, intersect, dissolve, centroid | `geo_utils/spatial_ops.py` with 6+ functions |
| 12 | Choropleth Maps | Create population choropleth, legend, popups | Choropleth map route working |
| 13 | Multi-Indicator | Dropdown for population/literacy/healthcare | Dynamic indicator switching |
| 14 | Heatmaps + Clusters | Heatmap plugin, marker clustering, sample data | Heatmap and cluster map routes |
| 15 | Integration + Testing | Update homepage, test all routes, fix bugs | All visualizations working, homepage updated |

**GitHub Commits:**
- Add spatial operations utility module
- Add choropleth map route and template
- Add dynamic indicator switching for choropleth
- Add heatmap and cluster map visualizations
- Integrate all visualizations, update homepage

**Files Created:**
- `geo_utils/spatial_ops.py`, `data/sample_facilities.geojson`
- `templates/choropleth.html`, `heatmap.html`, `cluster.html`
- Updated `app.py`, `templates/index.html`

---

### WEEK 4: PostGIS Integration & Spatial Queries
**Duration:** Days 16–20 (Mon–Fri)  
**Hours Target:** 15–20  
**Outcome:** Census data explorer with PostGIS backend + live queries

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 16 | PostGIS Setup | Install PostgreSQL, PostGIS, load Malawi shapefiles | Database with tables loaded |
| 17 | SQL Spatial Queries | Write ST_DWithin, ST_Intersects, ST_Contains | Query functions working |
| 18 | Flask + PostGIS | SQLAlchemy connection, query from Flask | Flask routes querying database |
| 19 | Census Explorer | Load census EA + TA + region data, create explorer | Interactive census explorer app |
| 20 | Testing + Deployment | Performance test (<2s load), update live app | Live app using PostGIS backend |

**GitHub Commits:**
- Add PostGIS database setup script
- Add SQLAlchemy connection + spatial queries
- Add Census Explorer with PostGIS backend
- Performance optimization + caching
- Week 4 complete: Live PostGIS app deployed

**Files Created:**
- `config.py` (database config), `geo_utils/db_queries.py`
- `deployment/postgis_setup.sql` (setup script)
- Updated `app.py`, new route `/census-explorer`

---

### WEEK 5: Advanced Spatial Joins & Aggregations
**Duration:** Days 21–25 (Mon–Fri)  
**Hours Target:** 15–20  
**Outcome:** Optimized queries, spatial aggregations, caching layer

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 21 | Spatial Joins | PostGIS spatial joins (ST_WITHIN, ST_INTERSECT) | Query returns overlapping features |
| 22 | Aggregations | Calculate stats by region (sum pop, avg literacy) | Dashboard showing aggregated stats |
| 23 | Caching | Implement Flask-Caching for tile layers, results | < 2s load time with 1000+ features |
| 24 | Query Optimization | Analyze slow queries, add indexes, test performance | Query benchmarks documented |
| 25 | Load Test + Deploy | Stress test with many users, update live app | Performance report, live app optimized |

**GitHub Commits:**
- Add spatial join queries
- Implement aggregation functions + dashboard
- Add Flask-Caching layer
- Performance optimization + indexing
- Week 5 complete: Optimized production app

**Files Created:**
- Enhanced `geo_utils/db_queries.py`
- `templates/dashboard.html`
- `deployment/performance_report.md`

---

### WEEK 6: Data Export & API Development
**Duration:** Days 26–30 (Mon–Fri)  
**Hours Target:** 15–20  
**Outcome:** CSV/GeoJSON export, JSON API, full documentation

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 26 | CSV Export | Route to export filtered data as CSV | `/api/export/csv?region=North` working |
| 27 | GeoJSON Export | Route to export spatial data as GeoJSON | `/api/export/geojson` working |
| 28 | JSON API | Create RESTful endpoints for data queries | `/api/districts`, `/api/regions` endpoints |
| 29 | API Documentation | Write Swagger/OpenAPI docs, usage examples | API docs published |
| 30 | Testing + Deployment | Test export routes, update live app | All export routes live, API docs online |

**GitHub Commits:**
- Add CSV export route
- Add GeoJSON export route
- Add JSON API endpoints
- Write API documentation
- Week 6 complete: Export + API live

**Files Created:**
- `templates/api_docs.html`, `/api_docs.json` (Swagger)
- New routes in `app.py` for exports + API

---

### WEEK 7: Advanced Interactivity (Leaflet.draw & AJAX)
**Duration:** Days 31–35 (Mon–Fri)  
**Hours Target:** 18–22  
**Outcome:** Geospatial Query Tool (user draws polygon → get results)

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 31 | Leaflet.draw Setup | Install plugin, user can draw polygon/circle | Draw controls visible on map |
| 32 | AJAX Requests | Send drawn geometry to backend as GeoJSON | Frontend JavaScript AJAX working |
| 33 | Spatial Query Backend | Backend: geom_from_request → ST_Intersects → results | Query returns features inside polygon |
| 34 | Result Display | Show results as table, export options | Table with query results, export buttons |
| 35 | Polish + Deploy | UX improvements, error handling, live deployment | Query tool live, demo video recorded |

**GitHub Commits:**
- Add Leaflet.draw to map
- Implement AJAX geometry submission
- Add spatial query backend
- Display results + export options
- Week 7 complete: Query tool live

**Files Created:**
- `templates/query_tool.html`
- `static/js/draw_interactions.js`
- New route `/api/spatial-query` in `app.py`

---

### WEEK 8: Production Deployment & Monitoring
**Duration:** Days 36–40 (Mon–Fri)  
**Hours Target:** 12–15  
**Outcome:** Live production app with domain, monitoring, error handling

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 36 | Environment Setup | Production `.env`, secrets management | Heroku/Railway config vars set |
| 37 | WSGI Server | Gunicorn config, load testing | `Procfile`, `gunicorn.conf.py` created |
| 38 | Error Handling | Try/catch blocks, logging, error pages | Error logging to file, 404/500 pages |
| 39 | Custom Domain | Bind domain (optional), SSL certificate | HTTPS working, domain redirects |
| 40 | Monitoring + Docs | Setup error alerts, write deployment guide | Deployment guide complete, live monitoring |

**GitHub Commits:**
- Add WSGI server config (Gunicorn)
- Implement error handling + logging
- Setup production environment
- Add custom domain + SSL
- Week 8 complete: Production deployment guide

**Files Created:**
- `Procfile`, `gunicorn.conf.py`
- `.env.production` (template)
- `deployment/DEPLOYMENT_GUIDE.md`
- `logs/app.log`

---

### WEEK 9: Capstone Project
**Duration:** Days 41–45 (Mon–Fri)  
**Hours Target:** 20–25  
**Outcome:** Fully functional capstone + demo video + documentation

**Choose ONE:**
- **A) Spatial Analysis Dashboard:** Upload CSV (survey respondents) → clustering, density, proximity analysis
- **B) Multi-layer Thematic Map:** Combine 3+ datasets (boundaries, infrastructure, population, water)
- **C) Real-time Location Tracker:** Simulate GPS tracking → animated trace on map

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 41 | Planning + Design | Scope capstone, wireframe, tech choices | Design document + wireframes |
| 42–43 | Core Development | Build main features (2 days) | Core features working |
| 44 | Polish + Testing | UI refinement, bug fixes, testing | All features working smoothly |
| 45 | Demo + Docs | Record demo video, write technical docs | Demo video (60s), full documentation |

**GitHub Commits:**
- Capstone project scaffold + planning
- Core features implemented
- Feature complete + tested
- Demo video + documentation

**Files Created:**
- Full capstone project with all features
- `CAPSTONE_DEMO.mp4` (demo video)
- `CAPSTONE_DOCUMENTATION.md`

---

### WEEK 10: Portfolio & Freelance Launch
**Duration:** Days 46–50 (Mon–Fri)  
**Hours Target:** 12–15  
**Outcome:** 3+ gigs live, portfolio website, published articles

| Day | Topic | Activity | Deliverable |
|-----|-------|----------|-------------|
| 46 | GitHub Portfolio | Polish 4 repos, update READMEs, pin repos | Portfolio repos ready for viewing |
| 47 | Portfolio Website | Create 1-page portfolio linking to projects | Portfolio site live + custom domain |
| 48 | Professional Presence | LinkedIn update, Medium/Dev.to profile setup | Profiles updated with links |
| 49 | Freelance Gigs | Create 3 Upwork/Fiverr gigs with descriptions | Gigs live: Consultation, Custom App, Data Viz |
| 50 | Technical Posts | Publish 2 articles (Flask+Folium, PostGIS tips) | 2 articles published + cross-posted |

**GitHub Commits:**
- Polish repo documentation + screenshots
- Commit portfolio updates (no code changes)

**Files Created:**
- Portfolio website (`portfolio/index.html` or external)
- Medium/Dev.to blog posts (2)
- Freelance gig descriptions

---

## FULL 90-DAY TIMELINE AT A GLANCE

```
WEEK 1-3   | FOUNDATIONS        | 3 weeks × 18 hrs = 54 hours
-----------|-------------------|------------------------
Day 1-5    | Flask + Folium basics, first app
Day 6-10   | GeoJSON filtering, sidebar, styling
Day 11-15  | Spatial analysis, 4 visualization types

WEEK 4-6   | INTERMEDIATE       | 3 weeks × 18 hrs = 54 hours
-----------|-------------------|------------------------
Day 16-20  | PostGIS setup, Census Explorer
Day 21-25  | Spatial joins, aggregations, caching
Day 26-30  | Data export, API endpoints

WEEK 7-8   | ADVANCED           | 2 weeks × 18 hrs = 36 hours
-----------|-------------------|------------------------
Day 31-35  | Leaflet.draw, AJAX, Query tool
Day 36-40  | Production deployment, monitoring

WEEK 9-10  | CAPSTONE + LAUNCH  | 2 weeks × 18 hrs = 36 hours
-----------|-------------------|------------------------
Day 41-45  | Capstone project + demo video
Day 46-50  | Portfolio + freelance launch

TOTAL: ~180 hours over 90 days (18 hrs/week average)
```

---

## KEY DELIVERABLES BY END OF WEEK 10

✅ **4+ GitHub Repositories (polished)**
- Week 1-2 Project (Districts Map)
- Week 3 Project (4 Visualizations)
- Week 4-6 Project (Census Explorer + API)
- Capstone Project

✅ **3+ Live Production Apps**
- Week 2: Regional map (Heroku/Railway)
- Week 4: Census explorer (PostGIS backend)
- Week 9: Capstone project

✅ **Portfolio Assets**
- Portfolio website (1-pager)
- GitHub profile with pinned repos
- LinkedIn profile updated

✅ **Freelance Presence**
- 3 Upwork gigs live (Consultation, Custom App, Data Viz)
- 3 Fiverr gigs live (optional)

✅ **Published Content**
- 2 Medium/Dev.to technical articles
- API documentation online
- Deployment guide

✅ **Technical Skills**
- Confident building Flask+Folium apps independently
- PostGIS spatial queries
- Map optimization (< 2s load times)
- Full-stack development (backend + frontend)
- Production deployment

---

## Notes on Pace & Flexibility

**This timeline is ambitious but achievable with 15–20 hrs/week.**

### If you fall behind:
- Compress non-critical features (advanced caching, custom styling)
- Skip one visualization type if needed
- Focus on substance over polish in capstone

### If you get ahead:
- Learn Django (more scalable than Flask)
- Build Streamlit dashboards (rapid prototyping)
- Explore React + Mapbox GL for advanced frontend
- Take on early freelance projects

### If freelance work comes in:
- Pivot capstone to client work (real > portfolio)
- Use client projects as portfolio pieces
- Timeline becomes flexible

---

## Success Metrics (End of Day 50)

**Code Quality:**
- ✓ 3+ GitHub repos with clean commits
- ✓ Documented code + READMEs
- ✓ Tests passing (basic coverage)

**Functionality:**
- ✓ 3+ live production apps
- ✓ Map loads < 2s with 1000+ features
- ✓ Export routes working (CSV, GeoJSON)
- ✓ API documented + tested

**Portfolio:**
- ✓ Portfolio website published
- ✓ Repos pinned on GitHub
- ✓ 2+ blog posts published

**Freelance:**
- ✓ 3+ gigs live on Upwork/Fiverr
- ✓ Profile complete with samples
- ✓ First inquiry received (target)

**Skills:**
- ✓ Confident with Flask + Folium
- ✓ Understand PostGIS basics
- ✓ Can optimize map performance
- ✓ Ready for full-stack projects

---

## Next Steps After 90 Days

**Option 1: Go Deeper (Web Development)**
- Learn Django for larger projects
- Frontend framework (React + Mapbox GL)
- Advanced database design

**Option 2: Expand Domain (GIS)**
- Cloud GIS platforms (GCP, AWS GIS)
- Drone imagery + ortho mosaics
- Real-time spatial data (sensors, GPS)

**Option 3: Monetize (Freelancing)**
- Scale freelance offerings
- Build SaaS product (map-based service)
- Consulting (design GIS systems for clients)

**Option 4: Institutional (Employment)**
- Resume/LinkedIn ready for GIS developer roles
- Portfolio demonstrates full-stack capability
- Target: NGOs, tech companies, gov agencies

---

**You've got this. Let's build something.**
