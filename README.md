# IntelliStock — AI-Powered Inventory & Demand Forecasting Platform

An intelligent inventory management and demand forecasting web application built with **Python, Django, Pandas, JavaScript, Bootstrap, and SQL**. IntelliStock helps businesses manage products, track sales, monitor inventory levels, and estimate future demand using historical sales data.

The project demonstrates how a traditional inventory management system can be enhanced with data analysis, forecasting, and an optional AI-powered assistant.

> **Project status:** Development project  
> **Primary goal:** Demonstrate full-stack development, database management, data analysis, and demand forecasting in a single application.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Problem Statement](#2-problem-statement)
3. [Project Objectives](#3-project-objectives)
4. [Key Features](#4-key-features)
5. [Technology Stack](#5-technology-stack)
6. [System Architecture](#6-system-architecture)
7. [Application Workflow](#7-application-workflow)
8. [Demand Forecasting and Data Analysis](#8-demand-forecasting-and-data-analysis)
9. [Database Design](#9-database-design)
10. [Project Structure](#10-project-structure)
11. [Prerequisites](#11-prerequisites)
12. [Installation and Setup](#12-installation-and-setup)
13. [Environment Variables](#13-environment-variables)
14. [Database Migrations](#14-database-migrations)
15. [Running the Application](#15-running-the-application)
16. [Application Modules](#16-application-modules)
17. [Testing and Quality Checks](#17-testing-and-quality-checks)
18. [API and Health Check](#18-api-and-health-check)
19. [Deployment](#19-deployment)
20. [Security Considerations](#20-security-considerations)
21. [Limitations and Future Enhancements](#21-limitations-and-future-enhancements)
22. [Learning Outcomes](#22-learning-outcomes)
23. [Author](#23-author)

---

## 1. Overview

IntelliStock is a web-based inventory management and demand forecasting platform designed to help businesses make more informed inventory decisions.

Traditional inventory systems primarily record product quantities and sales transactions. IntelliStock extends this workflow by organizing inventory data, analyzing historical sales, estimating future demand, and presenting actionable information through a web interface.

The application combines:

- **Full-stack web development:** Django backend with HTML, CSS, JavaScript, and Bootstrap.
- **Database management:** Structured storage for products and sales records.
- **Data analysis:** Processing historical sales data using Python and Pandas.
- **Demand forecasting:** Estimating future demand from available historical information.
- **AI integration:** An optional AI assistant, depending on API configuration.

The project is intended for learning, demonstration, and further development. Forecasts are estimates, not guaranteed predictions.

## 2. Problem Statement

Businesses can experience several inventory management challenges:

- Overstocking products that do not sell quickly.
- Running out of products that customers frequently purchase.
- Maintaining product and sales information across disconnected records.
- Making purchasing decisions without analyzing historical demand.
- Spending time manually reviewing sales data.

These problems can lead to wasted resources, missed sales opportunities, and inefficient inventory planning.

IntelliStock aims to provide a centralized application where inventory information and sales data can be reviewed together, with demand estimates supporting better planning.

## 3. Project Objectives

The primary objectives are to:

1. Build a functional inventory management web application.
2. Store and manage product and sales information in a database.
3. Present inventory information through a dashboard.
4. Process historical sales data for analysis.
5. Estimate future product demand using forecasting logic.
6. Provide an optional AI assistant for natural-language interactions.
7. Demonstrate a maintainable Django application structure.
8. Support local development, automated tests, and deployment configuration.

## 4. Key Features

### 4.1 Inventory Dashboard

The dashboard provides a centralized view of inventory-related information.

Depending on the available data and implementation, it can present:

- Product and inventory summaries.
- Sales-related information.
- Demand forecasting results.
- Inventory indicators and trends.
- Navigation to other application modules.

### 4.2 Product Management

The product module provides an interface for viewing and managing product records supported by the application.

Typical inventory workflows include:

- Reviewing product information.
- Maintaining product records.
- Checking current inventory quantities.
- Identifying products that may require replenishment.

The exact operations available depend on the configured views and model fields.

### 4.3 Demand Forecasting

The forecasting module processes historical sales information to estimate future demand.

Forecasts can help users identify potential demand changes and make more informed inventory decisions. Accuracy depends on data quality, historical coverage, seasonality, and the forecasting method used.

### 4.4 Sales Data Processing

The application includes a sample sales CSV file for demonstrating data-driven functionality.

Pandas can be used to load and transform records, prepare dates, aggregate sales, and generate data suitable for analysis.

### 4.5 AI Assistant

The assistant module is designed to provide an AI-based interaction layer.

If the optional Groq integration is configured correctly, it can connect the application to a supported language model. This requires a valid API key, a supported model identifier, and internet access.

Without the required API configuration, AI-powered functionality may be unavailable. Core application pages that do not depend on the external model can still be used.

### 4.6 Responsive User Interface

The frontend uses standard web technologies and Bootstrap-based styling to provide a consistent interface across common desktop and mobile screen sizes.

### 4.7 Django Administration

Django's administrative interface can be used to manage registered models and inspect application records.

Create a superuser to access the admin panel, provided the relevant models are registered.

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Django | Backend framework, routing, views, and ORM |
| SQL database | Persistent storage of application records |
| Pandas | Data cleaning, aggregation, and analysis |
| HTML5 | Page structure |
| CSS3 | Styling and layout |
| JavaScript | Client-side interactions |
| Bootstrap | Responsive UI components |
| Groq API | Optional external language-model integration |
| Git and GitHub | Version control and source-code hosting |
| Gunicorn | Production WSGI server where configured |
| Render | Potential hosting platform using deployment configuration |

**Database note:** The local setup may use SQLite, depending on the project settings. A production database such as PostgreSQL should be configured explicitly if required by the deployment environment.

---

## 6. System Architecture

IntelliStock follows a Django-based web application architecture.

```text
                 User / Browser
                       |
                       v
             HTML + CSS + JavaScript
                       |
                       v
                 Django URLs
                       |
                       v
               Django Views
                       |
            +----------+----------+
            |          |          |
            v          v          v
        Models     Services    AI Client
            |          |          |
            v          v          v
        SQL DB     Pandas     External API
            |          |
            +-----+----+
                  |
                  v
          Processed Results
                  |
                  v
            Django Templates
                  |
                  v
             User Interface
```

### Architecture Components

**Frontend:** Displays pages and sends user requests to the backend.

**URL routing:** Maps incoming paths to the corresponding Django views.

**Views:** Handle requests, coordinate application logic, and return responses.

**Models:** Define structured database records and interact with the database through Django's ORM.

**Services:** Keep reusable business logic and data-processing operations separate from presentation code.

**Database:** Stores persistent application data.

**AI integration:** Communicates with an external model when the feature is configured and available.

**Templates and static files:** Generate HTML pages and provide CSS and JavaScript assets.

---

## 7. Application Workflow

A typical application request follows this sequence:

1. A user opens a page in the browser.
2. Django receives the HTTP request.
3. The URL configuration selects the corresponding view.
4. The view validates inputs and retrieves the required records.
5. The model layer queries the database where needed.
6. The service layer processes the data when analysis or forecasting is required.
7. The view prepares the result and renders a template.
8. Django returns the HTTP response to the browser.
9. The frontend displays the result to the user.

For demand forecasting, the workflow additionally involves loading sales history, preparing time-series data, applying the implemented forecasting logic, and displaying the resulting estimates.

---

## 8. Demand Forecasting and Data Analysis

### 8.1 Why Forecasting Is Useful

Forecasting estimates future demand based on available historical observations.

For example, if a shop has recorded sales for a particular product over several weeks, it can analyze those records to estimate how much demand it might experience in a future period.

This helps support inventory planning, but it does not guarantee that future demand will match the estimate.

### 8.2 Data Preparation

A typical forecasting pipeline includes:

1. Load historical sales records.
2. Validate the required columns and values.
3. Parse dates into a consistent format.
4. Handle missing or invalid records.
5. Aggregate sales by product and time period.
6. Apply the forecasting method implemented in the project.
7. Return the forecast in a format the dashboard can display.

### 8.3 Example Sales Data

A simple dataset may contain the following columns:

| Date | Product | Quantity Sold |
|---|---|---:|
| 2026-01-01 | Product A | 12 |
| 2026-01-02 | Product A | 15 |
| 2026-01-03 | Product A | 10 |
| 2026-01-04 | Product A | 18 |

These are illustrative example records, not reported business results.

### 8.4 Example Analysis

The average daily demand over a period can be calculated as:

\[
\text{Average Demand} =
\frac{\text{Total Units Sold}}{\text{Number of Days}}
\]

If 300 units were sold across 30 days:

\[
\text{Average Demand} = \frac{300}{30}=10
\]

The average is a useful baseline. A more sophisticated forecasting method may also account for trends, seasonality, or other variables when enough appropriate data is available.

### 8.5 Important Forecasting Limitations

- Sparse or inaccurate data can reduce reliability.
- Sudden promotions and market changes may not be reflected in historical records.
- Forecasting methods should be evaluated against actual historical outcomes.
- Sample datasets are for demonstration and do not represent a real business.
- Forecasting output should support, not replace, business judgment.

**Implementation note:** Document the exact forecasting algorithm, forecast horizon, evaluation metrics, and fallback behavior after verifying the current code. Do not claim machine learning accuracy or production-grade predictive performance without measured evidence.

---

## 9. Database Design

Django models define the structure of the application's persistent data.

The inventory application includes a migration at `inventory/migrations/0001_initial.py`, which establishes the initial schema.

The main entities and relationships should be documented according to the current model definitions.

A conceptual relationship may look like this:

```text
Product
   |
   | associated with
   v
Sales Records
   |
   v
Historical Demand
   |
   v
Forecast Results
```

### Database Responsibilities

- Store product information.
- Maintain relevant sales records.
- Support filtering and retrieval through Django's ORM.
- Preserve schema changes through database migrations.
- Provide the data used by analysis and forecasting logic.

To inspect the actual database fields and relationships, review `inventory/models.py`.

---

## 10. Project Structure

```text
intellistock/
|
|-- manage.py
|-- requirements.txt
|-- pytest.ini
|-- Dockerfile
|-- render.yaml
|-- .gitignore
|-- .env.example
|
|-- intellistock/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   |-- wsgi.py
|
|-- inventory/
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- services.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |
|   |-- migrations/
|   |   |-- __init__.py
|   |   |-- 0001_initial.py
|   |
|   |-- templates/
|   |   |-- inventory/
|   |       |-- base.html
|   |       |-- dashboard.html
|   |       |-- products.html
|   |       |-- forecast.html
|   |       |-- assistant.html
|   |
|   |-- static/
|       |-- inventory/
|           |-- app.css
|           |-- app.js
|           |-- sample_sales.csv
|
|-- .venv/             # Local virtual environment; not committed
|-- .env               # Local secrets; not committed
```

Some files may be omitted if they are not present in your local repository. The `.venv/` and `.env` entries above illustrate local development files; they should not be uploaded to GitHub.

### Important Files

- `manage.py`: Django command-line entry point.
- `settings.py`: Application configuration, installed apps, database settings, and security options.
- `urls.py`: Project-level URL routing.
- `models.py`: Database model definitions.
- `views.py`: Request-handling logic.
- `services.py`: Reusable business logic and data processing.
- `admin.py`: Django admin model registration.
- `tests.py`: Automated tests.
- `templates/`: HTML templates.
- `static/`: CSS, JavaScript, and sample data.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Container build instructions.
- `render.yaml`: Deployment configuration for Render, subject to verification.

---

## 11. Prerequisites

Before setting up the application, install:

- Python 3.11 or another version supported by the dependencies.
- Git.
- A terminal such as PowerShell, Command Prompt, or Bash.
- A web browser.
- Optional: a Groq API key if using the external AI assistant.

Check the installed versions:

```bash
python --version
git --version
```

---

## 12. Installation and Setup

### Step 1: Clone the Repository

After uploading the project to GitHub, clone it with:

```bash
git clone https://github.com/YOUR-USERNAME/intellistock.git
cd intellistock
```

Replace `YOUR-USERNAME` with the appropriate GitHub username.

### Step 2: Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the commands from Command Prompt using:

```bat
.venv\Scripts\activate.bat
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a local `.env` file using the examples in the next section.

Never commit real credentials, API keys, or production secrets.

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 6: Create an Administrator

```bash
python manage.py createsuperuser
```

Follow the prompts to create the admin username and password.

### Step 7: Run System Checks

```bash
python manage.py check
```

### Step 8: Start the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 13. Environment Variables

The application may use environment variables for settings and optional integrations.

Create a `.env` file in the project root:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=

GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b
```

These values are examples. Confirm the variable names and defaults used in `intellistock/settings.py` and the AI service before relying on them.

### Variable Reference

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django cryptographic signing key |
| `DEBUG` | Enables or disables Django debug mode |
| `ALLOWED_HOSTS` | Hostnames permitted to serve the application |
| `DATABASE_URL` | Optional database connection string, if supported by the project |
| `GROQ_API_KEY` | Optional credential for the external AI service |
| `GROQ_MODEL` | Configured language-model identifier, if supported |

### Keep Secrets Out of Git

The `.gitignore` file should include:

```gitignore
.env
.env.*
!.env.example

.venv/
venv/
__pycache__/
*.py[cod]
db.sqlite3
staticfiles/
```

You can commit `.env.example` only when it contains placeholders rather than real secrets.

For production, use a strong secret key, set `DEBUG=False`, configure the actual deployment hostname, and store credentials in the hosting platform's environment settings.

---

## 14. Database Migrations

Django migrations track database schema changes.

After changing model definitions, generate migrations:

```bash
python manage.py makemigrations
```

Apply them:

```bash
python manage.py migrate
```

To inspect migration status:

```bash
python manage.py showmigrations
```

To validate the application configuration:

```bash
python manage.py check
```

Migrations should be committed to version control so that other developers and deployment environments can create the required database schema.

---

## 15. Running the Application

Start the server:

```bash
python manage.py runserver
```

### Common Local URLs

| Path | Intended purpose |
|---|---|
| `/` | Dashboard or home page |
| `/products/` | Product management page |
| `/forecast/` | Demand forecasting page |
| `/assistant/` | AI assistant page |
| `/admin/` | Django administration |
| `/health/` | Health check endpoint, if configured |

These paths reflect the intended project routes. Confirm them in `inventory/urls.py` and `intellistock/urls.py` before publishing them as guaranteed working endpoints.

### Django Admin

Visit:

```text
http://127.0.0.1:8000/admin/
```

Sign in with the superuser credentials created earlier.

Only models registered in Django admin will appear. The admin panel is intended for authorized management and development, not public access to administrative credentials.

---

## 16. Application Modules

### 16.1 Dashboard Module

**Responsibility:** Summarize inventory-related information.

**Typical flow:**

1. The user opens the dashboard.
2. The view retrieves the required data.
3. The backend prepares summary values.
4. The template renders the dashboard.

### 16.2 Product Module

**Responsibility:** Display and manage product information supported by the implementation.

**Typical flow:**

1. The user opens the products page.
2. Django retrieves product records.
3. The view passes the records to the template.
4. The frontend displays the product information.

### 16.3 Forecasting Module

**Responsibility:** Estimate future demand using historical sales data.

**Typical flow:**

1. Retrieve or load the relevant sales history.
2. Prepare the dataset.
3. Apply the configured forecasting method.
4. Return the result to the view.
5. Display the forecast in the user interface.

### 16.4 AI Assistant Module

**Responsibility:** Provide optional interaction with an external language model.

**Typical flow:**

1. The user submits a prompt.
2. The backend validates the request.
3. The configured AI client sends the prompt to the provider.
4. The backend handles the response or error.
5. The interface displays the result.

The external AI service may have rate limits, usage limits, network requirements, or costs depending on the provider's current terms and account.

### 16.5 Services Module

**Responsibility:** Keep reusable business logic outside the views where practical.

Separating service logic makes the application easier to maintain, test, and extend.

---

## 17. Testing and Quality Checks

Run the automated test suite:

```bash
python manage.py test
```

Run Django's configuration checks:

```bash
python manage.py check
```

If the repository is configured for pytest, tests may also be run with:

```bash
pytest
```

### What Should Be Tested?

- Dashboard responses.
- Product-page behavior.
- Valid and invalid input handling.
- Database operations.
- Forecasting behavior with representative data.
- Missing or malformed CSV input.
- AI integration error handling, if implemented.
- Health-check response behavior, if available.

### Testing Best Practices

- Use predictable sample data.
- Test normal cases and edge cases.
- Avoid depending on real external AI calls in ordinary unit tests.
- Keep secrets and production data out of tests.
- Verify tests pass before merging changes or deploying.

A successful test run demonstrates that the covered checks pass; it does not guarantee that every feature is bug-free.

---

## 18. API and Health Check

The current project is primarily a Django web application. Do not assume that it exposes a REST API unless API routes and handlers have been implemented.

If `/health/` is configured, it can be used as a basic health-check endpoint to determine whether the application responds.

A simple health check does not necessarily verify database availability, AI-provider connectivity, or the correctness of forecasting output. These require additional checks if needed.

---

## 19. Deployment

The repository includes deployment-related files that may support containerized or hosted deployment. Verify their contents and environment assumptions before deploying.

### General Deployment Workflow

1. Push the project to GitHub.
2. Select a hosting platform that supports Django.
3. Configure the build and start commands.
4. Add the required production environment variables.
5. Configure the production database.
6. Apply database migrations.
7. Configure static-file handling.
8. Run Django deployment checks.
9. Open the deployed application and test its main workflows.

### Production Considerations

- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS` with the real deployment hostname.
- Use a secure production `SECRET_KEY`.
- Keep database credentials and AI API keys private.
- Configure persistent database storage.
- Configure static-file serving.
- Review HTTPS and secure-cookie settings.
- Ensure the deployment process applies migrations safely.

A deployment configuration file alone does not prove that the application is currently deployed or available. Add a live URL only after verifying the deployment.

---

## 20. Security Considerations

Security is an important part of a full-stack application.

- Do not commit `.env` files or API credentials.
- Do not expose the Django secret key.
- Disable debug mode in production.
- Restrict administrative access.
- Validate and sanitize user-provided inputs.
- Use Django's built-in CSRF protection for applicable forms.
- Use secure database credentials and appropriate permissions.
- Avoid logging passwords, API keys, or other sensitive data.
- Apply updates to dependencies when needed.
- Handle external API failures without exposing secrets or internal traces.

If a secret is accidentally pushed to a public repository, removing the file from a later commit may not remove it from Git history. Revoke or rotate the exposed credential first, then clean the repository history if necessary.

---

## 21. Limitations and Future Enhancements

### Current Limitations

- Forecast quality depends on the quantity and quality of historical sales data.
- Sample CSV data does not represent actual business operations.
- External AI features require valid configuration and provider availability.
- Production readiness depends on database, security, deployment, and monitoring configuration.
- Forecasting accuracy should be measured before making business-critical decisions.

### Future Enhancements

1. User authentication and role-based permissions.
2. Product categories and supplier management.
3. Low-stock alerts and reorder recommendations.
4. Interactive sales and demand charts.
5. CSV upload and validation workflows.
6. More advanced time-series forecasting models.
7. Forecast evaluation using MAE, RMSE, or other suitable metrics.
8. Historical forecast-versus-actual comparisons.
9. Automated scheduled forecasting.
10. REST API integration for external clients.
11. Audit logs and inventory movement history.
12. Improved error monitoring and production observability.

These are proposed enhancements, not claims that all features are already implemented.

---

## 22. Learning Outcomes

This project provides practical experience with:

- Django project structure and request-response flow.
- Model design and database migrations.
- Backend views and template rendering.
- HTML, CSS, JavaScript, and responsive design.
- Data processing using Python and Pandas.
- Historical sales analysis and forecasting concepts.
- Optional third-party API integration.
- Automated testing and debugging.
- Environment-variable management.
- Git, GitHub, and deployment preparation.

The project also demonstrates how backend engineering and data analysis can work together to support a real-world business use case.

---

## 23. Author

**Sneha Kashyap**

Python Developer | Django | SQL | Data Analysis | Machine Learning Fundamentals

- GitHub: [snehaa94](https://github.com/snehaa94)
- LeetCode: [sneha_kashyap](https://leetcode.com/u/sneha_kashyap/)

---

## License

Choose and add an appropriate open-source license if you want others to reuse, modify, and distribute this project. Until a license is added, do not assume that the repository grants unrestricted reuse rights.

---

**IntelliStock — Turning Inventory Data into Better Decisions.**
