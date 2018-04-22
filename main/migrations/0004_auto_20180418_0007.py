# Generated by Django 2.0 on 2018-04-17 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180417_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionAPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api', models.TextField()),
                ('permission', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SuspiciousAPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='extract',
            unique_together={('apk', 'feature')},
        ),
        migrations.AlterUniqueTogether(
            name='permissionapi',
            unique_together={('api', 'permission')},
        ),
    ]