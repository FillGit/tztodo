import rsa
import binascii
import string
import random
import datetime
from todo.models import Desks, CompanyName, Profile
from django.contrib.auth.models import User
from datetime import datetime

key_pub=rsa.PublicKey(
        int("0xabbd1d8445082db0d148b129b5cfa4c60b747b1f470f5ec7362e0ed165088477230c0071c96bb60e4ae6a0aa54b51338af264bf83cfca5d33beb1a73cecc311f",16),
        65537)
key_pri=rsa.PrivateKey(
        int("0xabbd1d8445082db0d148b129b5cfa4c60b747b1f470f5ec7362e0ed165088477230c0071c96bb60e4ae6a0aa54b51338af264bf83cfca5d33beb1a73cecc311f",16),
        65537,
        int("0x84381d39704c53a105ff89262baba9982fc985e116bc66a3c8babcfdc96279e8ad1bf59b8acac1a8523b70d4c4ca61d68ee9104267805df56146a308a0912f41",16),
        int("0xfdda817925c144525b330da5452d77d8aeb66dd04067c707f6625898cb8e778b0b2d",16),
        int("0xad30dce748fb344e73cccbd14728584fd6d20e1cec3721ee650fc78eacfb",16))

def kod_for_auth(user, password):
	now = datetime.now()
	S= (user + "/" + password + "/" + now.strftime("%d-%m-%Y")).encode('utf8')
	key_pub=rsa.PublicKey(
        int("0xabbd1d8445082db0d148b129b5cfa4c60b747b1f470f5ec7362e0ed165088477230c0071c96bb60e4ae6a0aa54b51338af264bf83cfca5d33beb1a73cecc311f",16),
        65537)
	crypto = rsa.encrypt(S,key_pub)
	
	return (binascii.b2a_hex(crypto))

def str_query_list (user, company_name, time_password):
	now = datetime.now()
	S= (user + "/" + company_name + "/" +
            time_password + "/" + now.strftime("%d-%m-%Y")).encode('utf8')
	key_pub=rsa.PublicKey(
        int("0xabbd1d8445082db0d148b129b5cfa4c60b747b1f470f5ec7362e0ed165088477230c0071c96bb60e4ae6a0aa54b51338af264bf83cfca5d33beb1a73cecc311f",16),
        65537)
	crypto = rsa.encrypt(S,key_pub)
	
	return (binascii.b2a_hex(crypto))

def query_de(str_code):
	key_pri=rsa.PrivateKey(
        int("0xabbd1d8445082db0d148b129b5cfa4c60b747b1f470f5ec7362e0ed165088477230c0071c96bb60e4ae6a0aa54b51338af264bf83cfca5d33beb1a73cecc311f",16),
        65537,
        int("0x84381d39704c53a105ff89262baba9982fc985e116bc66a3c8babcfdc96279e8ad1bf59b8acac1a8523b70d4c4ca61d68ee9104267805df56146a308a0912f41",16),
        int("0xfdda817925c144525b330da5452d77d8aeb66dd04067c707f6625898cb8e778b0b2d",16),
        int("0xad30dce748fb344e73cccbd14728584fd6d20e1cec3721ee650fc78eacfb",16))

	str_codeX=b'str_code'
	message = rsa.decrypt(binascii.unhexlify(str_codeX), key_pri)
	return (message)

def idsession_generator(size=8, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

def check_auth(key_idsession_f, companyname):
        
        
        if Profile.objects.filter(idsession=key_idsession_f, active_company=companyname).count()==1:
                modProfile=Profile.objects.get(idsession=key_idsession_f)

                now = datetime.now()
                check_date_idsession=(now.strftime("%Y-%m-%d")==str(modProfile.date_idsession))

                if check_date_idsession:
                        return True
                else:
                        return False


def check_auth_user_params(pk, key_auth_user_f):
        str_decode = query_de(key_auth_user_f).split('/')

        username=str_decode[0]
        password=str_decode[1]
        date_password=str_decode[2]

        user_obj=User.objects.get(username=username)
        modProfile=Profile.objects.get(user=user_obj)

        if (check_password(password, user_obj.password)):
                modProfile.time_password=time_password_generator()
                modProfile.date_password=now.strftime("%d-%m-%Y")
                modProfile.active_company=pk
                return True
        else:
                return False
