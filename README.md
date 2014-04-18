==============
Carpooling App
==============

This is a project that I started with a friend, than in a week we changed our mind and abandon the project. Here is the work so far, and I am willing to continue as an open source project if there's anyone to help me. 

Take a look at `design` folder and my initial class diagram. Rest api is implemented as well. 

What is the App
===============

Carpooling app will be a mobile app to share rides with fellow drivers. The goal is to make commuters life easier, as well as helping inter-city travelers.

App Pages
=========

Application consists of following pages

 * [[Request a ride]]
 * [[Select a ride]]
 * [[Create a ride]]
 * [[Ride Details]]
 * [[My rides]]
 * [[User profile]]
 * [[Notifications]]
 * [[Accept/Reject a ride request]]

In addition, there are some simple pages as follows:

 * Help
 * About Us
 * [[Contact Us]]

Use Cases
=========

Sorry, use-cases are in Turkish.

Data Dictionary (For use-cases)
-------------------------------

Term|Description
----|-----------
Yolculuk/Ride|A’dan B’ye olan yolculuk.
Sofor/Driver|araci olan kullanici
Yolcu/Passenger| araci olmayan kullanici
Rating|2 tip rating var. 1.cisi kullanicilarin 5 uzerinden verdigi rating. 2.cisi sistemin kullanicilarin sozunde durup durmadigini hesaplayan 100 uzerinden verilen rating. 100: guvenilir. 0: guvenilmez.
Verified User| En az bir basarili yolculuk yapmis kullanici.

Use Case 1: Sofor Yolculuk Yaratiyor
------------------------------------

**Aciklama**: Sofor yolculuk yaratiyor

**Roller**: Sofor, Sistem

**Flow of events**:
 * Sofor “Yolculuk yarat” ekranini aciyor.
 	* Harita uzerinde baslangic nokrasi seciyor.
 	* Harita uzerinde baslangic noktasinin yaricapini belirliyor. Bu yaricap yolculari alabilecegi alani gosteriyor.
 * Harita uzerinde bitis noktasi seciyor.
 	* Harita uzerinde yari capi belirliyor. Bu yaricap yolculari birakabilecegi maksimum uzakligi belirliyor (detour).
 * Tarih ve zaman seciyor.
 	* Tarih tek bir zaman olabilir (12 aralik 13:00 gibi)
 	* Tarih tekrar edebilir (h.ici her gun 08:30 gibi)
 * Arac ozelliklerini seciyor
 	* Marka
 	* Model
 	* Resim (opsiyonel)
 * Kac kisiyi alabilecegini seciyor (aracin kapasitesine gore secenekler cikacak.)
 * Yolculuk icin istedigi ucreti belirliyor
 	* Sistem Ucret icin km’ye gore max ve min degerleri gosteriyor.
 * “Yolculuk Yarat” dugmesine dokunuyor.
 * Sistem yolculugu kaydedip, sofore soyle bir mesaj gosteriyor: “Sisteme yolculuk kaydiniz alindi. Talep gelince size haber verecegiz”.
 * Sistem soforu baska bir sayfaya yonlendiriyor.

Use Case 2: Yolcu yolculuk aramasi yapiyor
------------------------------------------

**Aciklama**: Yolcu yolculuk aramasi yapiyor

**Roller**: Yolcu, Sistem

**Flow of events**:
 * Yolcu “Yolculuk Arama” ekranini aciyor.
 * Harita uzerinden baslangic noktasi (araca binmek istedigi nokta) seciyor.
 * Harita uzerinden bitis noktasi (inmek istedigi nokta) seciyor.
 * Yolculuk zamanini seciyor.
 	* Zaman tek bir tarih olabilir (12 haziran 12:00 gibi).
 	* Zaman tekrar eden bir tarih olabilir (h.ici hergun 08:30 gibi).
 * “Devam Et” dugmesine dokunuyor.
 * Sistem istenen rotadaki yolculuklari sunucudan cekiyor.
 * Sistem yapilan aramayi kaydediyor. Kriterlere uyan yeni yolculuk ilani girilmesi durumunda sistem bu yolcuya notification gonderiyor.
 * Sistem yolcuyu “Yolculuk Sec” ekranina yonlendiriyor.

Use Case 3: Sofor ve yolcu yolculugu tamamliyor
-----------------------------------------------

**Aciklama**: Sofor yolculugu tamamliyor

**Roller**: Sofor, Yolcu, Sistem

**Pre conditions**:
 * Sofor yolculuk olusturdu, listeledi
 * Yolcu(lar) yolculuga kayit oldu.

**Flow of events**:
 * Sistem, sofore yolcu kayitlarini gonderiyor. push notification ile.
 * Sofor yolculari kabul ediyor.
 * Yolculara kabul edildikleri gonderiliyor.
 * Sistem yolculardan ucretleri tahsil ediyor. Kredi kartlarinda yolculuk ucretini acik provizyona aliyor (ucreti kilitliyor).
 * Yolculuk zamani gelince sofor yolcuyu yoldan aliyor ve varis noktasina birakiyor.
 * Yolculuk sonunda sistem hem sofore hem de yolculara zorunlu olarak “Yolculugu onayla” ekranini cikartiyor. Onay verilmeden uygulama baska hicbir sayfa gostermiyor. Sistem bu ekrani gosterecegini yolculuk zamanindan otomatik olarak anliyor. 
 * Sofor “Basarili” onay veriyor.
 * Sistem sofore opsiyonel “Rating” ekranini gosteriyor.
  * Rating ekraninda yolculuga 5 uzerinden puan veriyor.
  * Yolculuga katilanlar hakkinda yorum yapilabliyor.
 * Sistem yolcularin provizyonunu onayliyor (parayi cekiyor).
 * Sistem yolculuga katilanlari “Verified User” haline getiriyor. (yolculuk basarili oldugu icin)

**Yolculuk Basarisiz Oluyor**:
 * Yolculuk sonunda, yolcu ya da sofor “Onay ekrani”nda, yolculugu “Basarisiz” olarak isaretliyor.
 * Sistem yolculuga katilan herkese yolculugun basarisiz olma sebebini yazabilecegi “Basarisiz Yolculuk” ekrani cikartiyor.
 * Yolcu ve sofor bu sayfada basarisizlik sebebini yaziyor. 
 * Sistem yolcular parayi iade ediyor. 

Use Case 4: Sofor yolcuyu onayliyor
-----------------------------------

**Aciklama**: Sofor yolcuyu onayliyor

**Roller**: Sofor, Yolcu, Sistem

**Pre conditions**:
 * Sofor yolculuk olusturdu, listeledi
 * Yolcu(lar) yolculuga kayit oldu.

**Flow of events**:
 * Sistem sofore, yolcularin kayit oldugu anda, push notification gonderiyor.
 * Sofor accept/reject ekranina gelip, pending durumundaki istekleri gosteriyor.
 * Isteklerin herhangi birine girdiginde, o kullanicinin profilini goruyor. Profilde asagidaki ozellikleri goruyor:
 	* Kullanicinin eski yolculuklari
 	* Kullanicinin reviewlar
 	* Kullanicinin biosu
 * Yolculugu onaylama linki
 * Sofor yolcuyu onayliyor.
 * Yolcuya onayin gerceklestigine dair bir push notification gidiyor.

**Onay vermeme durumu**:
 * Yolcuya onay verilmedigi mesaji gidiyor.
 * Cekilen Provizyon iptal ediliyor.

Use Case 5: Yolcu yolculuga kaydoluyor
--------------------------------------

**Aciklama**: Yolcu yolculuga kaydoluyor

**Roller**: Yolcu, Sistem

**Pre conditions**: 
 * Use Case #2
 * Yolcu yolculuk aramasi gerceklestirdi
 * Sistem aranan kriterlerde birden fazla yolculuk buldu ve “Yolculuk sec” ekranini acti.

**Flow of events**:
 * Sistem yolculuklari listeledi. 
 * Yolcu, listeden bir yolculuk secti
 * Sistem, “yolculuk detay” ekranini acti.
 * Yolcu detaylari inceledi ve “Book it now” butonuna dokundu.
 * Yolcu “Book it now” ekranindan kredi karti ile odeme yapti.
 * Sistem odemeyi bankanin provizyonuna aldi.
 * Sistem yolcuyu, yolculuk detayina ekledi. Baska bir yolcu, bu detay sayfasina girdiginde, bu yolcuyu gorebilecek.
 * Sistem sofore, yolcuyu onaylamasi icin bir notification gonderdi.

Use Case 6: Sofor yolculugu iptal ediyor
----------------------------------------

TODO

Use Case 7: Sofor yolculuk ilanini duzenliyor
---------------------------------------------

TODO

Class Diagram
=============

This is how model layer look.

![Class Diagram](https://raw.githubusercontent.com/laplacesdemon/carpooling-app/master/design/ClassDiagram.png)

Rest API
========

The REST api is the data endpoint of mobile apps.

GET Rides Service
-----------------

Returns ride objects for specified parameters. If no parameter is passed, returns all rides with pagination.

A ride object is a brief description of the ride. If you want to see details of it, use [[Ride Detail Service]]

**Endpoint**

/api/rides

**Parameters**

Name|Description|Example
----|-----------|-------
start_latitude|Latitude coordinates for the start location (in decimals)|42.3434
start_longitude|Longitude coordinates for the start location (in decimals)|42.3434
start_radius|Radius of the start location's circle (in meters)|1000
end_latitude|Latitude coordinates for the destination (in decimals)|42.3434
end_longitude|Longitude coordinates for the destination location (in decimals)|42.3434
end_radius|Radius of the destination location's circle (in meters)|1000
date|The date and time of the ride.|2013-12-25T14:53:05Z
until|Optional date to fetch results until specified date.|2013-12-25T14:53:05Z

**Example Response**

		[
		    {
		        "pk": 1, 
		        "route": {
		            "start_address": "Hac\u0131 \u015e\u00fckr\u00fc Sk 1-19, Kadikoy, Turkey", 
		            "end_address": "Cicek Pasaji, Beyoglu, Turkey"
		        }, 
		        "driver": {
		            "url": "/api/users/2/", 
		            "username": "ahmet", 
		            "public_name": "Ahmet K."
		        }, 
		        "vehicle": {
		            "url": "/api/vehicles/1/", 
		            "brand": "BMW", 
		            "model": "3.16i", 
		            "year": 2001, 
		            "seat_capacity": 3
		        }, 
		        "registered_seats": "0/2", 
		        "price": 40, 
		        "date": "2013-12-25T13:32:05Z"
		    }
		]

Ride Detail Service
===================

Returns the details of a ride.

**Endpoint**

/api/rides/{ride_id}

**Parameters**

No parameters.

**Response**

Object Name|Description
-----------|-----------
route|Route object
schadule|An object for detailed schedule of the ride
driver|Driver object
offerred_seats|The number of seats that is available for this ride. It is different than the vehicle capacity
state|PENDING|SUCCESS|FAILED|FAILED_WITH_PROBLEMS
passengers|An array of user id's who are registered passengers for this ride

Ride Insert/Update Service
==========================

**Endpoint**

/api/rides

**Parameters**

Name|Description
----|-----------
route|Route object
schedule|Schedule object
vehicle|Vehicle object
offerred_seats|Offerred seats
price|Price
