import requests

postUrl='http://panel.vatansms.com/panel/smsgonder1Npost.php'
musteriNo='39944'
kullaniciAdi='905350274019'
sifre='190wud40'
orjinator="SMS TEST"

tur='Normal' """ Normal yada Turkce """
zaman=''

mesaj='Bu bir test mesajidir GTU.'
numara1='05350274019'

string = """
<sms>
    <kno>"""+musteriNo+"""</kno>
    <kulad>"""+kullaniciAdi+"""</kulad>
    <sifre>"""+sifre+"""</sifre>
    <gonderen>"""+orjinator+"""</gonderen>
    <mesaj>"""+mesaj+"""</mesaj>
    <numaralar>"""+numara1+"""</numaralar>
    <tur>"""+tur+"""</tur>
</sms>
"""

""" Xml içinde aşağıdaki alanlarıda gönderebilirsiniz.
<zaman>2014-04-07 10:00:00</zaman> İleri tarih için kullanabilirsiniz """

response =  requests.post(postUrl, data={"data":string})

print(response.text)