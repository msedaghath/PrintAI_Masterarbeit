# Database Migration Plan

## Overview

This document outlines the migration process for transitioning from the monolithic portal app structure to the new modular architecture with separate apps for accounts, printers, monitoring, and API.

## Migration Steps

1. **Preparation Phase**
   - Create initial migrations for all new apps without making database changes
   - Create data migration scripts to transfer data between models
   - Test migrations in development environment

2. **Execution Process**
   - Backup existing database
   - Run initial structure migrations
   - Execute data transfer migrations
   - Run final model migrations
   - Verify data integrity

3. **Rollback Plan**
   - If issues arise, restore database backup
   - Temporarily revert to the old codebase

## Data Migration Details

### Profile Model Migration
- Source: `portal.Profile`
- Target: `accounts.Profile`
- Fields to migrate:
  - user (FK to User)
  - name
  - email
  - username
  - organization

### Printer Model Migration
- Source: `portal.Printer`
- Target: `printers.Printer`
- Fields to migrate:
  - profile (FK to Profile)
  - ip_address
  - api_key
  - id (primary key)
  - ping
  - printing

## Implementation Commands

To generate migrations without applying them:

```bash
python manage.py makemigrations accounts printers monitoring api core
```

To create data migration files:

```bash
python manage.py makemigrations accounts --empty --name=migrate_profile_data
python manage.py makemigrations printers --empty --name=migrate_printer_data
```

To apply migrations:

```bash
python manage.py migrate
```

## Post-Migration Verification

After the migration, run verification scripts to ensure:

1. No data was lost during transfer
2. Foreign key relationships are maintained 
3. All functionality works as expected with the new models

## Temporary Compatibility Layer

To ensure backward compatibility during transition, the original models in the portal app will temporarily remain but will proxy data to the new models via database triggers or application-level redirection.