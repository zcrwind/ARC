from django.db import models


# Create your models here.
class ArcUser(models.Model):
    sno = models.CharField(max_length=10, primary_key=True)  # 学号
    nickname = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    sex = models.CharField(max_length=4)
    dept = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)  # 联系方式
    email = models.EmailField(unique=True)
    totalbought = models.IntegerField()
    totalsell = models.IntegerField()


class unverified(models.Model):
    sno = models.ForeignKey(ArcUser, on_delete=models.CASCADE)


class book(models.Model):
    uuid = models.CharField(max_length=64, primary_key=True)
    bname = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quality = models.IntegerField()
    bimg = models.CharField(max_length=64)
    discp = models.CharField(max_length=200)
    bclass = models.CharField(max_length=20)


class own(models.Model):
    goods = models.ForeignKey(book, related_name='book_own', on_delete=models.CASCADE, primary_key=True)
    seller = models.ForeignKey(ArcUser, related_name='user_own', on_delete=models.CASCADE)


class trade(models.Model):
    goods = models.ForeignKey(book, related_name='trade_goods', on_delete=models.CASCADE, primary_key=True)
    seller = models.ForeignKey(ArcUser, related_name='whoSell', on_delete=models.CASCADE)
    buyer = models.ForeignKey(ArcUser, related_name='whoBuy', on_delete=models.CASCADE)
    statu = models.IntegerField()


class shoppingcart(models.Model):
    sno = models.ForeignKey(ArcUser, related_name='whocart', on_delete=models.CASCADE)
    goods = models.ForeignKey(book, related_name='wantgoods', on_delete=models.CASCADE)
