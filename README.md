# CivicPulse

**Video Demo:** https://youtu.be/OSHGc8cnW6U

**Developer:** Yasith Tharuka  
**Email:** tharukayasith8@gmail.com  
**Location:** Pitabeddara, Sri Lanka

## Description

CivicPulse is a web application that bridges the communication gap between citizens and local authorities. It addresses the problem of infrastructure failures—broken streetlamps, pipe leaks, uncollected trash—going unnoticed due to difficult reporting processes.

The platform enables citizens to report hazards in real-time while giving officials a centralized, district-filtered view to track and resolve issues efficiently.

## Project Structure

Built with Python (Flask), SQLite, and Bootstrap 5:

- **app.py** — Core server logic handling authentication, role-based access control (Citizen/Official), session management, and form data processing
- **civicpulse.db & data.sql** — SQLite database with `users` and `incidents` tables, linked via Foreign Key; passwords stored as secure hashes
- **templates/** — Dynamic HTML pages using Jinja2 templating
    - `layout.html` — Navigation bar and footer skeleton with Flash messaging
    - `dashboard.html` — Displays incident cards with conditional "Mark Resolved" and "Delete" buttons based on user role and district filtering
    - `report.html` — Form for categorizing issues and setting severity levels
    - `register.html` — Registration form with Sri Lankan district dropdown
- **static/styles.css** — Custom CSS overriding Bootstrap defaults with "Civic Orange" theme (#E47D32)

## Key Design Decisions

- **Single Unified App:** Integrated citizen and official portals with role-based access instead of separate applications
- **Severity Triage System:** Low/Medium/Critical levels with color-coded badges for prioritization
- **Hard Deletion with Confirmation:** Spam removal balanced with JavaScript confirmation popups to prevent accidents

