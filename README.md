# blogabetWatcher

blogabet.com is a social network where you can find bet tips and follow paid and free tipster to see their picks.

blogabetWatcher is a simple tool to help you follow live picks from tipsters you are following. That's why you need to be registered 
in blogabet.com.

###	Setup
The first step is to download or clone locally this repository. For that, open a terminal or PowerShell and type:
```console
>>> git clone  https://github.com/espinosa012/blogabetWatcher.git
```
Optionally, you can set a virtualenv to isolate from the rest of your system
```console
>>> virtualenv bbwenv
```
To activate it, if you are on a terminal (Linux/Mac)
```console
>>> source bbwenv/bin/activate
```
If you are using cmd/PowerShell
```console
>>> source bbwenv/Scripts/activate
```
###	Use
Once you set up, to start using, execute main.py
```console
>>> python main.py
```

The first time you run the program, it will ask you to type your blogabet credentials.
After that, you will get them saved locally and encrypted (using cryptography module).

In main script, you can set 'my_tipsters' flag to watch your personal feed, this is, the feed with tipsters you are following,
or the all tipsters feed, to watch all blogabet tipsters and not only the one you are following.

Every time a new pick appears in feed, it prints on terminal, but you are free to change this behavour to perform anything you want
(like send it over email)

