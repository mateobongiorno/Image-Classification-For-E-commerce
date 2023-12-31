import hashlib
import os

def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    # Current implementation will allow any kind of file.
    
    _, extension = os.path.splitext(filename)

    if extension.lower() in [".png", ".jpg", ".jpeg", ".gif"]:
        return True
    else:
        return False

def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # Current implementation will return the original file name.
    
    md5 = hashlib.md5(file.read()).hexdigest()
    file.seek(0) 
    _, extension = os.path.splitext(file.filename)
    file.filename = md5 + extension
    return os.path.basename(file.filename)
