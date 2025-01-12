import json
from django.http import JsonResponse
from octorest import OctoRest
from .models import Printer
from django.views.decorators.csrf import csrf_exempt
import requests
import csv
import io
import urllib.parse
from datetime import datetime

class PrinterService:
    @staticmethod
    def get_client(printer):
        url = printer.ip_address if any(x in printer.ip_address for x in ['http://', 'https://']) else f"http://{printer.ip_address}"
        return OctoRest(url=url, apikey=printer.api_key , timeout=3)

    @staticmethod
    def ping_printer(printer):
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
        try:
            client = PrinterService.get_client(printer)
            return {
                'version': client.version['server'],
                'is_printing': client.printer()['state']['flags']['printing'],
                'temperature': client.printer()['temperature']
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_last_print_data(printer):
        try:
            prom_url = "http://prometheus:9090/api/v1/query"
            query = 'octoprint_printer_state_info{instance="141.41.42.202:80"}'
            response = requests.get(prom_url, params={'query': query})
            data = response.json()

            if data.get('status') == 'success' and data['data']['result']:
                # Read the state_id from the first result
                metric = data['data']['result'][0]['metric']
                state_id = metric.get('state_id', 'Unknown')
                return {'state_id': state_id}
            return {}
        except Exception:
            return {}

    @staticmethod
    def export_instance_data_to_csv(printer, start_time, end_time):
        """Export instance data from Prometheus to CSV for the given time range."""
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
            instance = "141.41.42.202:80"  # Using the specific instance
            query = f'octoprint_printer_state_info{{instance="{instance}"}}'

            params = {
                'query': query,
                'start': start_dt,
                'end': end_dt,
                'step': '60s'
            }

            # Ensure the query URL matches the exact format
            query_url = f"{prom_url}?query={urllib.parse.quote(query)}&start={start_dt}&end={end_dt}&step=60s"
            print(f"Debug - Query URL: {query_url}")
            
            response = requests.get(query_url)
            if response.status_code != 200:
                print(f"Prometheus query failed: {response.text}")
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
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return ""

class AlertService:
    @csrf_exempt
    def handle_alert(request):
        if request.method == 'POST':
            try:
                alert_data = json.loads(request.body)
                # Process the alert data here
                
                
                return JsonResponse({'status': 'success'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'invalid json'}, status=400)
        return JsonResponse({'status': 'invalid request'}, status=400)

