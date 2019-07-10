import hashlib
def md5encrypt( str ):
    hl = hashlib.md5()
    hl.update( str.encode(encoding='utf-8') )
    return hl.hexdigest()

if __name__ == "__main__":
    result = md5encrypt('mypwd')
    print(result)