from django.db import migrations


def remove_consecutive_zero_locations(apps, schema_editor):
    Location = apps.get_model('robotit', 'Location')

    for robotti_id in Location.objects.values_list('robotti_id', flat=True).distinct():
        previous = None
        for location in Location.objects.filter(robotti_id=robotti_id).order_by('pk'):
            if (
                previous is not None
                and previous.location_x == 0
                and previous.location_y == 0
                and location.location_x == 0
                and location.location_y == 0
            ):
                location.delete()
            else:
                previous = location


class Migration(migrations.Migration):

    dependencies = [
        ('robotit', '0003_location_and_unique_robot_identity'),
    ]

    operations = [
        migrations.RunPython(remove_consecutive_zero_locations, migrations.RunPython.noop),
    ]
