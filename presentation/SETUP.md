# Presentation Website Setup

## Quick Start (Local Development)

1. **Navigate to presentation directory:**
   ```bash
   cd /home/justdial/Downloads/face_scanner/presentation
   ```

2. **Start the server:**
   ```bash
   python3 start_server.py
   ```

3. **Open in browser:**
   - Automatically opens at: http://localhost:8000
   - Or manually visit: http://localhost:8000

4. **Stop server:**
   - Press `Ctrl+C` in terminal

---

## Production Setup (/var/www/production/)

### Option 1: Copy Files (Recommended)

```bash
# Create directory (if doesn't exist)
sudo mkdir -p /var/www/production

# Copy presentation files
sudo cp -r /home/justdial/Downloads/face_scanner/presentation/* /var/www/production/

# Set permissions
sudo chown -R www-data:www-data /var/www/production
sudo chmod -R 755 /var/www/production
```

### Option 2: Symlink (For Development)

```bash
# Create directory
sudo mkdir -p /var/www/production

# Create symlink
sudo ln -s /home/justdial/Downloads/face_scanner/presentation /var/www/production/face-scanner

# Set permissions
sudo chown -R $USER:$USER /var/www/production
```

---

## Apache Configuration (If using Apache)

Add to `/etc/apache2/sites-available/000-default.conf`:

```apache
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot /var/www/production
    
    <Directory /var/www/production>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

Then restart Apache:
```bash
sudo systemctl restart apache2
```

---

## Nginx Configuration (If using Nginx)

Add to `/etc/nginx/sites-available/default`:

```nginx
server {
    listen 80;
    server_name localhost;
    root /var/www/production;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Then restart Nginx:
```bash
sudo systemctl restart nginx
```

---

## Access the Website

- **Local development**: http://localhost:8000 (Python server)
- **Apache/Nginx**: http://localhost (port 80)
- **Remote access**: http://your-server-ip

---

## Files Included

- `index.html` - Main presentation website
- `PRESENTATION_GUIDE.md` - Complete presentation guide
- `start_server.py` - Simple Python HTTP server
- `SETUP.md` - This file

---

## Troubleshooting

### Permission Denied
```bash
sudo chown -R $USER:$USER /var/www/production
sudo chmod -R 755 /var/www/production
```

### Port Already in Use
Change PORT in `start_server.py`:
```python
PORT = 8080  # or any available port
```

### Apache/Nginx Not Serving Files
- Check file permissions
- Check Apache/Nginx error logs: `sudo tail -f /var/log/apache2/error.log`
- Verify DocumentRoot path is correct
