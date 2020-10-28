# Email_Client_IMAP

python3 client.py

Some guidelines regarding the usage of commands:

1. Commands valid in any state are - 
      CAPABILITY      NOOP    LOGOUT

2. Commands valid in non-authenticated state are - 
      LOGIN
     
3.  Commands valid in authenticated state are -
      SELECT    EXAMINE   CREATE    DELETE    RENAME    STATUS
 
4. Commands valid in selected state are - 
      CHECK     CLOSE     EXPUNGE   READ     COPY
