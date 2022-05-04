# Generated by Django 4.0.4 on 2022-05-03 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainlib', '0012_alter_userbook_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='book_image',
            field=models.ImageField(default='placceholder', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='books',
            name='book_author',
            field=models.CharField(max_length=200, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_cat',
            field=models.CharField(choices=[('Comic', 'Comic'), ('Fantasy', 'Fantasy'), ('Action', 'Action'), ('Thriller', 'Thriller'), ('Contemporary', 'Contemporary')], max_length=15, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_desc',
            field=models.CharField(max_length=200, verbose_name='About the Book'),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_pubd',
            field=models.DateField(verbose_name='Publication Date'),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
    ]