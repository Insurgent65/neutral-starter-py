# Configuration

This directory contains the application configuration files.

## Files

- **`.env.example`** - Template with all available configuration variables and their default values.
- **`.env`** - Actual configuration file (not included in the repository, must be created from `.env.example`).

## Usage

To configure the application:

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and modify the values according to your environment:
   - `SECRET_KEY`: Secret key for the application (change it in production)
   - `SITE_DOMAIN` and `SITE_URL`: Configure your domain
   - Database configuration if using something other than SQLite
   - Mail configuration if you need to send emails

3. Variables with empty values in `.env.example` are optional or will use the default values defined in the code.

## Important Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `SECRET_KEY` | Secret key for sessions and tokens | - |
| `SITE_DOMAIN` | Site domain | `localhost` |
| `SITE_URL` | Full site URL | `http://localhost` |
| `ALLOWED_HOSTS` | Allowed request hosts (comma separated, wildcard supported) | `localhost` |
| `NEUTRAL_IPC` | Enable IPC mode | `False` |
| `NEUTRAL_CACHE_DISABLE` | Disable cache | `False` |
| `TEMPLATE_HTML_MINIFY` | Minify HTML | `False` |
| `VALIDATE_SIGNUP` | Validate user registrations | `True` |
