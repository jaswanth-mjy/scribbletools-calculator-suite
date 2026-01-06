# ShramTools Deployment Guide

## Subdomain Setup: shramtools.shramkavach.com

This folder contains the ShramTools calculator suite that should be deployed to the `shramtools.shramkavach.com` subdomain.

### Recent Updates

✅ **Rebranded from ScribbleTools to ShramTools**
✅ **New modern UI/UX** - Professional header and footer
✅ **All 254 tools organized** - Financial, Health, Math, Text, Image, Student, Other
✅ **Sections collapsed by default** - Cleaner initial view
✅ **Search functionality** - Real-time tool filtering
✅ **Responsive design** - Works on all devices

### Deployment Steps

#### Option 1: Direct Server Deployment (Recommended)

1. **Upload Files to Server**
   ```bash
   # SSH into your server
   ssh user@your-server.com
   
   # Navigate to web directory
   cd /var/www/
   
   # Create subdomain directory
   sudo mkdir -p shramtools.shramkavach.com
   
   # Upload files (from local machine)
   scp -r /Users/mjaswanth/shramkavachscribbletools/scribbletools-calculator-suite/* user@your-server.com:/var/www/shramtools.shramkavach.com/
   ```

2. **DNS Configuration**
   - Log into your domain registrar (where shramkavach.com is registered)
   - Add an A record or CNAME:
     - **Type**: A Record or CNAME
     - **Name/Host**: `shramtools`
     - **Value**: Your server IP address (or main domain for CNAME)
     - **TTL**: 3600 (or auto)

3. **Web Server Configuration**

   **For Apache:**
   ```bash
   # Create virtual host configuration
   sudo nano /etc/apache2/sites-available/shramtools.shramkavach.com.conf
   ```
   
   Add this configuration:
   ```apache
   <VirtualHost *:80>
       ServerName shramtools.shramkavach.com
       ServerAlias www.shramtools.shramkavach.com
       DocumentRoot /var/www/shramtools.shramkavach.com
       
       <Directory /var/www/shramtools.shramkavach.com>
           Options -Indexes +FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>
       
       ErrorLog ${APACHE_LOG_DIR}/shramtools-error.log
       CustomLog ${APACHE_LOG_DIR}/shramtools-access.log combined
   </VirtualHost>
   ```
   
   Enable site and restart:
   ```bash
   sudo a2ensite shramtools.shramkavach.com.conf
   sudo systemctl restart apache2
   ```

   **For Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/shramtools.shramkavach.com
   ```
   
   Add this configuration:
   ```nginx
   server {
       listen 80;
       listen [::]:80;
       server_name shramtools.shramkavach.com www.shramtools.shramkavach.com;
       
       root /var/www/shramtools.shramkavach.com;
       index index.html;
       
       location / {
           try_files $uri $uri/ =404;
       }
       
       # Cache static assets
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```
   
   Enable site and restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/shramtools.shramkavach.com /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. **SSL Certificate (HTTPS)**
   ```bash
   # Install Certbot if not already installed
   sudo apt install certbot python3-certbot-apache  # For Apache
   # OR
   sudo apt install certbot python3-certbot-nginx   # For Nginx
   
   # Get SSL certificate
   sudo certbot --apache -d shramtools.shramkavach.com -d www.shramtools.shramkavach.com
   # OR
   sudo certbot --nginx -d shramtools.shramkavach.com -d www.shramtools.shramkavach.com
   
   # Certificate will auto-renew
   ```

#### Option 2: GitHub Pages with Custom Domain

1. **Create GitHub Repository**
   ```bash
   cd /Users/mjaswanth/shramkavachscribbletools/scribbletools-calculator-suite
   git init
   git add .
   git commit -m "Initial ShramTools deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/shramtools.git
   git push -u origin main
   ```

2. **GitHub Pages Setup**
   - Go to repository Settings → Pages
   - Source: Deploy from main branch
   - Custom domain: `shramtools.shramkavach.com`
   - Create `CNAME` file in root with content: `shramtools.shramkavach.com`

3. **DNS Configuration**
   - Add CNAME record: `shramtools` → `yourusername.github.io`

#### Option 3: cPanel / Shared Hosting

1. **Login to cPanel**
2. **Create Subdomain**
   - Go to Domains → Subdomains
   - Subdomain: `shramtools`
   - Domain: `shramkavach.com`
   - Document Root: `/public_html/shramtools`
3. **Upload Files**
   - Use File Manager or FTP
   - Upload all files to `/public_html/shramtools/`
4. **SSL Certificate**
   - Go to Security → SSL/TLS Status
   - Run AutoSSL for `shramtools.shramkavach.com`

### Verification Checklist

After deployment, verify:

- [ ] https://shramtools.shramkavach.com loads correctly
- [ ] Header shows "ShramTools" branding
- [ ] All 7 tool sections are visible (collapsed by default)
- [ ] Search functionality works
- [ ] Stats bar shows "254 Tools, 7 Categories"
- [ ] Footer displays properly with all links
- [ ] Back-to-top button appears on scroll
- [ ] SSL certificate is valid (padlock in browser)
- [ ] Mobile responsive (test on phone)
- [ ] Links to shramkavach.com work

### Testing URLs

Once deployed, test these URLs:
- https://shramtools.shramkavach.com
- https://shramtools.shramkavach.com/robots.txt
- https://www.shramtools.shramkavach.com (should redirect to non-www or vice versa)

### Troubleshooting

**Issue: "Site can't be reached"**
- Check DNS propagation: https://dnschecker.org
- Wait 24-48 hours for DNS to propagate globally

**Issue: "403 Forbidden"**
```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/shramtools.shramkavach.com
sudo chmod -R 755 /var/www/shramtools.shramkavach.com
```

**Issue: "404 Not Found"**
- Verify DocumentRoot path in virtual host config
- Check if index.html exists in the directory

**Issue: "SSL Certificate Error"**
```bash
# Manually run certbot
sudo certbot certonly --webroot -w /var/www/shramtools.shramkavach.com -d shramtools.shramkavach.com
```

### File Structure

```
shramtools.shramkavach.com/
├── index.html                 # Main landing page (NEW DESIGN)
├── all-tools.html            # Complete tool directory
├── 404.html                  # Error page
├── client/
│   └── tools/
│       ├── financial/        # 30 Financial calculators
│       ├── health/           # 46 Health calculators
│       ├── math/             # 33 Math calculators
│       ├── text/             # 45 Text tools
│       ├── image/            # 48 Image tools
│       ├── student/          # 47 Student tools
│       └── other/            # 5 Other utilities
├── assets/
│   ├── css/                  # Stylesheets
│   └── js/                   # JavaScript files
├── api/                      # API endpoints (if any)
├── robots.txt               # SEO robots file
├── sw.js                    # Service worker
├── CNAME                    # GitHub Pages domain
└── config.js                # Configuration

### Quick Start (If Server is Already Configured)

If your server already hosts shramkavach.com and you just need to add the subdomain:

1. Upload files to subdomain directory
2. DNS should auto-resolve if wildcard is configured
3. Run Certbot for SSL
4. Done!

### Support

For issues:
- Main site: https://shramkavach.com
- Updates: https://shramkavach.com/updates

---

**Current Status**: Ready for deployment
**Last Updated**: January 5, 2026

**Last Updated:** December 28, 2025
**Status:** Ready for deployment
