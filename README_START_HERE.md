# 90-Day Geospatial Web Mapping Roadmap - Complete Documentation Index

## 📚 All Documents (Start Here)

### 1. **MASTER_SCHEDULE_10weeks.md** ⭐ START HERE
   - Overview of all 10 weeks at a glance
   - Phase breakdown (Foundations → Intermediate → Advanced → Capstone)
   - Week-by-week activities and deliverables
   - Success metrics and timeline summary
   - **Read this first to understand the big picture**

---

### 2. **Week-by-Week Detailed Guides** (5 files)

#### WEEK 01: Flask Basics & Folium Introduction
   - **File:** `WEEK_01_Foundations_Part1.md`
   - **Days:** 1–5
   - **Focus:** Flask setup, Folium map creation, CSV data, deployment
   - **Deliverable:** Live Flask+Folium app with Malawi cities
   - **Key Skills:** Flask routing, Folium basics, Jinja2 templates, Heroku deployment

#### WEEK 02: GeoJSON & Dynamic Map Filtering
   - **File:** `WEEK_02_Foundations_Part2.md`
   - **Days:** 6–10
   - **Focus:** GeoJSON loading, region filtering, sidebar stats, CSS styling
   - **Deliverable:** Interactive regional map with statistics
   - **Key Skills:** GeoPandas, URL parameters, CSS Flexbox, responsive design

#### WEEK 03: Spatial Analysis & Choropleth Mapping
   - **File:** `WEEK_03_Intermediate_Part1.md`
   - **Days:** 11–15
   - **Focus:** Spatial operations, choropleth maps, heatmaps, marker clusters
   - **Deliverable:** 4 visualization types (choropleth, heat, cluster, districts)
   - **Key Skills:** GeoPandas spatial ops, Folium plugins, dynamic indicators

#### WEEK 04: PostGIS Integration & Spatial Queries
   - **File:** `WEEK_04_Intermediate_Part2.md`
   - **Days:** 16–20
   - **Focus:** PostgreSQL+PostGIS setup, spatial queries, database layer
   - **Deliverable:** Census Explorer with PostGIS backend
   - **Key Skills:** PostGIS, SQLAlchemy, spatial indexes, ogr2ogr import

#### WEEKS 05–10: (Coming Soon or In Progress)
   - Week 5: Advanced spatial joins, aggregations, caching
   - Week 6: Data export, API endpoints, documentation
   - Week 7: Leaflet.draw, AJAX queries, interactive tools
   - Week 8: Production deployment, monitoring, error handling
   - Week 9: Capstone project (choose one option)
   - Week 10: Portfolio finalization, freelance launch

---

### 3. **Project Templates & Code**

#### Flask + Folium Project Template
   - **File:** `flask_folium_template.md`
   - **Contents:**
     - Complete directory structure
     - `requirements.txt` with all dependencies
     - `config.py` for different environments
     - `.env.example` template
     - Minimal `app.py` example
     - Flask templates (base, map, index)
     - Utility modules for spatial operations
     - `.gitignore` and `README.md` template
   - **Use:** Copy this structure to start your first project immediately

#### 90-Day Roadmap (Original Detailed Version)
   - **File:** `90day_geospatial_webmapping_roadmap.md`
   - **Contents:** Full phase breakdown with learning resources, deliverables, and success criteria
   - **Use:** Reference for learning resources and deeper context on each phase

---

### 4. **Progress Tracking**

#### Weekly Progress Tracker
   - **File:** `progress_tracker.md`
   - **Contents:**
     - Week-by-week checklists
     - Hours logged tracking
     - Blocker/solution log
     - Skills confidence self-assessment
     - Freelance momentum tracker
     - Final 90-day checklist
   - **Use:** Print or copy to Google Docs, fill in weekly as you progress

---

## 🗂️ How to Use This Documentation

### **For Beginners (Starting Fresh)**
1. Read `MASTER_SCHEDULE_10weeks.md` (30 min)
2. Skim Week 1 daily breakdown in `WEEK_01_Foundations_Part1.md` (15 min)
3. Copy the `flask_folium_template.md` directory structure
4. Start Day 1 activities

### **For Active Development (Weeks 1–4)**
1. Read the week's document (start of week, 20 min)
2. Work through daily activities in order
3. Update `progress_tracker.md` at end of each day
4. Commit code to GitHub daily

### **For Mid-Course Check-in (Week 5+)**
1. Review `MASTER_SCHEDULE_10weeks.md` progress to date
2. Check if you're on track (15+ hrs/week)
3. Review `progress_tracker.md` for any blockers
4. Adjust pace if needed (see "If you fall behind" section in master schedule)

### **For Portfolio Building (Weeks 8–10)**
1. Refer to capstone options in master schedule (Week 9)
2. Check freelance guidelines in Week 10 section
3. Use portfolio website template suggestions

---

## 📖 Quick Reference by Topic

### **Flask**
- Week 1: Basic routing, template inheritance
- Week 4: Database connection, model definition
- Example code in `flask_folium_template.md`

### **Folium & Leaflet.js**
- Week 1: Basic map, markers, popups
- Week 2: GeoJSON, layer control
- Week 3: Choropleth, heatmaps, clusters
- Week 7: Advanced interactivity (Leaflet.draw)

### **GeoPandas & Spatial Analysis**
- Week 2: Loading GeoJSON, filtering
- Week 3: Buffer, intersect, dissolve, centroid
- Week 4–6: Database integration

### **PostGIS & Database**
- Week 4: Setup, import shapefiles, basic queries
- Week 5: Spatial joins, aggregations, caching
- Week 6: Indexes, performance optimization

### **Deployment & DevOps**
- Week 1: Heroku/Railway deployment (quick)
- Week 8: Production setup, monitoring, custom domain

### **Freelancing & Portfolio**
- Week 10: GitHub portfolio, Upwork/Fiverr gigs
- Throughout: Commit frequently, document well

---

## 🎯 Key Milestones

| Week | Code Repos | Live Apps | Freelance Progress |
|------|-----------|-----------|-------------------|
| 1 | 1 repo | 1 live app | — |
| 2 | 2 repos | 2 live apps | — |
| 3 | 3 repos | 2 live apps | — |
| 4 | 4 repos | 2 live apps | — |
| 5 | 4 repos | 3 live apps | — |
| 6 | 4 repos | 3 live apps | Demo drafts ready |
| 7 | 5 repos | 3 live apps | Portfolio drafted |
| 8 | 5 repos | 3 live apps | Portfolio live, gigs drafted |
| 9 | 6 repos | 4 live apps | Gigs live, 1st inquiry (target) |
| 10 | 6 repos | 4 live apps | 1–2 micro-projects, 2 articles |

---

## 🚀 Start Your First Week

### **Day 1 Checklist (90 minutes)**
- [ ] Create virtual environment: `python -m venv geo_web`
- [ ] Install Flask: `pip install flask folium pandas geopandas`
- [ ] Create project folder: `mkdir geo-web-mapping && cd geo-web-mapping`
- [ ] Initialize Git: `git init`
- [ ] Create `app.py` with Flask "Hello World"
- [ ] Run: `python app.py` and visit `http://localhost:5000`
- [ ] Commit: `git add . && git commit -m "Initial Flask setup"`

**You've done it.** You now have a working Flask app. The momentum is real.

---

## 🔗 Resource Links (by Week)

### **Week 1–2 Resources**
- Flask: https://flask.palletsprojects.com/
- Folium: https://python-visualization.github.io/folium/
- Jinja2: https://jinja.palletsprojects.com/
- Leaflet.js: https://leafletjs.com/

### **Week 3 Resources**
- GeoPandas: https://geopandas.org/
- Shapely: https://shapely.readthedocs.io/
- Folium Plugins: https://python-visualization.github.io/folium/plugins.html

### **Week 4–6 Resources**
- PostgreSQL: https://www.postgresql.org/docs/
- PostGIS: https://postgis.net/docs/
- SQLAlchemy: https://docs.sqlalchemy.org/
- GeoAlchemy2: https://geoalchemy-2.readthedocs.io/
- GDAL/ogr2ogr: https://gdal.org/

### **Week 7–8 Resources**
- Leaflet.draw: https://leaflet.com/plugins.html#drawing
- Production deployment (Heroku): https://devcenter.heroku.com/articles/getting-started-with-python
- Gunicorn: https://gunicorn.org/
- Error handling: https://flask.palletsprojects.com/en/latest/errorhandling/

### **Week 9–10 Resources**
- GitHub Portfolio Guide: https://docs.github.com/en/github/setting-up-and-managing-your-github-profile
- Upwork: https://www.upwork.com/
- Fiverr: https://www.fiverr.com/
- Medium/Dev.to: https://medium.com/, https://dev.to/

---

## 📝 Document Quick Links

| Document | Purpose | Best For |
|----------|---------|----------|
| `MASTER_SCHEDULE_10weeks.md` | Full roadmap overview | Planning, understanding pace |
| `WEEK_0X_*.md` (5 files) | Day-by-day details | Active development |
| `flask_folium_template.md` | Project boilerplate | Starting projects |
| `90day_geospatial_webmapping_roadmap.md` | Original roadmap | Deep context, resources |
| `progress_tracker.md` | Weekly tracking | Accountability, reflection |

---

## 💡 Pro Tips

### **Commit Frequently**
- Commit daily, even small changes
- Good commit messages: "Add choropleth map route" not "update"
- GitHub shows activity; employers see progress

### **Deploy Early**
- Get live apps running by Week 1
- Updates to live app weekly
- Shows ability to deploy (critical skill)

### **Build in Public**
- Share your progress (LinkedIn, Twitter)
- Tweet/post one milestone per week
- Helps with freelance credibility

### **Stay on Pace**
- Target: 15–20 hrs/week (2–3 hrs/day)
- If behind, compress non-essentials
- If ahead, add stretch goals (Django, React)

### **Document Everything**
- README on every repo (future you will thank you)
- Code comments for complex logic
- Blog posts as you learn (great for SEO + freelancing)

---

## ❓ FAQ

**Q: I'm not a web developer. Is this too hard?**  
A: You have a strong GIS + Python foundation. Weeks 1–2 teach web basics. By Week 4, you'll have built 3 apps. You're not starting from zero.

**Q: Can I go faster?**  
A: Yes. If you dedicate 25+ hrs/week, you can compress this to 60 days. But quality > speed. Slow and steady wins.

**Q: What if I get stuck on PostGIS?**  
A: PostGIS is hardest part (Week 4). Spend extra time here. It's also highest ROI (employers love it). Reach out in communities (Stack Overflow, PostGIS list).

**Q: How do I know when I'm ready to freelance?**  
A: By Week 6, you have a live Census Explorer + API. That's freelance-ready. Post it. First gigs come by Week 8.

**Q: Should I focus on Django instead of Flask?**  
A: No. Flask is simpler, enough for this scope. Learn Django later (Week 11+) if you want.

**Q: Can I do this while job hunting?**  
A: Yes. Your active job search (NSO, UN roles) is separate. This builds portfolio in parallel. By Week 8, you have live projects to show employers.

---

## 🎓 What You'll Know by Day 50

- [ ] Confident building Flask web apps from scratch
- [ ] Understand how to load and filter spatial data
- [ ] Can create interactive maps (Folium + Leaflet)
- [ ] Know PostGIS basics (spatial queries, indexes)
- [ ] Have deployed 3+ apps to production
- [ ] Understand full-stack development (backend + frontend)
- [ ] Ready to take on freelance projects
- [ ] Have portfolio to show employers

---

## 🤝 Community & Help

**Getting Stuck?**
- Stack Overflow: Tag `flask`, `folium`, `postgis`
- Reddit: r/gis, r/Python, r/webdev
- Discord: Python Discord, GIS/Mapping communities

**Finding Data:**
- OpenStreetMap: osmdata.openstreetmap.de
- GADM: gadm.org (administrative boundaries)
- Natural Earth: naturalearthdata.com
- World Bank Open Data: data.worldbank.org

**Inspiration:**
- GitHub: Search "folium" + "flask" → find other projects
- Observable: Observable.com (Leaflet visualizations)
- Medium: Search "geospatial web mapping"

---

## ✅ Final Checklist (Before You Start)

- [ ] Read `MASTER_SCHEDULE_10weeks.md` (30 min)
- [ ] Create GitHub account (if not already)
- [ ] Python 3.8+ installed
- [ ] Text editor/IDE ready (VS Code, PyCharm)
- [ ] Commit to 15–20 hrs/week
- [ ] First week planned on calendar
- [ ] `progress_tracker.md` ready

**You're ready. Let's go.**

---

**Questions? Blockers?**  
Refer to the specific week's document. The answer is almost certainly there.

**Good luck. You've got this.**
