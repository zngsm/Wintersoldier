# Generated by Django 3.1.4 on 2021-01-04 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_grouptodo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GroupTodo',
        ),
    ]