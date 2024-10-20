# Generated by Django 5.1.2 on 2024-10-19 23:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_mediatype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Full title of the media.', max_length=255)),
                ('authors', models.CharField(blank=True, help_text='Authors of the media (optional).', max_length=255, null=True)),
                ('media_number', models.CharField(help_text="Unique media number (e.g., T001 for category 'T').", max_length=10, unique=True)),
                ('isbn13', models.CharField(blank=True, help_text='ISBN13 number (optional).', max_length=13, null=True)),
                ('acquisition_date', models.DateField(blank=True, help_text='Acquisition date of the media (optional).', null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, help_text='Price of the media (optional).', max_digits=10, null=True)),
                ('left_library_date', models.DateField(blank=True, help_text='Date when the media left the library (optional).', null=True)),
                ('comments', models.TextField(blank=True, help_text='Additional comments (optional).', null=True)),
                ('publisher', models.CharField(blank=True, help_text='Publisher of the media (optional).', max_length=255, null=True)),
                ('publishing_date', models.DateField(blank=True, help_text='Publishing date of the media (optional).', null=True)),
                ('short_description', models.TextField(blank=True, help_text='Short description of the media (optional).', null=True)),
                ('media_file', models.FileField(blank=True, help_text='Reference to uploaded media (optional).', null=True, upload_to='media_files/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(help_text='Media category (e.g., Fiction, Science).', on_delete=django.db.models.deletion.CASCADE, to='inventory.mediacategory')),
                ('created_by', models.ForeignKey(blank=True, help_text='User who created this media.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media_created', to=settings.AUTH_USER_MODEL)),
                ('media_type', models.ForeignKey(help_text='Type of media (e.g., Book, Game, Music CD).', on_delete=django.db.models.deletion.CASCADE, to='inventory.mediatype')),
                ('site', models.ForeignKey(help_text='Library site where this media is stored.', on_delete=django.db.models.deletion.CASCADE, to='inventory.librarysite')),
                ('updated_by', models.ForeignKey(blank=True, help_text='User who last updated this media.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
                'ordering': ['media_number'],
            },
        ),
    ]
