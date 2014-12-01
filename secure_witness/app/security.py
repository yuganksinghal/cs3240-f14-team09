import hashlib
import os, struct


def encrypt(password, input, outputfile, path, chunksize = 64*512):
    key = hashlib.sha256(password).digest()
    outfile = outputfile+'.enc'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(input)
    with open(input, 'rb') as infile:
        with open(outfile, 'wb') as outf:
            outf.write(struct.pack('<Q', filesize))
            outf.write(iv)
            outf.write(key)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outf.write(encryptor.encrypt(chunk))

def decrypt(password, input, chunksize = 16*512):
    output = input[:-4]
    with open(input, 'rb') as infile:
        fsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        check = infile.read(32)
        key = hashlib.sha256(password)
        if(check != key):
            return False
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(output, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(fsize)

    return True