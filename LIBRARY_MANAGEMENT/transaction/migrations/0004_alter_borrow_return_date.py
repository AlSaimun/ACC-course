# Generated by Django 4.2.3 on 2023-07-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_alter_borrow_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
