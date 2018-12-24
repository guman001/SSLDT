# SSLDT
Sign/Verify and Send/Receive Large Dictionaries via TCP socket (= SSLDT)

The following needs in a project led me to write this class and share it:
1) Digitally sign a Python dictionary
2) Send a large signed dictionary via TCP socket

How dictionary is signed and verified? 

Dictionary is ordered by keys alphabetically. The ordered dictionary is converted to json dictionary. Then the string is digitally signed. Signature is encoded by Base64 and added to "signature" key of the original dictionary.
On receiving, the received message is dumped and "signature" key is omitted. After that, dictionary is ordered by keys alphabetiacally and converted to json string. Now, message is ready for verification.

How large dictionary is sent and received?
