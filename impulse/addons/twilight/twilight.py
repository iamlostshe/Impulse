# Import modules
import impulse.addons.twilight.hash as Hash
import impulse.addons.twilight.salt as Salt
import impulse.addons.twilight.xor as Xor


# Encrypt function
def Encrypt(text, key):
    salt = Hash.getSaltByKey(key, text)
    saltedText = Salt.protect(text, salt)
    xoredText = Xor.encode(saltedText, key)
    return xoredText


# Decrypt function
def Decrypt(text, key):
    unxoredText = Xor.decode(text, key)
    salt = Hash.getSaltByKey(key, unxoredText)
    unsaltData = Salt.unprotect(unxoredText, salt)
    return unsaltData
