#!/usr/bin/env bash
# exit on error
set -o errexit

# Debug: Show Python version
echo "Python version:"
python --version
echo "Pip version:"
pip --version

# Upgrade pip to latest version
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Debug: Show installed packages
echo "Installed packages:"
pip list | grep -E "(psycopg|django)"

# Test psycopg import
echo "Testing psycopg import..."
python -c "
try:
    import psycopg
    print('✓ psycopg imported successfully')
except ImportError as e:
    print('✗ psycopg import failed:', e)

try:
    import psycopg2
    print('✓ psycopg2 imported successfully')
except ImportError as e:
    print('✗ psycopg2 import failed:', e)
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "=== Verifying WSGI module ==="
python -c "import core.wsgi; print('✓ core.wsgi module found')"

echo "=== Checking Procfile ==="
if [ -f "Procfile" ]; then
    echo "✓ Procfile found:"
    cat Procfile
else
    echo "⚠ Procfile not found"
fi

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate