# Generated by Django 3.0.3 on 2020-04-03 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WAD2app', '0002_auto_20200403_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlife',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_life', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='/static/profileImg', null=True, upload_to='profileImages'),
        ),
    ]