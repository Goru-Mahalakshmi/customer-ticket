# Overview

This is a comprehensive Flask-based customer support ticketing system that provides role-based access control with separate user and admin portals. The system enables customers to create and track support tickets while allowing administrators to manage, assign, and analyze ticket data through an intuitive dashboard with reporting capabilities.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Framework**: Flask web framework with modular blueprint structure for clean separation of routes (auth, user, admin, api)
- **Database**: PostgreSQL with SQLAlchemy ORM for data persistence and relationship management
- **Authentication**: Flask-Login for session management with bcrypt password hashing via Werkzeug security utilities
- **Security**: CSRF protection through Flask-WTF, secure password storage, and role-based access control decorators

## Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **Visualization**: Chart.js for analytics dashboards and reporting charts
- **Icons**: Font Awesome for consistent iconography
- **Templates**: Jinja2 templating with base template inheritance and component reuse

## Data Model Design
- **Users**: Authentication with role-based permissions (user/admin)
- **Tickets**: Core entity with status tracking (open, in_progress, closed), priority levels, categories, and assignment capabilities
- **Comments**: Threaded discussions on tickets with internal/external visibility controls
- **Relationships**: Foreign key constraints linking users to their created and assigned tickets

## Role-Based Access Control
- **User Role**: Personal dashboard, ticket creation, viewing own tickets, commenting
- **Admin Role**: System-wide dashboard, all ticket management, user assignment, reporting, CSV export
- **Security**: Decorator-based route protection ensuring proper authorization

## API Structure
- **REST Endpoints**: JSON API for statistics, timeline data, and performance metrics
- **Data Aggregation**: Database queries using SQLAlchemy functions for analytics
- **Export Features**: CSV generation for ticket data analysis

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework
- **SQLAlchemy**: Database ORM and query builder
- **Flask-Login**: User authentication and session management
- **Flask-WTF**: Form handling with CSRF protection
- **Werkzeug**: Password hashing and security utilities

## Database
- **PostgreSQL**: Primary database with connection pooling and health checks configured

## Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme variant
- **Chart.js**: JavaScript charting library for data visualization
- **Font Awesome**: Icon library for UI elements

## Development Environment
- **Python**: Runtime environment
- **Environment Variables**: SESSION_SECRET for Flask sessions, DATABASE_URL for PostgreSQL connection