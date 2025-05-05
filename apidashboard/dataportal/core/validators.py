from django.core.exceptions import ValidationError
import ipaddress
from urllib.parse import urlparse

def validate_ip_or_url(value):
    """
    Validate that a given value is either a valid IP address or URL.
    
    Args:
        value (str): The IP address or URL to validate
        
    Raises:
        ValidationError: If the value is neither a valid IP address nor URL
    """
    try:
        ipaddress.ip_address(value)
    except ValueError:
        try:
            result = urlparse(value)
            if not all([result.scheme, result.netloc]):
                raise ValueError
        except ValueError:
            raise ValidationError(f"'{value}' is not a valid IP address or URL.")