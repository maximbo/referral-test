# Generated by Django 5.1.3 on 2024-12-03 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activated_on', models.DateTimeField(null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('deleted_on', models.DateTimeField(db_index=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'купон',
                'verbose_name_plural': 'купоны',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('deleted_on', models.DateTimeField(db_index=True, null=True)),
            ],
            options={
                'verbose_name': 'отправленное приглашение',
                'verbose_name_plural': 'отправленные приглашения',
            },
        ),
    ]
