# Generated by Django 4.1.2 on 2022-10-11 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cartNum', models.BigAutoField(primary_key=True, serialize=False, verbose_name='장바구니 번호')),
                ('buyCount', models.IntegerField(verbose_name='선택한 상품의 수량')),
                ('prodNum', models.ForeignKey(db_column='prodNum', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('userId', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.CASCADE, to='member.member')),
            ],
        ),
    ]
