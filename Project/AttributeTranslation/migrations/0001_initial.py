# Generated by Django 3.2.12 on 2022-05-27 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Attribute', '0001_initial'),
        ('Language', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='attributeTranslation',
            fields=[
                ('attributeTranslationId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.attribute')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Language.language')),
            ],
        ),
    ]
