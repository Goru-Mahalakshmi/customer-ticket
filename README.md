# Customer Support Ticketing System

A comprehensive Flask-based customer support ticketing system with user authentication, role-based access control, and advanced reporting capabilities.

## Features

### Core Functionality
- **User Authentication**: Secure login/registration with bcrypt password hashing
- **Role-Based Access**: Separate user and admin portals with different permissions
- **Ticket Management**: Create, view, update, and assign support tickets
- **Comments System**: Add comments to tickets with internal/external visibility
- **Status Tracking**: Track ticket status (Open, In Progress, Closed)
- **Priority Management**: Set and manage ticket priorities (Low, Medium, High, Urgent)

### Admin Features
- **Dashboard**: Overview of all tickets and system statistics
- **Ticket Assignment**: Assign tickets to administrators
- **Advanced Reports**: Visual analytics with Chart.js
- **CSV Export**: Export ticket data for external analysis
- **User Management**: View and manage user accounts

### User Features
- **Personal Dashboard**: View own tickets and statistics
- **Ticket Creation**: Easy-to-use ticket creation form
- **Ticket Tracking**: Monitor ticket status and updates
- **Communication**: Add comments and communicate with support staff

### Technical Features
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Security**: CSRF protection, password hashing, session management
- **Modular Architecture**: Clean separation of concerns with blueprints

## Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Database
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **bcrypt**: Password hashing via Werkzeug

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icons
- **Vanilla JavaScript**: Client-side functionality

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

### Environment Variables
Set the following environment variables:

```bash
export DATABASE_URL="postgresql://username:password@host:port/database_name"
export SESSION_SECRET="your-secret-key-here"
