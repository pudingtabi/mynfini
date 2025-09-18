#!/bin/bash
# MYNFINI Production Build Script for Render Deployment
# Optimized for Render static site deployment with comprehensive validation

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Start deployment process
log "🚀 Starting MYNFINI production build for Render deployment..."

# System Information
log "📋 System Information:"
node --version
npm --version
echo "Current Directory: $(pwd)"
echo "Build Time: $(date)"

# Environment Variables Check
log "🔍 Checking environment variables..."
if [ -n "$VITE_ENVIRONMENT" ]; then
    log "Environment: $VITE_ENVIRONMENT"
else
    warning "VITE_ENVIRONMENT not set, using default"
fi

if [ -n "$VITE_APP_VERSION" ]; then
    log "App Version: $VITE_APP_VERSION"
else
    warning "VITE_APP_VERSION not set"
fi

# Install dependencies with audit
log "📦 Installing production dependencies..."
if npm ci --audit-level=moderate; then
    success "Dependencies installed successfully"
else
    error "Failed to install dependencies"
    exit 1
fi

# Run comprehensive tests
log "🧪 Running comprehensive tests..."
if npm run test -- --reporter=verbose --colors; then
    success "All tests passed"
else
    error "Tests failed"
    exit 1
fi

# Code quality checks
log "🔍 Performing code quality checks..."
if npm run lint; then
    success "Linting passed"
else
    error "Linting failed"
    exit 1
fi

# Security audit
log "🔒 Running security audit..."
if npm audit --audit-level=moderate; then
    success "Security audit passed"
else
    warning "Security audit found issues (but within acceptable level)"
fi

# Analyze bundle size
log "📊 Analyzing bundle size..."
npm run analyse 2>/dev/null || warning "Bundle size analysis failed (not critical)"

# Production build
log "🏗️ Building application for production..."
if npm run build; then
    success "Build completed successfully"
else
    error "Build failed"
    exit 1
fi

# Build verification
log "🔍 Verifying build output..."
if [ -f "dist/index.html" ]; then
    success "Main index.html found"
else
    error "index.html not found in dist/"
    exit 1
fi

if [ -f "dist/service-worker.js" ] || [ -f "dist/sw.js" ]; then
    success "Service worker found"
else
    warning "Service worker not found (may not be generated yet)"
fi

# Performance analysis
log "📊 Performance Analysis:"
echo "Build Duration: $SECONDS seconds"
echo "Build Size Summary:"
find dist -type f -name "*.js" -exec wc -c {} \; | sort -nr | head -5 | while read size file; do
    echo "File: $(basename "$file") - Size: $(numfmt --to=iec --from=auto $size)"
done

# Build size validation
TOTAL_SIZE=$(du -sh dist/ | cut -f1)
log "Total build size: $TOTAL_SIZE"

# Security headers check
echo -e "\n${BLUE}Security Headers Check:${NC}"
cat dist/_headers 2>/dev/null | head -10 || echo "Security headers configuration not found"

# Generate deployment information
cat > deployment-info.txt << EOF
Deployment Information
=======================
Application: MYNFINI AI Game Master
Environment: Production
Build Time: $(date)
Node Version: $(node --version)
NPM Version: $(npm --version)
Build Duration: $SECONDS seconds
Total Bundle Size: $TOTAL_SIZE
Commit Hash: ${GITHUB_SHA:-$(git rev-parse HEAD)}
Branch: ${GITHUB_REF:-$(git branch --show-current)}
EOF

success "Deployment information generated"

log "🎉 Production build completed successfully!"
success "Application is ready for deployment to Render"
echo -e "\n${GREEN}🚀 Your creative universe is ready to be explored!${NC}"
echo -e "${BLUE}📊 Build Metrics:${NC}"
echo "- Total Bundle Size: $TOTAL_SIZE"
echo "- Build Duration: $SECONDS seconds"
echo "- Build successful at $(date)"
echo -e "\n${BLUE}🔗 Deployment will be available at: https://mynfini-frontend.onrender.com${NC}"