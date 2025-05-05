from django.db import migrations

def migrate_printer_data(apps, schema_editor):
    """
    Migrates Printer data from portal app to printers app
    """
    # Get the models
    OldPrinter = apps.get_model('portal', 'Printer')
    NewPrinter = apps.get_model('printers', 'Printer')
    NewProfile = apps.get_model('accounts', 'Profile')
    
    # Create mapping for profiles
    profile_mapping = {}
    for profile in NewProfile.objects.all():
        if hasattr(profile, 'user') and profile.user:
            profile_mapping[profile.user.id] = profile
    
    # Iterate through all printers in the old model
    for old_printer in OldPrinter.objects.all():
        # Get the associated profile
        old_profile = old_printer.profile
        new_profile = None
        
        if old_profile and old_profile.user:
            new_profile = profile_mapping.get(old_profile.user.id)
            
        # Create a new printer with the same data
        new_printer = NewPrinter(
            id=old_printer.id,  # Keep the same ID
            profile=new_profile,
            ip_address=old_printer.ip_address,
            api_key=old_printer.api_key,
            ping=old_printer.ping,
            printing=old_printer.printing
        )
        new_printer.save()

def reverse_migrate_printer_data(apps, schema_editor):
    """
    Reverses the migration by deleting all printers.Printer objects
    """
    NewPrinter = apps.get_model('printers', 'Printer')
    NewPrinter.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),  # Depend on the portal's initial migration
        ('accounts', '0002_migrate_profile_data'),  # Updated to point to the renamed migration
        ('printers', '0001_initial'),  # Add dependency on printers' initial migration
    ]

    operations = [
        migrations.RunPython(migrate_printer_data, reverse_migrate_printer_data),
    ]