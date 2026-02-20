# Research Partner Platform (Django Version)

This is the Django migration of the original Flask research collaboration platform.

## Setup Instructions

1.  **Navigate to the project directory:**
    ```bash
    cd "e:/My Django Project/Research Partner/research_platform/peermatch"
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the database:**
    ```bash
    python manage.py makemigrations core
    python manage.py migrate
    ```

4.  **Create an admin user:**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6.  **Access the application:**
    - Main site: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

- `manage.py`: Django's command-line utility.
- `peermatch_project/`: Project configuration (settings, urls, wsgi).
- `core/`: The main application containing models, views, and templates.
    - `models.py`: Database models (User, Idea, CollaborationRequest, ChatMessage).
    - `views.py`: Application logic and view functions.
    - `templates/`: HTML templates (adapted from Flask).
    - `static/`: Static files (CSS, JS, images).

## Features

- **User Authentication**: Login, Register, Profile management.
- **Research Ideas**: Post, view, and search for research ideas.
- **Collaboration**: Request to collaborate, accept/reject requests.
- **Messaging**: Real-time chat with collaborators.
- **Admin Dashboard**: Manage users, ideas, and collaborations.

## Notes

- The database is configured to use SQLite by default (`db.sqlite3`).
- Email backend is set to distinct console output for development.
- Media files (profile pictures) are stored in `media/` directory.
