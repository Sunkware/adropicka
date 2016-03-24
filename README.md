## adropicka

Another very basic one-file-per-run console client-wrapper for DropBox, based on Python SDK

You'll need [Python](https://www.python.org/) and [DropBox for Python SDK](https://github.com/dropbox/dropbox-sdk-python) to run this one.

### Authorization

```
python adropicka.py --authorize-dir
```
or
```
python adropicka.py --authorize-root
```

to authorize the application within DropBox (in development status now, 100 users limit).

Run, copy URL from the console, follow this URL in the browser and allow the application to have an access to your DropBox account (its own dir or the whole tree).
Then copy authentication code from the web page and enter it at the application's prompt.
The token file, "adropicka_token.txt", should appear.
You have to perform the authorization only once.

### Upload file

```
python adropicka.py --upload ./testfile.dat /folderOne
```
or
```
python adropicka.py -u ./testfile.dat /folderOne
```

### Download file

```
python adropicka.py --download /folderOne/testfile.dat ./innerDir
```
or
```
python adropicka.py -d /folderOne/testfile.dat ./innerDir
```

### Remove file

```
python adropicka.py --remove /folderOne/testfile.dat
```
or
```
python adropicka.py -r /folderOne/testfile.dat
```

If file doesn't exist, error will not be raised.

### Also...

There are few other options, run

```
python adropicka.py --help
```

to see them all.

### TODO

Listing, copying, moving, sharing, ... a lot.

### Reverence

goes to [skicka](https://github.com/google/skicka), a much more sophisticated Google Drive console client,
which was the example to follow, in syntax and usage.

### Why so scarce?

The main purpose of this thing is to add a DropBox support to [Naamari project](http://sunkware.org/NAAMARI/index.html).
The upload/download/remove functionality seems to be sufficient... at the moment.
