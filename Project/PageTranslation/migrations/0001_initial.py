# Generated by Django 3.2.12 on 2022-05-23 09:57

import PageTranslation.models
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Language', '0001_initial'),
        ('Page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pageTranslation',
            fields=[
                ('contentId', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', tinymce.models.HTMLField()),
                ('language', models.ForeignKey(default=PageTranslation.models.get_language, on_delete=django.db.models.deletion.CASCADE, to='Language.language')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Page.page')),
            ],
            options={
                'verbose_name': 'Page Translation',
                'unique_together': {('language', 'page')},
            },
        ),
    ]
