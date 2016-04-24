#Walang
##Apa ini
Walang adalah skrip dalam bahasa python untuk memonitor mailbox email di server. Skrip ini dikembangkan dalam lingkungan raspberry pi. Notifikasi berupa nyala lampu led berpola, jika ada email yang belum dibaca.
##Bagaimana cara kerjanya?
- Sebuah daemon selalu membaca status file data yang ada di /tmp/led.db
- Jika ada modifikasi terhadap file, file akan dibaca. Dari data ini akan didapatkan lampu led mana yang akan dinyalakan. Demikian juga polanya. Saat ini ditentukan ada 3 pola: normal, new, alarm. Masing-masing didefinisikan menggunakan 'kode morse', berupa 'titik' dan 'garis'.
- Sebuah daemon lagi akan memantau akun email. jika ada email perubahan pada mailbox yang dimonitor, maka daemon akan mengupdate file data di /tmp/led.db
##Bagaimana menjalankannya?
```
$ git clone https://github.com/guspri/walang.git
$ cd walang
```
edit file walang.py, sesuaikan informasi berikut:
```
HOSTNAME = 'mail.server.dom'
USERNAME = 'account@server.dom'
PASSWORD = 'password'
MAILBOX = 'Inbox'
```
kemudian jalankan dengan perintah,
```
$ ./walang.py
$ ./walang-display.py
```

Untuk mempermudah kedua skript diatas bisa disalin ke direktori /usr/loca/bin.

```
$ sudo cp walang.py /usr/local/bin
$ sudo cp walang-display.py /usr/local/bin
```

##Menjalankan Walang dengan *systemd*
Untuk menjalankan service walang melalui systemd salin file walang.service dan walang-display.service ke direktori /etc/systemd/system

```
$ sudo cp walang.service /etc/systemd/system
$ sudo cp walang-display.service /etc/systemd/system
```
Jalankan dengan perintah:
```
$ sudo systemctl start walang
$ sudo systemctl start walang-display
```
##Hardware

![GPIO Raspberry Pi 2](/images/GPIO_Pi2.png)
![Rangkaian LED 1 Sederhana Satu Lampu](/images/simplecircuit.jpg)
- Katoda LED dihubungkan ke pin 14 Raspberry Pi
- Anoda LED disisipkan resistor pembatas arus 220Ohm atau 100Ohm. Dihubungkan ke pin 12 GPIO Raspberry Pi.

Selamat mencoba.
