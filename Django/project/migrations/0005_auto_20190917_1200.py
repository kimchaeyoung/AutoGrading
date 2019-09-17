# Generated by Django 2.2.1 on 2019-09-17 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_homework_student_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hwname', models.CharField(max_length=200)),
                ('madeby', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Homeworks',
        ),
        migrations.RemoveField(
            model_name='homework_student',
            name='homework_name',
        ),
        migrations.AlterField(
            model_name='homework_student',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Homework'),
        ),
        migrations.AlterField(
            model_name='homework_student',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Student'),
        ),
    ]
