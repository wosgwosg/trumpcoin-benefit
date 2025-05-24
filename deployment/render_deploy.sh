#!/bin/bash
# Script to deploy the TrumpCoin Benefit application to Render.com

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}===== TrumpCoin Benefit Render.com Deployment Script =====${NC}"
echo

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed. Please install git and try again.${NC}"
    exit 1
fi

# Check if we're in the project root directory
if [ ! -f "manage.py" ] || [ ! -d "trumpcoin_benefit" ]; then
    echo -e "${RED}Error: This script must be run from the project root directory.${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Collecting static files locally to verify they work${NC}"
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to collect static files. Please fix the errors and try again.${NC}"
    exit 1
fi
echo -e "${GREEN}Static files collected successfully.${NC}"
echo

echo -e "${YELLOW}Step 2: Checking for uncommitted changes${NC}"
git status

echo
echo -e "${YELLOW}Do you want to commit these changes? (y/n)${NC}"
read -r commit_changes

if [ "$commit_changes" = "y" ] || [ "$commit_changes" = "Y" ]; then
    echo -e "${YELLOW}Enter commit message:${NC}"
    read -r commit_message
    
    git add .
    git commit -m "$commit_message"
    
    echo -e "${GREEN}Changes committed successfully.${NC}"
else
    echo -e "${YELLOW}Skipping commit. Make sure to commit your changes before pushing.${NC}"
fi

echo
echo -e "${YELLOW}Step 3: Push to GitHub${NC}"
echo -e "${YELLOW}Do you want to push to GitHub now? (y/n)${NC}"
read -r push_changes

if [ "$push_changes" = "y" ] || [ "$push_changes" = "Y" ]; then
    echo -e "${YELLOW}Enter branch name (default: main):${NC}"
    read -r branch_name
    branch_name=${branch_name:-main}
    
    git push origin "$branch_name"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to push to GitHub. Please check your credentials and try again.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Changes pushed to GitHub successfully.${NC}"
    echo -e "${GREEN}Render.com will automatically deploy the new changes.${NC}"
else
    echo -e "${YELLOW}Skipping push. Remember to push your changes to GitHub to trigger a deployment on Render.com.${NC}"
fi

echo
echo -e "${YELLOW}Step 4: Deployment Checklist${NC}"
echo -e "${GREEN}✓${NC} Updated render.yaml to include collectstatic command"
echo -e "${GREEN}✓${NC} Added diagnostic views for troubleshooting"
echo -e "${GREEN}✓${NC} Created test HTML and CSS files"
echo -e "${GREEN}✓${NC} Updated render_settings.py with improved configuration"
echo -e "${GREEN}✓${NC} Added inline styles to base_render.html template"

echo
echo -e "${YELLOW}After deployment, check the following URLs:${NC}"
echo -e "1. ${GREEN}/static/test.html${NC} - Basic static file test"
echo -e "2. ${GREEN}/static/test-with-css.html${NC} - CSS loading test"
echo -e "3. ${GREEN}/debug-info/${NC} - Environment and configuration information"
echo -e "4. ${GREEN}/test-template/${NC} - Template rendering test"

echo
echo -e "${YELLOW}If you encounter any issues:${NC}"
echo -e "1. Check the Render.com logs for error messages"
echo -e "2. Verify that the staticfiles directory exists on the server"
echo -e "3. Make sure WhiteNoise is configured correctly"
echo -e "4. Check that the CSS files are being loaded properly"

echo
echo -e "${GREEN}Deployment preparation completed successfully!${NC}"
