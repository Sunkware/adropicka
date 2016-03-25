#!/usr/bin/env python3

#
#  Adropicka - a very basic one-file-per-run console client-wrapper for DropBox
#  Copyright (c) 2016 Sunkware
#  Key FP = 6B6D C8E9 3438 6E9C 3D97  56E5 2CE9 A476 99EF 28F6
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#  ----------------------------------------------------------------
#  WWW:       sunkware.org
#  E-mail:    sunkware@gmail.com
#  ----------------------------------------------------------------
#


import os
import optparse
import dropbox


APP_ROOT_KEY = "aocd70ng4f8xfjw"
APP_ROOT_SECRET = "quymsslrmgeqtv4"

APP_DIR_KEY = "w1bbm86307efcwb"
APP_DIR_SECRET = "r03i2ayet4yr1sm"

UPLOAD_CHUNK_SIZE = 16777216 # 16 Mb
UPLOAD_MAX_SINGLE_CHUNK_FILE_SIZE = 33554432 # 32 Mb (DropBox API mentions 150 (March 2016))


def main():

    global APP_ROOT_KEY
    global APP_ROOT_SECRET

    global APP_DIR_KEY
    global APP_DIR_SECRET

    global UPLOAD_CHUNK_SIZE
    global UPLOAD_MAX_SINGLE_CHUNK_FILE_SIZE


    print("Adropicka v0.94")


    op = optparse.OptionParser()

    op.add_option("--authorize-root", action = "store_true", default = False, dest = "authorize_root", help = "Authorize the application for root access")
    op.add_option("--authorize-dir", action = "store_true", default = False, dest = "authorize_dir", help = "Authorize the application for folder access")
    op.add_option("-l", "--list", action = "store_true", default = False, dest = "enlist", help = "List content of folder")
    op.add_option("-m", "--makedir", action = "store_true", default = False, dest = "makedir", help = "Create folder")
    op.add_option("-u", "--upload", action = "store_true", default = False, dest = "upload", help = "Upload file")
    op.add_option("-d", "--download", action = "store_true", default = False, dest = "download", help = "Download file")
    op.add_option("-r", "--remove", action = "store_true", default = False, dest = "remove", help = "Remove file or folder")

    op.add_option("-t", "--tokenpath", action = "store", default = "adropicka_token.txt", dest = "tokenpath", help = "Path to the text file with an access token")
    op.add_option("-c", "--chunksize", action = "store", default = UPLOAD_CHUNK_SIZE, dest = "chunksize", help = "Size of upload chunk in bytes")
    op.add_option("-s", "--singlemaxsize", action = "store", default = UPLOAD_MAX_SINGLE_CHUNK_FILE_SIZE, dest = "singlemaxsize", help = "Max size of file to be uploaded as a single data block")    

    opts, args = op.parse_args()


    authorize_root = opts.authorize_root;
    authorize_dir = opts.authorize_dir;
    enlist = opts.enlist
    makedir = opts.makedir
    upload = opts.upload
    download = opts.download
    remove = opts.remove

    actionsnum = int(authorize_root) + int(authorize_dir) + int(enlist) + int(makedir) + int(upload) + int(download) + int(remove)

    if actionsnum == 0:
        print("No action is specified! Run with --help or -h to get to know the syntax.")
        return -1

    if actionsnum > 1:
        print("More than one action is specified!")
        return -2


# Process authorizing (before checking for token)...
    if authorize_root or authorize_dir:

# Taken from SDK/dropbox/oauth...

        if authorize_root:
            auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_ROOT_KEY, APP_ROOT_SECRET)
        else:
            auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_DIR_KEY, APP_DIR_SECRET)

        authorize_url = auth_flow.start()
        print("1. In your browser, go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            access_token, user_id = auth_flow.finish(auth_code)
        except Exception as e:
            print("Error: %s" % (e,))
            return -3

        print("Access token obtained.")

        try:
            file = open(opts.tokenpath, "wt")
        except IOError as err:
            print("Cannot create token file " + "\"" + opts.tokenpath + "\"!")
            print(err)
            return -4

        file.write(access_token)
        file.close()

        print("Token saved in " + "\"" + opts.tokenpath + "\".")


# Reading access token
    tokenpath = opts.tokenpath

    try:
        tokenfile = open(tokenpath, "rt")
    except IOError as err:
        print("Cannot open token file " + "\"" + tokenpath + "\"!")
        print(err)
        print("If you haven't got a token yet, run with --authorize-dir or --authorize-root option.")
        return -5

    token = tokenfile.readline()
    tokenfile.close()


    if opts.chunksize > 0:
        UPLOAD_CHUNK_SIZE = opts.chunksize

    if opts.singlemaxsize > 0:
        UPLOAD_MAX_SINGLE_CHUNK_FILE_SIZE = opts.singlemaxsize


    dbx = dropbox.Dropbox(token)
    if dbx is None:
        print("Client hasn't been initialized!")
        return -6

    print("Client initialized.")


# Process list operation
    if enlist:
        if len(args) != 1:
            print("Remote dir path must be specified!")
            return -7
        
        dirpath = args[0]
        if not dirpath.startswith("/"):
            dirpath = "/" + dirpath
        if dirpath.endswith("/"):
            dirpath = dirpath[0:len(dirpath) - 1] # particularly, root path should be represented by empty string

        print("Listing content of " + "\"" + dirpath + "\"...")

        try:
            folder_res = dbx.files_list_folder(dirpath)
        except dropbox.exceptions.ApiError as err:
           print("API error!")
           print(err)
           return -8

        entries_num = len(folder_res.entries)

        for i in range(0, entries_num):
            print(make_folder_entry_string(folder_res.entries[i]))

        while folder_res.has_more:
            try:
                folder_res = dbx.files_list_folder_continue(folder_res.cursor)
            except dropbox.exceptions.ApiError as err:
                print("API error!")
                print(err)
                return -9

            entries_num = len(folder_res.entries)

            for i in range(0, entries_num):
                print(make_folder_entry_string(folder_res.entries[i]))


# Process makedir operation
    if makedir:
        if len(args) != 1:
            print("Remote dir path must be specified!")
            return -10
        
        dirpath = args[0]
        if not dirpath.startswith("/"):
            dirpath = "/" + dirpath
        if dirpath.endswith("/"):
            dirpath = dirpath[0:len(dirpath) - 1]

        print("Creating " + "\"" + dirpath + "\" folder...")

        folder_exists = False

        try:
            folder_res = dbx.files_create_folder(dirpath)
        except dropbox.exceptions.ApiError as err:
# If the folder exists, don't interrupt with error (goal of making is attained already)
# Other API error-s are processed as usual

# Unwinding error stack...
           if isinstance(err.error, dropbox.files.CreateFolderError):
               if err.error.is_path():
                   if err.error.get_path().is_conflict():
                       if err.error.get_path().get_conflict().is_folder():
                           folder_exists = True

           if not folder_exists:
               print("API error!")
               print(err)
               return -11

        if folder_exists:
            print("Folder exists already.")
        else:
            print("Created folder")


# Process upload operation
    if upload:
        if len(args) != 2:
            print("Local file path and remote dir path must be specified!")
            return -12

        srcfilepath = args[0]
        destpath = args[1]


        basename = os.path.basename(srcfilepath)

        destfilepath = destpath;
        if not destfilepath.startswith("/"):
            destfilepath = "/" + destfilepath
        if not destfilepath.endswith("/"):
            destfilepath += "/"

        destfilepath += basename
 
        print("Uploading " + "\"" + basename + "\"...")

        ub = upload_to_file(dbx, destfilepath, srcfilepath) # breaking file content into chunks if needed
        if ub < 0:
            print("Upload error!")
            return -13

        print("Uploaded " + "\"" + basename + "\"" + " (" + str(ub) + " bytes)")


# Process download operation
    if download:
        if len(args) != 2:
            print("Remote file path and local dir path must be specified!")
            return -14

        srcfilepath = args[0]
        if not srcfilepath.startswith("/"):
            srcfilepath = "/" + srcfilepath

        destpath = args[1]


        basename = os.path.basename(srcfilepath)

        destfilepath = destpath;
        if not destpath.endswith("/"):
            destfilepath += "/"

        destfilepath += basename


        print("Downloading " + "\"" + basename + "\"...")

        try:
           res = dbx.files_download_to_file(destfilepath, srcfilepath)
        except dropbox.exceptions.ApiError as err:
           print("API error!")
           print(err)
           return -15

        print("Downloaded " + "\"" + basename + "\"" + " (" + str(res.size) + " bytes)")


# Process remove operation
    if remove:
        if len(args) != 1:
            print("Remote file (or folder) path must be specified!")
            return -16

        filepath = args[0]
        if not filepath.startswith("/"):
            filepath = "/" + filepath

        basename = os.path.basename(filepath)

        print("Removing " + "\"" + basename + "\"...")

        obj_not_found = False 

        try:
            res = dbx.files_delete(filepath)
        except dropbox.exceptions.ApiError as err:
# If file not found, show message but don't interrupt with error (goal of removal is attained already)
# Other ApiError-s are processed as usual

# Unwinding error stack...
            if isinstance(err.error, dropbox.files.DeleteError):
                if err.error.is_path_lookup():
                    if err.error.get_path_lookup().is_not_found():
                        obj_not_found = True

            if not obj_not_found:
                print("API error!")
                print(err)
                return -17

        if obj_not_found:
            print("File or folder not found, considered to be removed.")
        else:
            if hasattr(res, "size"):
                print("Removed " + "\"" + basename + "\"" + " (" + str(res.size) + " bytes)")
            else:
                print("Removed " + "[" + basename + "]" + " folder")

    return 0



def upload_to_file(dropbox_client, destfilepath, srcfilepath):

    global UPLOAD_CHUNK_SIZE
    global UPLOAD_MAX_SINGLE_CHUNK_FILE_SIZE

    try:
        file = open(srcfilepath, 'rb')
    except IOError as err:
        print("Cannot open file " + "\"" + basename + "\"" + "!")
        print(err)
        return -1

    fsize = filesize(file)


    if fsize <= UPLOAD_MAX_SINGLE_CHUNK_FILE_SIZE: # upload without chunks and session

        data = file.read()

        try:
            res = dropbox_client.files_upload(data, destfilepath, dropbox.files.WriteMode.overwrite)
        except dropbox.exceptions.ApiError as err:
            print("API error!")
            print(err)
            return -2

        file.close()

        return fsize

# else --- start session, append to it, then finish...

    fullchunks = fsize // UPLOAD_CHUNK_SIZE
    lastchunksize = fsize % UPLOAD_CHUNK_SIZE

    offset = 0

# upload 0 bytes to start session

    data = file.read(0)

    try:
        session_start_res = dropbox_client.files_upload_session_start(data)
    except dropbox.exceptions.ApiError as err:
        print("API error!")
        print(err)
        return -3

    offset += len(data)


# Appending full chunks...

    for i in range(0, fullchunks):
        data = file.read(UPLOAD_CHUNK_SIZE)

        try:
            dropbox_client.files_upload_session_append(data, session_start_res.session_id, offset)
        except dropbox.exceptions.ApiError as err:
            print("API error!")
            print(err)
            return -4

        offset += len(data)
    

# Finishing session with the last chunk...
    data = file.read(lastchunksize)

    cursor = dropbox.files.UploadSessionCursor(session_start_res.session_id, offset)
    commit = dropbox.files.CommitInfo(destfilepath, dropbox.files.WriteMode.overwrite)

    try:
        dropbox_client.files_upload_session_finish(data, cursor, commit)
    except dropbox.exceptions.ApiError as err:
        print("API error!")
        print(err)
        return -5


    file.close()

    return fsize


def filesize(f):
    if f is not None:
        curpos = f.tell()
        size = f.seek(0, 2)
        f.seek(curpos, 0)
        return size        
    
    return -1


def make_folder_entry_string(en):
    res = ""

    if en is not None:
        if isinstance(en, dropbox.files.FileMetadata):
            res = "\"" + en.name + "\"" + " (" + str(en.size) + " B)"
        elif isinstance(en, dropbox.files.FolderMetadata):
            res = "[" + en.name + "]"
        else:
            res = "???"

    return res



if __name__ == "__main__":
    main()