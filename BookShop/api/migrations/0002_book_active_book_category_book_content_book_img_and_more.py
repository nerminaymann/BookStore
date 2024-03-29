# Generated by Django 4.1.2 on 2023-01-13 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('fantasy', 'Fantasy'), ('romance', 'Romance'), ('science_fiction', 'Science Fiction')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='img',
            field=models.ImageField(null=True, upload_to='photos/%y/%m/%d'),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
