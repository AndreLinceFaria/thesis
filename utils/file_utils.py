import os,shutil

readsize = 1024
bytes = 99000000
chunksize = int(bytes)

def split(fromfile, todir, chunksize=chunksize, zip=False, remove_file=True):
    #print("Splitting file: " + fromfile)
    if not os.path.exists(todir):  # caller handles errors
        os.mkdir(todir)
    '''else:
        for fname in os.listdir(todir):  # delete any existing files
            os.remove(os.path.join(todir, fname))'''
    partnum = 0
    input = open(fromfile, 'rb')  # use binary mode on Windows
    while 1:  # eof=empty string from read
        chunk = input.read(chunksize)  # get next part <= chunksize
        if not chunk: break
        partnum = partnum + 1
        filename = os.path.join(todir, ('database%04d' % partnum))
        fileobj = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()  # or simply open(  ).write(  )
    input.close()
    assert partnum <= 9999  # join sort fails if 5 digits
    if remove_file:
        os.remove(fromfile)
    return partnum

def join(fromdir, tofile, zip=False, remove_dir = True):
    #print("Joining into file: " + tofile)
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    parts.sort(  )
    parts = os.listdir(fromdir)
    parts.sort()
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(readsize)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close()
    output.close()
    if remove_dir:
        shutil.rmtree(fromdir)


def remove_from_dir(dir):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)