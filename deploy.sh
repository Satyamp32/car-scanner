#!/bin/bash

# Exit on error
set -e

echo "====================================================="
echo "🚗 Vehicle Owner Contact QR System - Deployment Tools"
echo "====================================================="
echo ""
echo "Select an action:"
echo "1) Run local test server (http://localhost:8085)"
echo "2) Initialize Git and prepare for GitHub Pages"
echo "3) Deploy to Vercel (Requires Vercel CLI)"
echo "4) Re-generate QR Codes & Stickers with a custom URL"
echo "5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "--> Starting local development server at http://localhost:8085"
        echo "--> Press Ctrl+C to stop the server."
        echo ""
        # Open in default browser (macOS command)
        sleep 1 && open http://localhost:8085 || true
        python3 -m http.server 8085
        ;;
    2)
        echo ""
        echo "--> Preparing for GitHub Pages..."
        if [ ! -d .git ]; then
            git init
            echo "✓ Git repository initialized."
        else
            echo "✓ Git repository already exists."
        fi
        
        git add index.html styles.css assets/ generate_qr.py README.md
        git commit -m "Initial commit of Vehicle Contact QR System" || echo "No changes to commit."
        
        echo ""
        echo "To deploy to GitHub Pages:"
        echo "1. Create a public repository on GitHub (e.g., 'car-scanner')."
        echo "2. Run these commands to push your code:"
        echo "   git branch -M main"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/car-scanner.git"
        echo "   git push -u origin main"
        echo "3. Go to GitHub Repository -> Settings -> Pages."
        echo "4. Set source to 'Deploy from a branch', select 'main' branch and '/ (root)', then click Save."
        echo "5. Your page will be live at: https://YOUR_USERNAME.github.io/car-scanner/"
        ;;
    3)
        echo ""
        echo "--> Deploying to Vercel..."
        if ! command -v vercel &> /dev/null; then
            echo "Vercel CLI is not installed. You can install it using npm:"
            echo "  npm install -g vercel"
            echo "Or download the desktop app, or sign in to vercel.com and upload this directory."
            read -p "Would you like to try installing Vercel CLI via npm now? (y/n): " install_choice
            if [ "$install_choice" = "y" ] || [ "$install_choice" = "Y" ]; then
                npm install -g vercel
            else
                echo "Aborting Vercel CLI deployment. Please deploy manually via Vercel Web Dashboard."
                exit 0
            fi
        fi
        
        vercel login
        vercel deploy --prod
        echo "✓ Deployed to Vercel successfully!"
        ;;
    4)
        echo ""
        read -p "Enter your live deployment URL (e.g., https://yourusername.github.io/car-scanner): " custom_url
        if [ -z "$custom_url" ]; then
            echo "Error: URL cannot be empty."
            exit 1
        fi
        python3 generate_qr.py --url "$custom_url"
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac
