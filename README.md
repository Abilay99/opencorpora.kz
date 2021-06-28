# Kazakh Open Source -- Development of a module for information and analytical data analysis of text resources and documents of the Kazakh language based on machine learning
* **System Requirements** 
  * OS: Linux, recommended distribution Ubuntu 20.04
  * Database: MySQL | MariaDB > 5.0 | 10.1 recommended MariaDB 10.3
  * Apertium: version > 3.6
  * CPU: core > 4; RAM > 8GB; recommended RAM > 16
  * GPU: intel hd graphics or minimal or minimal graphics accelerator
  * Interpreter: Python > 3.6.8
* **Installation**
  * Install MariaDB: https://downloads.mariadb.org/mariadb/10.3.30/ or using terminal command
    * $ sudo apt update
    * $ sudo apt install mariadb-server
  * Settings database
     * $ sudo mysql_secure_installation
     * Enter current password for root (enter for none): Press Enter
     * Set root password? [Y/n] Type N and then press ENTER
     * From there, you can press Y and then ENTER to accept the defaults for all the subsequent questions. 
     * $ sudo mariadb
     * MariaDB [(none)]> GRANT ALL ON *.* TO 'yourusername'@'localhost' IDENTIFIED BY 'Yourpassword123' WITH GRANT OPTION;
     * MariaDB [(none)]> FLUSH PRIVILEGES;
     * MariaDB [(none)]> exit
     * sudo systemctl status mariadb
      <br>. . .
      <br>Active: active (running)
      <br>. . .
     * $ mariadb -u yourusername -p
     * Enter password: Enter Yourpassword123 but you will not see it after typing press Enter
     * MariaDB [(none)]> CREATE DATABASE searchengine CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
     * MariaDB [(none)]> exit;
    * importing database
     * Global database for backup, link: https://disk.yandex.kz/d/0BpSWrp_N3gV7A downloading and paste to $HOME or /home/\<username\> directory and
      * $ cd $HOME
      * $ sed -i backup_20210613.sql -e 's/utf8mb4_unicode_ci/utf8mb4_general_ci/g'
      * $ sed -i backup_20210613.sql -e 's/utf8mb4_0900_ai_ci/utf8mb4_general_ci/g'
     * $ mysql -u yourusername -p searchengine < backup_20210613.sql
     * Enter your Yourpassword123 and wait to finish
  * apertium: use terminal:
      * $ mkdir $HOME/sources
      * $ cd $HOME/sources
      * $ wget http://apertium.projectjj.com/apt/install-nightly.sh
      * $ sudo bash install-nightly.sh
      * $ sudo apt-get -f install locales build-essential automake subversion pkg-config gawk libtool apertium-all-dev
      * Then execute all the commands on the link: https://wiki.apertium.org/wiki/Kazakh_and_Russian
  * Cloning project: use terminal:
      * $ cd $HOME
      * $ git clone https://github.com/Abilay99/opencorpora.kz.git
  * python packages: use terminal:
      * $ cd $HOME/opencorpora.kz
      * $ pip install -r requirements.txt 
* **Test**
  * Inserting *.txt files(only Kazakh lang.) to directory **testbasictexts** 
  * open terminal:
  * $ cd $HOME/opencorpora.kz/CorporaD
  * $ python3 zzgotoApertium.py
  * $ python3 zzgotoEditedApertium.py
  * $ python3 zzgotoouttext.py
  * $ python3 zzgototrain.py
  * $ python3 zzgotokeywordsplaintext.py
  * $ python3 zzgotoAbstracts.py
  * see directory testKeywords and testAbstracts
  * Change file CorporaDB.py line 18 user = "yourusername" and password = "Yourpassword123"
  * $ python3 interface0.0.1.py #(paste only kazakh lang.)
  * Change file CorporaDB.py line 18 user = "yourusername" and password = "Yourpassword123"
  * $ cd $HOME/opencorpora.kz
  * $ python3 manage.py makemigrations
  * $ python3 manage.py migrate
  * $ python3 manage.py createsuperuser #and enter yourname and password
  * $ python3 manage.py runserver
  * Open Web-browser and enter url http://127.0.0.1:8000/admin/ and click US flags next click Social applications next click Add Social applications and fill in all the fields for Google(https://console.cloud.google.com/ OAuth2 API) next click Save and add another for VK(https://vk.com/apps?act=manage). Then go to http://127.0.0.1:8000

