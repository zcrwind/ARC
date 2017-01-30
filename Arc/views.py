from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.template import loader
from .models import *
from PIL import Image
import uuid

areaname = '127.0.0.1:8000'


# Create your views here.

def register(req):
    referrer = req.META.get('HTTP_REFERER')
    if referrer != 'http://' + areaname + '/Arc/login/register.html':
        return render_to_response('register.html')
    else:
        sno = req.POST.get('sno', '')
        email = req.POST.get('email', '')
        passwd = req.POST.get('passwd', '')
        dept = req.POST.get('dept', '')
        nickname = req.POST.get('nickname', '')
        sex = req.POST.get('sex', '')
        phone = req.POST.get('phone', '')
        try:
            ArcUser.objects.create(sno=sno, passwd=passwd,
                                   dept=dept, email=email,
                                   nickname=nickname, sex=sex,
                                   phone=phone, totalsell=0,
                                   totalbought=0)
            req.session['authen'] = sno
            return HttpResponseRedirect('/Arc/index')
        except IntegrityError:
            error = '学号或邮箱已被注册'
            return render_to_response('register.html', locals())


def login(req):
    sno = req.POST.get('sno', '')
    passwd = req.POST.get('passwd', '')
    if sno and passwd:
        try:
            ArcUser.objects.get(sno=sno, passwd=passwd)
            req.session['authen'] = sno
            return HttpResponseRedirect('/Arc/index')
        except ObjectDoesNotExist:
            try:
                ArcUser.objects.get(sno=sno)
                error = '密码错误'
            except ObjectDoesNotExist:
                error = '用户不存在'
            finally:
                return render_to_response('login.html', locals())
        finally:
            pass
    else:
        return render_to_response('login.html', locals())


def upload(req):
    # referrer = req.META.get('HTTP_REFERER')
    # if referrer != 'http://' + areaname + '/Arc/manage.html':
    #     return HttpResponse(referrer)
    sno = req.session.get('authen')
    bname = req.POST.get('bname', '')
    author = req.POST.get('author', '')
    publisher = req.POST.get('publisher', '')
    price = req.POST.get('price', '')
    quality = req.POST.get('quality', '')
    bclass = req.POST.get('bclass', '')
    discp = req.POST.get('discp', '')
    bimg = req.FILES.get('bimg', '')
    if bname and price:
        if bimg:
            imgid = uuid.uuid1()
            img = Image.open(bimg)
            img.thumbnail((500, 500), Image.ANTIALIAS)
            img.save('Arc/static/source/' + str(imgid) + '.png', 'png')
            bimg = '/static/source/' + str(imgid) + '.png'
        else:
            bimg = '/static/source/default.png'

        try:
            bookid = uuid.uuid1()
            book.objects.create(uuid=str(bookid), bname=bname, author=author, price=price,
                                publisher=publisher, quality=quality, bclass=bclass,
                                discp=discp, bimg=bimg)
            # 写own表
            own.objects.create(goods=book.objects.get(uuid=str(bookid)),
                               seller=ArcUser.objects.get(sno=sno))
            req.session['upload'] = '上传成功'
            return HttpResponseRedirect('/Arc/manage')
        except IntegrityError:
            req.session['upload'] = '由于某种神秘原因上传失败了！'
            return HttpResponseRedirect('/Arc/manage')
    else:
        req.session['upload'] = '存在必要字段[书名]或[价格]没有填写！'
        return HttpResponseRedirect('/Arc/manage')


def index(req):
    ob = own.objects.all()
    books = []
    for o in ob:
        nob = book.objects.filter(uuid=o.goods.uuid)
        for a in nob:
            books.append(a)
    authen = req.session.get('authen')
    return render_to_response('index.html', locals())


def logout(req):
    del req.session['authen']
    return HttpResponseRedirect('/Arc/index')


def manage(req):
    referrer = req.META.get('HTTP_REFERER')
    if referrer == 'http://' + areaname + '/Arc/upload' or referrer == 'http://' + areaname + '/Arc/upload.html':
        upload_tips = req.session['upload']
        del req.session['upload']
    authen = req.session.get('authen')
    user = ArcUser.objects.get(sno=authen)
    uploaded = book.objects.filter(Q(book_own__seller__sno=authen) | Q(trade_goods__seller__sno=authen))
    order = book.objects.filter(trade_goods__buyer__sno=authen)
    for record in order:
        record.statu=trade.objects.get(goods__uuid=record.uuid).statu
        record.seller = trade.objects.get(goods__uuid=record.uuid).seller.nickname
    shoppingcart = book.objects.filter(wantgoods__sno__sno=authen)
    for record in shoppingcart:
        record.seller = own.objects.get(goods__uuid=record.uuid).seller.nickname
    return render_to_response('manage.html', locals())


def function(req):
    authen = req.session.get('authen')
    return render_to_response('function.html', locals())


def detail(req, uuid):
    authen = req.session.get('authen')
    thebook = book.objects.get(uuid=uuid)
    thebook.seller = thebook.book_own.get().seller.nickname
    return render_to_response('detailInfo.html', locals())


def addtoorder(req, uuid):
    authen = req.session.get('authen')
    thebook = book.objects.get(uuid=uuid)
    trade.objects.create(goods=book.objects.get(uuid=uuid),
                         seller=thebook.book_own.get().seller,
                         buyer=ArcUser.objects.get(sno=authen),
                         statu=0)
    own.objects.get(goods=book.objects.get(uuid=uuid)).delete()
    referrer = req.META.get('HTTP_REFERER')
    if referrer == 'http://' + areaname + '/Arc/manage':
        shoppingcart.objects.get(goods__uuid=uuid).delete()
    return HttpResponseRedirect('/Arc/manage')


def addtoshoppingcart(req, uuid):
    authen = req.session.get('authen')
    try:
        shoppingcart.objects.get(goods=book.objects.get(uuid=uuid),
                                 sno=ArcUser.objects.get(sno=authen))
    except ObjectDoesNotExist:
        shoppingcart.objects.create(goods=book.objects.get(uuid=uuid),
                                    sno=ArcUser.objects.get(sno=authen))
    return HttpResponseRedirect('/Arc/detail/uuid=' + uuid)


def delbook(req, uuid):
    authen = req.session.get('authen')
    willdelete = book.objects.get(uuid=uuid)
    if book.objects.get(uuid=uuid).trade_goods.get().buyer.sno != authen:
        return HttpResponse('身份验证失败')
    if book.objects.get(uuid=uuid).trade_goods.get().statu == 1:
        return HttpResponse('订单已经完成，不能取消')
    try:
        own.objects.create(goods=book.objects.get(uuid=uuid),
                           seller=ArcUser.objects.get(whoSell__goods__uuid=uuid))
        trade.objects.get(goods=book.objects.get(uuid=uuid)).delete()
        return HttpResponseRedirect('/Arc/manage')
    except:
        return HttpResponse('出现了异常请联系系统管理员')


def makesureorder(req, uuid):
    authen = req.session.get('authen')
    if book.objects.get(uuid=uuid).trade_goods.get().buyer.sno != authen:
        return HttpResponse('身份验证失败')
    t = trade.objects.get(goods__uuid=uuid)
    t.statu = 1
    t.save()
    return HttpResponseRedirect('/Arc/manage')

def query(req,queryclass):
    ob = own.objects.filter(goods__bclass=queryclass)
    books = []
    for o in ob:
        nob = book.objects.filter(uuid=o.goods.uuid)
        for a in nob:
            books.append(a)
    authen = req.session.get('authen')
    return render_to_response('index.html', locals())


def delshoppingcart(req,uuid):
    authen = req.session.get('authen')
    if book.objects.get(uuid=uuid).wantgoods.get().sno.sno != authen:
        return HttpResponse('身份验证失败')
    try:
        shoppingcart.objects.get(sno=authen,goods=book.objects.get(uuid=uuid)).delete()
        return HttpResponseRedirect('/Arc/manage')
    except ObjectDoesNotExist:
        #因为机制保证，这里理论上不会出现异常
        pass