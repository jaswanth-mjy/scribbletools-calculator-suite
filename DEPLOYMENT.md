# ScribbleTools Deployment Guide

## Subdomain Setup: scribbletools.shramkavach.com

This folder contains the ScribbleTools calculator suite that should be deployed to the `scribbletools.shramkavach.com` subdomain.

### What Changed

✅ **All URLs updated** from `scribbletools.in` to `scribbletools.shramkavach.com`
✅ **Main ShramKavach site updated** with links and banners to the subdomain
✅ **Navigation integrated** - ScribbleTools appears in main site menu
✅ **Footer links added** - Quick access from main site footer

### Deployment Steps

1. **DNS Configuration**
   - Add an A record or CNAME for `scribbletools.shramkavach.com` pointing to your hosting server
   - Example CNAME: `scribbletools.shramkavach.com` → Your hosting provider

2. **GitHub Pages Deployment (If using GitHub Pages)**
   ```bash
   # Option 1: Deploy this folder to a separate repo
   cd scribbletools
   git init
   git add .
   git commit -m "Initial ScribbleTools subdomain deployment"
   git branch -M main
   git remote add origin <your-scribbletools-repo-url>
   git push -u origin main
   ```

3. **Hosting Configuration**
   - Point the subdomain document root to this `scribbletools/` folder
   - Ensure `.htaccess` file is active (already included)
   - Verify `robots.txt` and `sitemap.xml` are accessible

4. **SSL Certificate**
   - Ensure SSL/TLS certificate covers `scribbletools.shramkavach.com`
   - Most hosting providers auto-generate wildcard certs for `*.shramkavach.com`

### Verification Checklist

After deployment, verify:

- [ ] https://scribbletools.shramkavach.com loads correctly
- [ ] https://scribbletools.shramkavach.com/sitemap.xml is accessible
- [ ] https://scribbletools.shramkavach.com/robots.txt is accessible
- [ ] Links from main site (shramkavach.com) work correctly
- [ ] All canonical URLs point to scribbletools.shramkavach.com
- [ ] SSL certificate is valid

### SEO Configuration

Already configured in the files:
- ✅ Canonical URLs updated
- ✅ Open Graph meta tags updated
- ✅ Twitter Card meta tags updated
- ✅ Schema.org structured data updated
- ✅ Sitemap.xml updated
- ✅ Robots.txt updated

### Integration with Main Site

The main ShramKavach site now includes:
1. **Navigation link** - ScribbleTools in main menu
2. **Hero banner** - Prominent announcement section
3. **Footer link** - Quick access in footer
4. **Sitemap reference** - Comment in main sitemap.xml

### File Structure

```
scribbletools/
├── index.html                 # Main landing page
├── all-tools.html            # Complete tool directory
├── client/
│   └── tools/
│       ├── financial/        # Financial calculators
│       ├── health/           # Health calculators
│       ├── math/             # Math calculators
│       ├── text/             # Text tools
│       ├── student/          # Student tools
│       ├── image/            # Image tools
│       └── other/            # Other utilities
├── assets/                   # Images, CSS, JS
├── api/                      # API endpoints (if any)
├── sitemap.xml              # Subdomain sitemap
├── robots.txt               # Subdomain robots.txt
└── .htaccess                # Apache configuration

```

### Support

For issues or questions:
- Main site: https://shramkavach.com
- Contact: Check main site for contact information

---

**Last Updated:** December 28, 2025
**Status:** Ready for deployment
