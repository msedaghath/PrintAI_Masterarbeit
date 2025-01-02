from octorest import OctoRest
from .models import Printer

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
