# Generated by Django 4.0.4 on 2022-06-18 09:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_alter_user_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.CharField(default=uuid.UUID('8dfef99b-f3ba-441a-8ff5-d7ffb34ce619'), max_length=3000),
        ),
    ]
