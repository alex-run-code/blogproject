# Generated by Django 3.1.1 on 2020-09-28 13:47

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0006_auto_20200928_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='blog.TaggedPost', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]