#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Enterprise AI Assistant - Setup Wizard                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt

echo "Step 4: Setting up environment file..."
if [ -f .env ]; then
    echo "  .env file already exists, skipping..."
else
    cp .env.example .env
    echo "  Created .env file from template"
    echo "  ⚠️  Please edit .env and add your API keys!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env file and add your API keys"
echo "  2. Run: python run.py --llm openai"
echo "  3. Test: python demo_scenarios.py"
echo ""
