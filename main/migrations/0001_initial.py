# Generated by Django 5.0.3 on 2024-03-31 12:52

import django.contrib.auth.models
import django.db.models.deletion
import main.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('openai_key', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='', max_length=500)),
                ('answer', models.IntegerField(default=0)),
                ('options', models.ManyToManyField(blank=True, to='main.option')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(default='', max_length=100)),
                ('level', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Easy', max_length=20)),
                ('description', models.TextField(default='General knowledge', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('number_questions', models.IntegerField(default=0)),
                ('author', models.ForeignKey(default=main.models.ExtendedUser, on_delete=django.db.models.deletion.CASCADE, to='main.extendeduser')),
                ('questions', models.ManyToManyField(blank=True, to='main.question')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_questions', models.IntegerField(default=0)),
                ('questions_answered', models.IntegerField(default=0)),
                ('details', models.JSONField(blank=True, default={'data': []}, null=True)),
                ('passed', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(default=main.models.Quiz, on_delete=django.db.models.deletion.CASCADE, to='main.quiz')),
                ('user', models.ForeignKey(default=main.models.ExtendedUser, on_delete=django.db.models.deletion.CASCADE, to='main.extendeduser')),
            ],
        ),
    ]
