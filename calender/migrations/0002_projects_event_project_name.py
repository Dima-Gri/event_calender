# Generated by Django 4.1.3 on 2023-04-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=150)),
                ('manager', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='project_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
