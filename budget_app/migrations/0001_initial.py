# Generated by Django 4.0.3 on 2022-03-17 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=30)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_app.category')),
            ],
        ),
    ]
