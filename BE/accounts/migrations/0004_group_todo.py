# Generated by Django 3.1.4 on 2021-01-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
        ('accounts', '0003_group_inviting'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='todo',
            field=models.ManyToManyField(related_name='group_Todo', to='todos.Todo'),
        ),
    ]
