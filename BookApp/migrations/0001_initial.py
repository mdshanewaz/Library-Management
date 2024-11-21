# Generated by Django 5.0 on 2024-11-19 13:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('writer', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Story', 'Story'), ('SciFi', 'SciFi'), ('History', 'History'), ('Documentary', 'Documentary'), ('Comic', 'Comic'), ('Nobel', 'Nobel'), ('Religious', 'Religious'), ('Academic', 'Academic')], max_length=100)),
                ('amount', models.PositiveIntegerField()),
                ('added_to_library', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]