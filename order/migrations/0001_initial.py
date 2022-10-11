# Generated by Django 4.1.2 on 2022-10-07 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderNum', models.BigAutoField(primary_key=True, serialize=False, verbose_name='주문번호')),
                ('userId', models.CharField(max_length=50, verbose_name='주문자 아이디')),
                ('getterName', models.CharField(max_length=50, verbose_name='받는 사람 이름')),
                ('getterAddress', models.CharField(max_length=500, verbose_name='받는 사람 주소')),
                ('getterDetailAddr', models.CharField(max_length=500, verbose_name='받는 사람 상세주소')),
                ('getterZonecode', models.CharField(max_length=10, verbose_name='받는 사람 우편번호')),
                ('getterTel', models.CharField(max_length=20, verbose_name='받는 사람 전화번호')),
                ('requirement', models.TextField(null=True, verbose_name='요구사항')),
                ('orderMsg', models.TextField(null=True, verbose_name='주문 메세지')),
                ('totalPrice', models.BigIntegerField(verbose_name='총액')),
                ('orderDate', models.DateTimeField(auto_now_add=True, verbose_name='주문날짜')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('orderDetailNum', models.BigAutoField(primary_key=True, serialize=False, verbose_name='주문상세번호')),
                ('prodNum', models.BigIntegerField(verbose_name='상품번호')),
                ('prodName', models.CharField(max_length=1000, verbose_name='상품명')),
                ('prodThumbnail', models.CharField(max_length=1000, verbose_name='썸네일')),
                ('prodPrice', models.BigIntegerField(verbose_name='상품 가격')),
                ('buyCount', models.IntegerField(verbose_name='구매 수량')),
                ('prodTotal', models.IntegerField(verbose_name='구매 금액')),
                ('is_refunded', models.BooleanField(default=0, verbose_name='반품/환불/교환 여부')),
                ('orderNum', models.ForeignKey(db_column='orderNum', on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]
