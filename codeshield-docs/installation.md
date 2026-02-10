# Installation Guide

## Prerequisites

Before installing CodeShield AI, ensure you have the following:

- **Node.js**: Version 16.x or higher
- **npm**: Version 7.x or higher
- **Git**: For cloning the repository

Check your versions:
```bash
node --version
npm --version
git --version
```

## Installation Methods

### Method 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/Lydiamorgan85/codeshield-ai.git

# Navigate to the project directory
cd codeshield-ai

# Install dependencies
npm install

# Verify installation
npm test
```

### Method 2: Download ZIP

1. Visit https://github.com/Lydiamorgan85/codeshield-ai
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file
5. Open terminal in the extracted folder
6. Run `npm install`

## Configuration

### Basic Configuration

Create a `.codeshield.config.js` file in your project root:

```javascript
module.exports = {
  // Languages to analyze
  languages: ['javascript', 'python'],
  
  // Severity levels to report
  severity: ['critical', 'high', 'medium'],
  
  // Exclude patterns
  exclude: [
    'node_modules/**',
    'dist/**',
    '*.test.js'
  ],
  
  // Custom rules (optional)
  customRules: []
};
```

### Environment Variables

For advanced features, set these environment variables:

```bash
# .env file
CODESHIELD_API_KEY=your_api_key_here
CODESHIELD_LOG_LEVEL=info
CODESHIELD_OUTPUT_FORMAT=json
```

## Verification

After installation, verify everything works:

```bash
# Run self-test
npm run verify

# Analyze sample code
npm run demo

# Run full test suite
npm test
```

Expected output:
```
✓ CodeShield AI installed successfully
✓ All dependencies resolved
✓ Configuration valid
✓ Ready to analyze code
```

## Troubleshooting

### Common Issues

**Issue: "Cannot find module 'xyz'"**
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Issue: "Permission denied"**
```bash
# Solution: Fix permissions (Unix/Mac)
sudo chown -R $(whoami) ~/.npm
npm install

# Solution: Run as administrator (Windows)
# Right-click Command Prompt → Run as Administrator
npm install
```

**Issue: "Unsupported Node version"**
```bash
# Solution: Update Node.js
# Visit https://nodejs.org and download latest LTS version
```

## Next Steps

After successful installation:

1. Read the [Usage Guide](usage.md)
2. Review [API Documentation](api.md)
3. Check [Examples](examples.md)
4. Join our community discussions

## Uninstallation

To remove CodeShield AI:

```bash
# Remove global installation
npm uninstall -g codeshield-ai

# Remove local installation
cd your-project
npm uninstall codeshield-ai

# Clean cache (optional)
npm cache clean --force
```

## Support

Having issues? 
- Check [Troubleshooting Guide](troubleshooting.md)
- Open an issue on GitHub
- Email: lydiamorgan000@gmail.com
