# 🚨 Live LIGO Gravitational Wave Events

A real-time front-end display for active gravitational wave candidates detected by LIGO, using Supabase as a backend
and live data from LIGO GraceDB.

## Features

- Real-time data from LIGO's GraceDB API
- Supabase-powered event storage and sorting
- Skymap images pulled automatically for each event (when available)
- Sortable by detection time or FAR (False Alarm Rate)
- Glossary and educational resources included

## Tech Stack

- Python
- HTML + Vanilla JS
- Supabase (PostgreSQL, REST API)
- GraceDB public API

---

## Getting Started

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/ligo-live.git
cd ligo-live
```

2. **Set Supabase Environment Variables**

Create a .env file in the root of your project with the following:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
```

⚠️ Never commit your .env file. Add it to .gitignore:

```bash
echo .env >> .gitignore
```

3. **Run Locally**

If you’re using PyCharm, VSCode, or another IDE, launch a static server — or from terminal:

```bash
# Using Python 3
python3 -m http.server
# OR with Node.js
npx serve .
```

Then open your browser to:

```bash
http://localhost:8000
```

📄 Supabase Table Schema

This project expects a table named ligo_gravity_waves - DDL is:

```bash
/Supabase/DDL/ddl_ligo_gravity_waves.sql
```
