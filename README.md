
# WhatsApp Blaster

WhatsApp Blaster adalah program yang dibuat untuk memudahkan mengirim pesan secara masal dan terjadwal di project ini adalah WhatsApp Versi Basic 
jika ingin melihat review demo versi pro / berminat dengan versi pro dapat melihat video berikut [Review WhatsApp Versi Pro](https://www.youtube.com/watch?v=9rmdJhRukEA&ab_channel=Sandroputraa)

Versi pro di-host di repositori pribadi. Akses berbayar. akan mendapatkan dukungan dasar untuk instalasi, konfigurasi, dan penggunaan. tersedia request fitur yang lainya

Anda dapat menghubungi saya di [Telegram](https://t.me/Sandroputraaa) untuk detailnya.

## 📝 Fitur

| Fitur             | Tersedia | Jenis Versi |
| ----------------- | -------- | -------- |
| Realtime update user interface| ✅  | Semua Versi| 
| List Contact  | ✅  | Semua Versi |
| Support whatsapp multi beta  | ✅  | Semua Versi |
| Template Maker | ✅ | Versi Pro  |
| Kirim pesan dengan template | ✅ | Versi Pro  |
| Kirim pesan multi contact | ✅ |  Versi Pro  |
| Kirim pesan dengan data dari excel | ✅ | Versi Pro  |
| Penjadwalan Kirim Pesan | ✅ | Versi Pro  |
| Log Schedule / Pesan | ✅ | Versi Pro  |
| Database Setting | ✅ | Versi Pro  |


## 📚 Dibuat Dengan
#### ⚙ Backend
- [Python3](https://www.python.org/downloads/)
- [Flask](https://pypi.org/project/Flask/)
- [Flask-SocketIO](https://pypi.org/project/Flask-SocketIO/)
- [flask-paginate](https://pypi.org/project/flask-paginate/)
- [Flask-Login](https://pypi.org/project/Flask-Login/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [Selenium](https://pypi.org/project/selenium/)
- [Sqlite3](https://www.sqlite.org/index.html)

#### 🌈 Frontend
- [SoftUI](https://github.com/creativetimofficial/soft-ui-dashboard)
- [Sweetalert](https://sweetalert2.github.io/)
- [SocketIO](https://socket.io/)


## 🚀 Penggunaan

Untuk menggunakan Project ini terdapat dua cara , menggunakan file yang sudah di compile menjadi exe / menjalankan file main.py
- Sebelum menjalankan project pastikan sudah menginstall [JDK (Java Development Kit)](https://www.oracle.com/java/technologies/downloads/#jdk18-windows)

#### Git clone project & masuk ke folder project
```bash
  git clone https://github.com/sandrocods/WhatsappBlaster.git
  cd WhatsappBlaster
```

#### Menjalankan Selenium Server
```bash
  java -jar ./src/selenium-server.jar -timeout 99999999
```
![ss](https://i.ibb.co/Nsx2t3C/image.png)


#### Menjalankan File Exe
Klik dua kali file bernama WhatsApp Blaster Open Source.exe jika sudah muncul console seperti gambar dibawah maka sistem sudah berjalan

![ss](https://i.ibb.co/LtyWPzk/image.png)

Akan otomatis membuka browser dengan alamat tujuan http://localhost:5000/

#### Menjalankan File main.py
Perlu melakukan instalasi requirements sebelum menjalankan file main.py

```bash
  pip3 install -r ./requirements.txt
```
setelah semua module requirements terinstall baru menjalankan file main.py
```bash
  python3 main.py
```

![ss](https://i.ibb.co/5k2XvQH/image.png)

Akan otomatis membuka browser dengan alamat tujuan http://localhost:5000/


### Result 
![ss](https://s4.gifyu.com/images/ezgif-3-710f0c4227.gif)

#### Login mengunakan username : admin & password : admin

## Screenshots

#### Tampilan Dashboard ( sebelum terkoneksi whatsapp device )
![App Screenshot](https://i.ibb.co/mcKn9Kz/image.png)

#### Tampilan Dashboard ( Request QR code )
![App Screenshot](https://i.ibb.co/qJyy9tQ/image.png)

#### Tampilan Dashboard ( terkoneksi whatsapp device )
![ss](https://i.ibb.co/1mbr55d/image.png)

#### List Contact ( terkoneksi whatsapp device )
![ss](https://i.ibb.co/b237d3C/image.png)
