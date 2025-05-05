from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from printers.models import Printer
from printers.services import MonitoringService

@login_required(login_url='login')
def export_csv(request, printer_id):
    """
    Export printer data to CSV for the given time range
    
    Args:
        request (HttpRequest): The HTTP request
        printer_id (int): ID of the printer to export data from
    
    Returns:
        HttpResponse: CSV data as a downloadable file
    """
    try:
        printer = get_object_or_404(Printer, id=printer_id)
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')

        if not all([start_time, end_time]):
            return HttpResponse("Start time and end time are required", status=400)

        # Validate that end_time is after start_time
        if end_time <= start_time:
            return HttpResponse("End time must be after start time", status=400)

        csv_data = MonitoringService.export_instance_data_to_csv(printer, start_time, end_time)
        if not csv_data:
            return HttpResponse("No data available for the specified time range", status=404)

        response = HttpResponse(csv_data, content_type='text/csv')
        filename = f"printer_{printer_id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except ValueError as e:
        return HttpResponse(f"Invalid date format: {str(e)}", status=400)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)