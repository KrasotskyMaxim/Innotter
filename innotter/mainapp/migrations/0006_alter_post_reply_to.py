# Generated by Django 4.0.6 on 2022-07-22 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_post_reply_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='mainapp.post'),
        ),
    ]
