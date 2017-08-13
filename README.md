# Quipto - Qui(ckCry)pto

This checks if a OS environment varaible called QUIPTO_SALT exists, if not, generates a random secure salt and stores it in the temporary running environment variables. If a random salt is generated the decrypt function will only work in the current running session (unless the salt is stored permenantly as an OS env var).

It also checks if OS environment variable called QUIPTO_SECRET exisits, if not, same as above.

It uses the salt and secret (OS if they exist or random/user defined if not) throughout the program to encrypt/decrypt data.

Options...
----
- e - takes PT data and a secret and encrypts it with the salt, then outputs the CT data
- d - asks for the CT data and uses the secret and salt to decrypt and outputs the PT
- q - quits


Example 1
----
No stored SALT or SECRET
```sh
(venv) C:\quipto>py app.py
No salt found, generating salt
ENV SALT = b'\xeb\xfa\x90\xb6\x11\xc4c\xba'
No secret found...
Enter secret: *****
(e)ncrypt / (d)ecrypt / (q)uit?: e
Enter PT: super secret data
CT data is: '1u2PB7U2Hl6HT1NsNbIBeU53SbDmv4OCQByZyuXr+IKBN/T9bV1dYPf2vdWvwJNW'
(e)ncrypt / (d)ecrypt / (q)uit?: d
Enter CT: '1u2PB7U2Hl6HT1NsNbIBeU53SbDmv4OCQByZyuXr+IKBN/T9bV1dYPf2vdWvwJNW'
super secret data
```

Example 2
----
Stored SALT and SECRET env vars
```sh
(venv) C:\quipto>py app.py
Stored salt detected!
Stored secret detected!
(e)ncrypt / (d)ecrypt / (q)uit?: e
Enter PT: super secret data
CT data is: 'TPh1lCg8hizxBUuiPWgKbLaLk6hUFiufuYJ+bmuf+hvzQwzdMnHTXuUNPdUw4qdw'
(e)ncrypt / (d)ecrypt / (q)uit?: d
Enter CT: 'TPh1lCg8hizxBUuiPWgKbLaLk6hUFiufuYJ+bmuf+hvzQwzdMnHTXuUNPdUw4qdw'
super secret data
```

Encryption Logic...
----
- PT (+padding if required) -->
- encrypt with ciper (AES + key (which is PBKDF2 of secret & salt) + random IV) +
- IV =
- IV (stored as first block), CT

Decryption Logic...
----
- IV (taken from first block of IV, CT) taken off -->
- decrypt with cipher (AES + key (which is PBKDF2 of secret & salt) + known IV from start) -
- padding (if added at the start) =
- PT


License
----
MIT