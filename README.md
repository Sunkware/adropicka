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

to authorize the application within DropBox (app has production status, there's no limit of user number).

Run, copy URL from the console, follow this URL in the browser and allow the application to have an access to your DropBox account (its own folder or the whole tree).
Then copy authentication code from the web page and enter it at the application's prompt.
The token file, "adropicka_token.txt", should appear.
You have to perform the authorization only once.

### List folder content

```
python adropicka.py --list /folderOne/yetAnotherFolder
```
or
```
python adropicka.py -l /folderOne/yetAnotherFolder
```

Nested folders are not traversed.

### Make folder

```
python adropicka.py --makedir /nested/nextInside
```
or
```
python adropicka.py -m /nested/nextInside
```

If the folder exists already, error will not be raised.

### Upload file

```
python adropicka.py --upload ./testfile.dat /folderOne
```
or
```
python adropicka.py -u ./testfile.dat /folderOne
```

If the file exists already, it will be re-uploaded.

### Download file

```
python adropicka.py --download /folderOne/testfile.dat ./innerDir
```
or
```
python adropicka.py -d /folderOne/testfile.dat ./innerDir
```

If the file exists already, it will be re-downloaded.

### Remove file or folder

```
python adropicka.py --remove /folderOne/testfile.dat
python adropicka.py --remove /folderOne
```
or
```
python adropicka.py -r /folderOne/testfile.dat
python adropicka.py -r /folderOne
```

If file or folder doesn't exist, error will not be raised.

### Also...

There are few other options, run

```
python adropicka.py --help
```

to see them all.

### TODO

Copying, moving, sharing, ... a lot.

### Reverence

goes to [skicka](https://github.com/google/skicka), a much more sophisticated Google Drive console client,
which was the example to follow, in syntax and usage.

### Why so scarce?

The main purpose of this thing was to add a DropBox support to [Naamari project](http://sunkware.org/NAAMARI/index.html).
The upload/download/remove functionality seems to be sufficient... at the moment.
