# Generated by Django 2.2.12 on 2020-05-27 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0056_remove_paper_external_source_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='figure',
            name='created_location',
            field=models.CharField(blank=True, choices=[('PROGRESS', 'Progress')], default=None, max_length=255, null=True),
        ),
    ]
