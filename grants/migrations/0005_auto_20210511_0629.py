# Generated by Django 3.2.2 on 2021-05-11 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0004_auto_20210510_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('status', models.IntegerField(choices=[(100, 'New'), (200, 'Active'), (300, 'Paused'), (400, 'Inactive')])),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='user',
        ),
        migrations.AlterField(
            model_name='application',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grants.company'),
        ),
        migrations.AlterField(
            model_name='applicationanswer',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grants.application'),
        ),
        migrations.AlterField(
            model_name='applicationanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grants.applicationquestion'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grants.application'),
        ),
        migrations.AlterField(
            model_name='reviewanswer',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grants.assignment'),
        ),
        migrations.AlterField(
            model_name='reviewanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grants.reviewquestion'),
        ),
        migrations.DeleteModel(
            name='UserStatus',
        ),
        migrations.AddField(
            model_name='assignment',
            name='reviewer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='grants.reviewer'),
            preserve_default=False,
        ),
    ]
