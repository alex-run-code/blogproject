# Generated by Django 3.1.1 on 2020-09-28 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200928_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggedpost',
            name='content_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
