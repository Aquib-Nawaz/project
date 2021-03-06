# Generated by Django 3.1.2 on 2020-10-25 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0003_auto_20201025_0746'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='class',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='class',
            name='student',
        ),
        migrations.RemoveField(
            model_name='class',
            name='teaching_assistant',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='NONE', max_length=255),
        ),
        migrations.DeleteModel(
            name='People',
        ),
        migrations.AddField(
            model_name='classes',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teach_classes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classes',
            name='students',
            field=models.ManyToManyField(related_name='in_classes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classes',
            name='teaching_assistant',
            field=models.ManyToManyField(related_name='assist_classes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='class_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='class_notification', to='Dashboard.classes'),
        ),
        migrations.DeleteModel(
            name='Class',
        ),
    ]
