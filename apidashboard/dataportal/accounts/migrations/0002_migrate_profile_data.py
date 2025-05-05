from django.db import migrations

def migrate_profile_data(apps, schema_editor):
    """
    Migrates Profile data from portal app to accounts app
    """
    # Get the models
    OldProfile = apps.get_model('portal', 'Profile')
    NewProfile = apps.get_model('accounts', 'Profile')
    
    # Create a dictionary to keep track of mapping between old and new profiles
    profile_mapping = {}
    
    # Iterate through all profiles in the old model
    for old_profile in OldProfile.objects.all():
        # Create a new profile with the same data
        new_profile = NewProfile(
            user=old_profile.user,
            name=old_profile.name,
            email=old_profile.email,
            username=old_profile.username,
            organization=old_profile.organization
        )
        new_profile.save()
        
        # Store the mapping between old and new profiles for reference
        profile_mapping[old_profile.id] = new_profile.id
    
    return profile_mapping

def reverse_migrate_profile_data(apps, schema_editor):
    """
    Reverses the migration by deleting all accounts.Profile objects
    """
    NewProfile = apps.get_model('accounts', 'Profile')
    NewProfile.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),  # Depend on the portal's initial migration
        ('accounts', '0001_initial'),  # Add dependency on accounts' initial migration
    ]

    operations = [
        migrations.RunPython(migrate_profile_data, reverse_migrate_profile_data),
    ]