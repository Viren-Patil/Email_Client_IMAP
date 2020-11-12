# Email_Client_IMAP

## Team Members
      111803155 Viren Patil
      111803166 Rutvik Moharil

## Steps to setup your system to be able to run the code
      1) pip3 install tabulate
      * Run the following commands as sudoer
      2) apt-get install postfix
      3) apt-get install dovecot
      4) apt-get install -y mailutils
      5) postconf "home_mailbox = Maildir/"
      6) systemctl reload postfix
      7) systemctl status postfix (you should be able to see "active")
      8) apt install dovecot-imapd dovecot-core
      9) systemctl status dovecot (you should be able to see "active")
      10) cd /etc/dovecot/conf.d
      11) vi 10-mail.conf
      12) Comment the line --> mail_location = mbox:~/mail:INBOX=/var/mail/%u
      13) Uncomment the line --> mail_location = maildir:~/Maildir
      14) Save and exit from 10-mail.conf
      15) cd /etc/skel
      16) ls (You will see a Maildir, if not don't worry)
      17) rm -rf Maildir (if and only if it is present)
      18) mkdir -p Maildir/.Drafts Maildir/.Drafts/cur Maildir/.Drafts/new Maildir/.Drafts/tmp
      19) mkdir -p Maildir/.Sent Maildir/.Sent/cur Maildir/.Sent/new Maildir/.Sent/tmp
      20) mkdir -p Maildir/.Trash Maildir/.Trash/cur Maildir/.Trash/new Maildir/.Trash/tmp
      21) mkdir Maildir/cur Maildir/new Maildir/tmp
      22) chmod 700 -R Maildir/
      23) adduser --gecos "" <anyusername>
      24) Create a password of your choice
      25) Add one more such test user if you wish to (minimum should have 2 localhost users)
      26) su - <anyusername> (Note: <anyusername> should be an existing user)
      27) You should see a Maildir directory (if yes then we are good to go!)
      28) cd
      29) cd /etc/dovecot
      30) vi dovecot.conf
      31) Insert the line--> protocols = imap pop3
      32) cd ..
      33) cd postfix
      34) vi main.cf
      35) Make sure you have the following lines:
            * myhostname = <whatever hostname>
            * mydestination = $myhostname, <whatever hostname>, localhost.localdomain, localhost
            * mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
            * inet_interfaces = loopback-only
            * inet_protocols = all
            * home_mailbox = Maildir/
      36) We are good to go!

## Steps to run the code
      1) cd CN_Project
      2) Read through the config file and set it up accordinf to your preference
      3) Become a sudoer and check status of dovecot (it should be running)
      4) To check the status: systemctl status dovecot
      5) logout from sudoer and cd into CN_Project
      6) python3 client.py
      7) Enjoy the Email Client!
      8) Note: If you use the option 12 then make sure that whichever email-id you are using, turn on the Less secure app access
      9) You can turn it off later after using the email client is over.