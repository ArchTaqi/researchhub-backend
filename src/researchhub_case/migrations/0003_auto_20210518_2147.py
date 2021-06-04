# Generated by Django 2.2 on 2021-05-18 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub_case', '0002_auto_20210518_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorclaimcase',
            name='creator',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='created_cases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='authorclaimcase',
            name='requestor',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='requested_cases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='authorclaimcase',
            name='target_author',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='related_claim_cases', to='user.Author'),
        ),
    ]
