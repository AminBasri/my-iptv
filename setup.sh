#!/bin/bash

echo "╔═══════════════════════════════════════════════════════╗"
echo "║     Malaysian IPTV Setup Script                      ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        echo "✓ Python $PYTHON_VERSION found"
        return 0
    else
        echo "✗ Python 3 not found. Please install Python 3.8 or higher."
        return 1
    fi
}

create_venv() {
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
        echo "✓ Virtual environment created"
    else
        echo "✓ Virtual environment already exists"
    fi
}

activate_venv() {
    echo "🔄 Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "✓ Virtual environment activated"
    else
        echo "✗ Failed to activate virtual environment"
        return 1
    fi
}

install_deps() {
    echo "📚 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed successfully"
    else
        echo "✗ Failed to install dependencies"
        return 1
    fi
}

setup_env() {
    if [ ! -f ".env" ]; then
        echo "⚙️  Creating .env file..."
        cp .env.example .env
        echo "✓ .env file created. Please edit it with your settings."
    else
        echo "✓ .env file already exists"
    fi
}

create_data_dir() {
    if [ ! -d "data" ]; then
        mkdir -p data
        echo "✓ Data directory created"
    else
        echo "✓ Data directory already exists"
    fi
}

echo "Starting setup..."
echo ""

check_python || exit 1
create_venv || exit 1
activate_venv || exit 1
install_deps || exit 1
setup_env
create_data_dir

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║     Setup Complete! ✓                                ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python run.py"
echo "     Or: uvicorn app.main:app --reload"
echo ""
echo "The application will be available at:"
echo "  - Web UI:   http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
