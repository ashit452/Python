# Generated by Django 3.2.12 on 2022-06-21 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='language',
            fields=[
                ('title', models.CharField(max_length=50)),
                ('locale', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('icon', models.ImageField(upload_to='images/')),
                ('isDefault', models.BooleanField(default=False, verbose_name='Is Default')),
                ('status', models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=10)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
