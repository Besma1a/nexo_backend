"""
Hackathon Setup Script
Sets up the Smart Menu Recommendation System for hackathon presentation
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def setup_project():
    """Setup the hackathon project"""
    print("🚀 Setting up Smart Menu Recommendation System for Hackathon")
    print("=" * 70)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 8:
        print("❌ Python 3.8+ is required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Create necessary directories
    directories = [
        "logs",
        "static",
        "templates",
        "media",
        "data/raw",
        "questionnaire/templates/questionnaire",
        "questionnaire/static/questionnaire"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Generate mock data if it doesn't exist
    if not os.path.exists("data/raw/items.csv"):
        print("🔄 Generating mock data...")
        if run_command("python -m src.generate_mock_data", "Generating mock data"):
            print("✅ Mock data generated successfully")
        else:
            print("⚠️  Mock data generation failed, but continuing...")
    
    # Setup Django database
    print("🔄 Setting up Django database...")
    if run_command("python manage.py makemigrations", "Creating Django migrations"):
        if run_command("python manage.py migrate", "Running Django migrations"):
            print("✅ Django database setup completed")
        else:
            print("⚠️  Django migrations failed, but continuing...")
    else:
        print("⚠️  Django setup failed, but continuing...")
    
    # Create Django superuser (optional)
    print("\n🔐 Django Admin Setup:")
    print("   To create a superuser, run: python manage.py createsuperuser")
    print("   Then visit: http://127.0.0.1:8000/admin/")
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 70)
    print("🚀 Quick Start Commands:")
    print("   1. Run Demo: python hackathon_demo.py")
    print("   2. Start API: uvicorn src.api:app --reload")
    print("   3. Start Django: python manage.py runserver")
    print("   4. View Admin: http://127.0.0.1:8000/admin/")
    print("   5. API Docs: http://127.0.0.1:8000/docs")
    print("=" * 70)
    
    return True


def create_manage_py():
    """Create Django manage.py file"""
    manage_py_content = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_menu_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''
    
    with open("manage.py", "w") as f:
        f.write(manage_py_content)
    
    print("✅ Created manage.py")


if __name__ == "__main__":
    # Create manage.py if it doesn't exist
    if not os.path.exists("manage.py"):
        create_manage_py()
    
    # Setup project
    if setup_project():
        print("\n🎊 Ready for Hackathon! Good luck! 🎊")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

