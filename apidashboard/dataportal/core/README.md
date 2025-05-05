# Core Module

## Overview

The Core module provides shared functionality and central components for the PrintAI Dashboard. This module serves as the foundation for the application, providing utilities, validators, and central views used across the system.

## Features

- Central dashboard interface
- System health monitoring
- Shared utilities and validators
- Base components used by other modules

## Components

### Validators
- `validate_ip_or_url`: Validates IP addresses and URLs for printer connections

### Views
- `dashboard`: Central dashboard view for the application
- `SystemHealthView`: System health monitoring interface

### Utilities
- Common helper functions
- Shared constants
- System-wide configuration

## URLs

- `/dashboard/`: Main application dashboard
- `/dashboard/system-health/`: System health monitoring interface

## Templates

- `dashboard.html`: Main application dashboard template
- `system_health.html`: System health monitoring interface

## Usage

The Core module is used as a dependency by all other modules in the system. It provides shared functionality and common interfaces to ensure consistency across the application.

## Design Principles

- DRY (Don't Repeat Yourself): Shared components prevent code duplication
- Separation of Concerns: Core functionality separate from domain-specific modules
- Consistency: Common patterns and interfaces across modules