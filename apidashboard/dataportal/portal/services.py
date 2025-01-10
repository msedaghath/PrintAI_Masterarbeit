import json
from django.http import JsonResponse
from octorest import OctoRest
from .models import Printer
from django.views.decorators.csrf import csrf_exempt

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

class AlertService:
    @csrf_exempt
    def handle_alert(request):
        if request.method == 'POST':
            try:
                alert_data = json.loads(request.body)
                # Process the alert data here
                print(alert_data)
                return JsonResponse({'status': 'success'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'invalid json'}, status=400)
        return JsonResponse({'status': 'invalid request'}, status=400)

