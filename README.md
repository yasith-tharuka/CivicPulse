# CivicPulse

#### Video Demo: [https://youtu.be/OSHGc8cnW6U](https://youtu.be/OSHGc8cnW6U)  
#### Developer: Yasith Tharuka  
#### Email: tharukayasith8@gmail.com  

---

## Description

CivicPulse is a web-based infrastructure reporting tool designed to solve a problem I witness daily in rapidly developing cities: the communication disconnect between citizens and local government authorities. In many urban areas, critical infrastructure failures-such as broken streetlamps, burst water pipes, uncollected trash, or potholes-often go unnoticed for days or weeks. This isn't because the authorities don't care, but because the reporting mechanisms are often archaic, opaque, or non-existent.

I built CivicPulse to bridge this gap. It serves as a centralized platform where citizens can report hazards in real-time, categorizing them by severity and type. Simultaneously, it provides local officials with a streamlined dashboard where they can track, prioritize, and resolve these issues based on their assigned district. By turning decentralized citizen observations into actionable engineering data, CivicPulse aims to improve urban safety and response times.

The application is built using **Python (Flask)** for the backend, **SQLite** for database management, and **Bootstrap 5** for a responsive frontend, customized with a unique *Civic Orange* brand identity. It features secure user authentication, role-based access control (RBAC), and district-specific content filtering.

---

## Project Structure

The project is organized into a modular structure to separate concerns between the backend logic, database, and frontend presentation.

### 1. `app.py` (The Controller)
This is the core entry point of the application. It initializes the Flask app, configures session management, and defines all the routes (URLs) that users visit. It handles three main responsibilities:

- **Authentication & Security:** Manages user sessions using `flask_session`. A custom `@login_required` decorator ensures sensitive routes (like the dashboard or reporting forms) are protected from anonymous access.  
- **Role-Based Logic:** Route functions check the `session["role"]` variable to determine if the current user is a *Citizen* or an *Official*. For example, `/resolve` and `/delete` routes forbid non-official users from modifying data, returning a `403 Unauthorized` error if attempted.  
- **Data Processing:** Handles POST requests from forms, validates input (like ensuring passwords match or required fields are filled), and executes SQL queries via the CS50 Library.  

---

### 2. `civicpulse.db` & `data.sql` (The Model)
The application relies on a SQLite database. The schema includes two primary tables:

- **users:** Stores authentication details. Includes a `district` column (to map users to specific geographic areas) and a `role` column (to distinguish between Citizens and Officials). Passwords are stored as secure hashes using `werkzeug.security`.  
- **incidents:** Stores reports. Each report links to the citizen who filed it via a Foreign Key (`user_id`). Tracks status (Open/Resolved), severity (Low/Medium/Critical), and category (Power, Water, etc.).  

---

### 3. `templates/` (The View)
Dynamic HTML pages built with Jinja2 templating:

- **layout.html:** Skeleton of the site. Contains the navigation bar (changes based on login status), footer, and Flash messaging block for user feedback.  
- **dashboard.html:** Displays incidents. Uses Jinja logic (`{% if session["role"] == 'official' %}`) to conditionally render administrative buttons. Officials see *Mark Resolved* and *Delete*; citizens only see status badges.  
- **report.html:** Intake form using Bootstrap controls to capture Title, Category, Severity, and Description.  
- **register.html:** Registration form with a dropdown for Sri Lankan districts. Hardcoded list ensures consistency and prevents typos like *Colmbo* instead of *Colombo*.  

---

### 4. `static/styles.css`
Custom CSS overrides Bootstrap defaults. Defines a unique brand identity with `--civic-orange (#E47D32)`, resembling construction/safety colors to suit the public infrastructure theme.

---

## Design Choices

During development, I faced several architectural decisions where I had to weigh complexity against functionality.

### 1. Role-Based Access Control (RBAC) vs. Separate Apps
- **Debate:** Whether to create a separate admin portal for officials.  
- **Decision:** Unified application with a `role` column in the users table. This reduced code duplication and simplified deployment.  

### 2. District Filtering Logic
- **Initial Idea:** Allow officials to see all reports nationwide.  
- **Decision:** Implement strict district filtering. Officials only see incidents from their district.  
- **Impact:** Keeps dashboards manageable and practical for real-world government use.  

### 3. Severity System
- **Problem:** Title and Description alone were insufficient for triage.  
- **Decision:** Added a Severity dropdown (Low, Medium, Critical).  
- **Impact:** Color-coded badges (Red = Critical, Yellow = Medium) allow officials to visually prioritize urgent hazards.  

### 4. Soft vs. Hard Deletion
- **Debate:** Soft deletion (hidden in DB) vs. hard deletion (row removal).  
- **Decision:** Hard deletion for simplicity and database efficiency.  
- **Safety:** Added JavaScript confirmation popups to prevent accidental data loss.  

---

## How to Run

### Install Dependencies
```bash
pip install -r requirements.txt

---

## Default Official Account

For demonstration purposes, an **official user account** has been preconfigured. Since officials cannot be registered directly through the web interface, this account must be created manually using the SQLite terminal.

- **Username:** `admin`  
- **Password:** `2345`  

### How to Create the Official Account
Open the SQLite shell and insert the record into the `users` table:

```sql
INSERT INTO users (username, hash, role, district)
VALUES ('admin', '<hashed_password>', 'official', 'Colombo');
