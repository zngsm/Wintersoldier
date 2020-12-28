# Generated by Django 3.1.4 on 2020-12-27 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('schedule_year', models.IntegerField()),
                ('schedule_month', models.IntegerField()),
                ('schedule_date', models.IntegerField()),
                ('schedule_hour', models.IntegerField()),
                ('schedule_min', models.IntegerField()),
                ('alarm_year', models.IntegerField()),
                ('alarm_month', models.IntegerField()),
                ('alarm_date', models.IntegerField()),
                ('alarm_hour', models.IntegerField()),
                ('alarm_min', models.IntegerField()),
                ('completed', models.CharField(default='no', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_todo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
