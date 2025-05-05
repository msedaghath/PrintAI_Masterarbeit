# Printers Module

## Overview

The Printers module manages all 3D printer-related functionality for the PrintAI Dashboard. This module handles printer configuration, control, and monitoring through the OctoPrint REST API.

## Features

- Printer CRUD operations
- Printer control (home, pause, resume, etc.)
- Status monitoring
- File management and upload
- Webcam streaming

## Models

- `Printer`: Represents a 3D printer with connection details and status information

## Services

- `PrinterService`: Core service for printer operations
  - Connection management
  - Status retrieval
  - Command execution
  - File operations
- `MonitoringService`: Service for monitoring printer metrics

## Views

- `PrinterListView`: Lists all printers and handles adding new ones
- `PrinterUpdateView`: Updates printer information
- `PrinterDetailView`: Shows detailed printer information
- `ControlPrinterView`: Handles printer control operations
- `PingPrinterView`: Checks printer connectivity
- `WebcamStreamView`: Streams printer webcam feed

## URLs

- `/printers/`: Printer list and creation
- `/printers/update/<id>/`: Update printer details
- `/printers/detail/<id>/`: View printer details
- `/printers/delete/<id>/`: Delete printer
- `/printers/ping/<id>/`: Ping printer
- `/printers/control/<id>/`: Control printer
- `/printers/webcam/<id>/`: Stream webcam

## Templates

- `printer_list.html`: Lists all printers with control options
- `printer_detail.html`: Shows detailed printer information
- `printer_update.html`: Form for updating printer details
- `control_printer.html`: Interface for controlling printer operations

## Usage

This module integrates with the Accounts module to associate printers with user profiles and with the Monitoring module for data collection and analysis.

## Dependencies

- OctoRest client library
- Core validators for IP/URL validation
- Accounts module for user association