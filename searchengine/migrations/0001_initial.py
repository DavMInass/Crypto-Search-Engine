# Generated by Django 4.1.7 on 2023-02-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_no', models.IntegerField(db_index=True)),
                ('text', models.TextField()),
            ],
        ),
    ]
