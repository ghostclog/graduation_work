# Generated by Django 4.1.4 on 2023-01-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_back', '0002_commentdata_postdata_teamuserdata_delete_findpeople_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('photo', models.ImageField(default='default.jpg', upload_to='media/profile')),
            ],
        ),
    ]
