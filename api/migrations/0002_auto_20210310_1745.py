# Generated by Django 3.1.7 on 2021-03-10 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=100)),
                ('education', models.CharField(max_length=100)),
                ('biography', models.TextField()),
                ('avatar', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='authors', to='api.Author'),
        ),
    ]
