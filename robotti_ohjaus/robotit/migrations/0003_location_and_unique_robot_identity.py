from itertools import groupby

from django.db import migrations, models
import django.db.models.deletion


def move_locations_and_merge_duplicate_robots(apps, schema_editor):
    Robotti = apps.get_model('robotit', 'Robotti')
    Location = apps.get_model('robotit', 'Location')
    database = schema_editor.connection.alias

    robots = list(
        Robotti.objects.using(database).order_by(
            'modelname', 'serialnumber', 'pk'
        ).values_list('pk', 'modelname', 'serialnumber', 'location_x', 'location_y')
    )

    for _, grouped_robots in groupby(robots, key=lambda row: (row[1], row[2])):
        group = list(grouped_robots)
        canonical_id = group[0][0]
        robot_ids = [row[0] for row in group]

        for robot_id, _, _, location_x, location_y in group:
            if location_x is not None or location_y is not None:
                Location.objects.using(database).create(
                    robotti_id=robot_id,
                    location_x=location_x,
                    location_y=location_y,
                )

        if len(robot_ids) > 1:
            Location.objects.using(database).filter(
                robotti_id__in=robot_ids
            ).update(robotti_id=canonical_id)
            Robotti.objects.using(database).filter(
                pk__in=robot_ids[1:]
            ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('robotit', '0002_robotti_location_x_robotti_location_y'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_x', models.FloatField(blank=True, null=True)),
                ('location_y', models.FloatField(blank=True, null=True)),
                ('robotti', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='locations',
                    to='robotit.robotti',
                )),
            ],
        ),
        migrations.RunPython(move_locations_and_merge_duplicate_robots),
        migrations.RemoveField(
            model_name='robotti',
            name='location_x',
        ),
        migrations.RemoveField(
            model_name='robotti',
            name='location_y',
        ),
        migrations.AddConstraint(
            model_name='robotti',
            constraint=models.UniqueConstraint(
                fields=('modelname', 'serialnumber'),
                name='unique_robotti_model_serialnumber',
            ),
        ),
    ]
