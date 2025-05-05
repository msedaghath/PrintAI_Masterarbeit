import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from printers.models import Printer

@csrf_exempt
def handle_alert(request):
    """
    Handle incoming alerts from monitoring systems
    
    Args:
        request (HttpRequest): The HTTP request
        
    Returns:
        JsonResponse: Response with status
    """
    if request.method == 'POST':
        try:
            alert_data = json.loads(request.body)
            # Process the alert data here
            # You can add logging or trigger notifications
            
            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'invalid json'}, status=400)
    return JsonResponse({'status': 'invalid request'}, status=400)

@csrf_exempt
def printer_status_update(request, printer_id=None):
    """
    Update printer status via API
    
    Args:
        request (HttpRequest): The HTTP request
        printer_id (int, optional): ID of the printer to update
        
    Returns:
        JsonResponse: Response with status
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        
        if printer_id:
            try:
                printer = Printer.objects.get(id=printer_id)
            except Printer.DoesNotExist:
                return JsonResponse({'status': 'Printer not found'}, status=404)
                
            # Update printer status
            if 'printing' in data:
                printer.printing = data['printing']
            if 'ping' in data:
                printer.ping = data['ping']
                
            printer.save()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'Printer ID required'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'invalid json'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)