#!/bin/bash
# TrumpCoin Benefit Program Deployment Script
# This script automates the deployment process for the TrumpCoin Benefit Program

# Exit on error
set -e

# Configuration variables - MODIFY THESE
PROJECT_NAME="trumpcoin-benefit"
PROJECT_PATH="/path/to/trumpcoin-benefit"  # TODO: Update with your actual path
DOMAIN_NAME="trumpcoin-benefit.live"              # TODO: Update with your actual domain
GIT_REPO="https://github.com/wosgwosg/trumpcoin-benefit.git"  # TODO: Update with your actual repo
DB_NAME="trumpcoin_db"
DB_USER="trumpcoin_user"
DB_PASSWORD="your-secure-password"         # TODO: Update with a secure password
SERVER_USER="your_username"                # TODO: Update with your server username

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${YELLOW}==== $1 ====${NC}\n"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if running as root
if [ "$(id -u)" -eq 0 ]; then
    print_error "This script should not be run as root. Please run as a regular user with sudo privileges."
    exit 1
fi

# Check if required commands are installed
print_section "Checking prerequisites"
for cmd in git python3 pip3 sudo nginx; do
    if ! command -v $cmd &> /dev/null; then
        print_error "$cmd is not installed. Please install it and try again."
        exit 1
    fi
    print_success "$cmd is installed"
done

# Update system packages
print_section "Updating system packages"
sudo apt update && sudo apt upgrade -y
print_success "System packages updated"

# Install required packages
print_section "Installing required packages"
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib certbot python3-certbot-nginx
print_success "Required packages installed"

# Clone or update the repository
print_section "Setting up the project"
if [ -d "$PROJECT_PATH" ]; then
    echo "Project directory exists. Updating..."
    cd "$PROJECT_PATH"
    git pull
    print_success "Repository updated"
else
    echo "Project directory does not exist. Cloning..."
    git clone "$GIT_REPO" "$PROJECT_PATH"
    cd "$PROJECT_PATH"
    print_success "Repository cloned"
fi

# Set up virtual environment
print_section "Setting up virtual environment"
if [ ! -d "$PROJECT_PATH/venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
print_success "Dependencies installed"

# Create logs directory
mkdir -p logs
print_success "Logs directory created"

# Set up PostgreSQL database
print_section "Setting up PostgreSQL database"
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    print_success "Database $DB_NAME already exists"
else
    echo "Creating database and user..."
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    print_success "Database and user created"
fi

# Collect static files
print_section "Collecting static files"
python manage.py collectstatic --noinput --settings=trumpcoin_benefit.production_settings
print_success "Static files collected"

# Apply migrations
print_section "Applying migrations"
python manage.py migrate --settings=trumpcoin_benefit.production_settings
print_success "Migrations applied"

# Set up Gunicorn service
print_section "Setting up Gunicorn service"
sudo cp deployment/systemd/trumpcoin.service /etc/systemd/system/
sudo sed -i "s|/path/to/trumpcoin-benefit|$PROJECT_PATH|g" /etc/systemd/system/trumpcoin.service
sudo sed -i "s|your_username|$SERVER_USER|g" /etc/systemd/system/trumpcoin.service
sudo systemctl daemon-reload
sudo systemctl enable trumpcoin
sudo systemctl restart trumpcoin
print_success "Gunicorn service set up"

# Set up Nginx
print_section "Setting up Nginx"
sudo cp deployment/nginx/trumpcoin.conf /etc/nginx/sites-available/trumpcoin
sudo sed -i "s|your-domain.com|$DOMAIN_NAME|g" /etc/nginx/sites-available/trumpcoin
sudo sed -i "s|/path/to/trumpcoin-benefit|$PROJECT_PATH|g" /etc/nginx/sites-available/trumpcoin
if [ ! -f /etc/nginx/sites-enabled/trumpcoin ]; then
    sudo ln -s /etc/nginx/sites-available/trumpcoin /etc/nginx/sites-enabled/
fi
sudo nginx -t
sudo systemctl restart nginx
print_success "Nginx set up"

# Set up SSL with Let's Encrypt
print_section "Setting up SSL with Let's Encrypt"
read -p "Do you want to set up SSL with Let's Encrypt? (y/n): " setup_ssl
if [ "$setup_ssl" = "y" ]; then
    sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME
    print_success "SSL certificate installed"
else
    print_success "SSL setup skipped"
fi

# Final message
print_section "Deployment completed"
echo -e "The TrumpCoin Benefit Program has been deployed successfully!"
echo -e "You can now access your site at: https://$DOMAIN_NAME"
echo -e "\nTo create a superuser, run:"
echo -e "cd $PROJECT_PATH && source venv/bin/activate && python manage.py createsuperuser --settings=trumpcoin_benefit.production_settings"
echo -e "\nTo check the status of the Gunicorn service:"
echo -e "sudo systemctl status trumpcoin"
echo -e "\nTo view the logs:"
echo -e "sudo journalctl -u trumpcoin"
echo -e "sudo tail -f /var/log/nginx/trumpcoin-error.log"
