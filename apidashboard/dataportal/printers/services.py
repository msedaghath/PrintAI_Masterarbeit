import requests
import csv
import io
import urllib.parse
from datetime import datetime
from octorest import OctoRest
from .models import Printer

class PrinterService:
    """Service class for managing printer operations and data retrieval"""
    
    @staticmethod
    def get_client(printer):
        """
        Create an OctoRest client for the given printer
        
        Args:
            printer (Printer): Printer model instance
            
        Returns:
            OctoRest: Configured client for the printer
        """
        url = printer.ip_address if any(x in printer.ip_address for x in ['http://', 'https://']) else f"http://{printer.ip_address}"
        return OctoRest(url=url, apikey=printer.api_key, timeout=3)

    @staticmethod
    def ping_printer(printer):
        """
        Check if a printer is online and update its status
        
        Args:
            printer (Printer): Printer model instance
            
        Returns:
            bool: True if printer is online, False otherwise
        """
        try:
            client = PrinterService.get_client(printer)
            is_ready = client.printer()['state']['flags']['ready']
            printer.ping = True
            printer.save()
            return True
        except Exception:
            printer.ping = False
            printer.save()
            return False

    @staticmethod
    def get_printer_status(printer):
        """
        Get comprehensive status information for a printer
        
        Args:
            printer (Printer): Printer model instance
            
        Returns:
            dict: Printer status information
        """
        try:
            client = PrinterService.get_client(printer)
            status = client.printer()
            return {
                'version': client.version['server'],
                'is_printing': status['state']['flags']['printing'],
                'temperature': status['temperature'],
                'state': status['state']['text']
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_printer_files(printer):
        """
        Get list of files available on the printer
        
        Args:
            printer (Printer): Printer model instance
            
        Returns:
            list: Available files on the printer
        """
        try:
            client = PrinterService.get_client(printer)
            file_list = client.files()['files']
            return [{'name': file['display'], 'path': file['path'], 'size': file['size']} for file in file_list]
        except Exception:
            return []
            
    @staticmethod
    def send_printer_command(printer, command, **kwargs):
        """
        Send a command to the printer
        
        Args:
            printer (Printer): Printer model instance
            command (str): Command to send ('home', 'pause', etc.)
            **kwargs: Additional arguments for the command
            
        Returns:
            bool: Success status
        """
        try:
            client = PrinterService.get_client(printer)
            
            if command == 'home':
                client.home()
            elif command == 'pause':
                client.pause()
            elif command == 'resume':
                client.resume()
            elif command == 'cancel':
                client.cancel()
            elif command == 'start':
                client.start()
            elif command == 'restart':
                client.restart()
            elif command == 'shutdown':
                client.execute_system_command(source='core', action='shutdown')
            elif command == 'upload' and kwargs.get('file'):
                client.files.upload(kwargs['file'].temporary_file_path())
            else:
                return False
                
            return True
        except Exception:
            return False


class MonitoringService:
    """Service class for monitoring printer data and metrics"""
    
    @staticmethod
    def get_last_print_data(printer):
        """
        Get the most recent print data for a printer from Prometheus
        
        Args:
            printer (Printer): Printer model instance
            
        Returns:
            dict: Last print data or empty dict if not available
        """
        try:
            prom_url = "http://prometheus:9090/api/v1/query"
            query = f'octoprint_printer_state_info{{instance="{printer.ip_address}:80"}}'
            response = requests.get(prom_url, params={'query': query})
            data = response.json()

            if data.get('status') == 'success' and data['data']['result']:
                metric = data['data']['result'][0]['metric']
                state_id = metric.get('state_id', 'Unknown')
                return {'state_id': state_id}
            return {}
        except Exception:
            return {}

    @staticmethod
    def export_instance_data_to_csv(printer, start_time, end_time):
        """
        Export printer data from Prometheus to CSV for the given time range
        
        Args:
            printer (Printer): Printer model instance
            start_time (str): Start time in ISO format
            end_time (str): End time in ISO format
            
        Returns:
            str: CSV data or empty string if error
        """
        try:
            # Format timestamps to ISO 8601 with Z suffix
            start_dt = datetime.fromisoformat(start_time).strftime('%Y-%m-%dT%H:%M:%SZ')
            end_dt = datetime.fromisoformat(end_time).strftime('%Y-%m-%dT%H:%M:%SZ')

            # Validate that end_dt is after start_dt
            if end_dt <= start_dt:
                raise ValueError("End time must be after start time")

            # Use the correct host and port for Prometheus
            prom_url = "http://raspiprintai:9090/api/v1/query_range"
            
            # Build query with the exact instance label format
            instance = printer.ip_address
            if not ":" in instance:
                instance += ":80"
            
            query = f'octoprint_printer_state_info{{instance="{instance}"}}'

            # Ensure the query URL matches the exact format
            query_url = f"{prom_url}?query={urllib.parse.quote(query)}&start={start_dt}&end={end_dt}&step=60s"
            
            response = requests.get(query_url)
            if response.status_code != 200:
                return ""

            data = response.json()
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['timestamp', 'state', 'value'])

            if data.get('status') == 'success' and data['data']['result']:
                for result in data['data']['result']:
                    state_id = result['metric'].get('state_id', 'unknown')
                    for timestamp, value in result['values']:
                        # Convert timestamp to ISO format
                        dt = datetime.fromtimestamp(timestamp).isoformat()
                        writer.writerow([dt, state_id, value])

            output.seek(0)
            return output.read()
        except Exception:
            return ""