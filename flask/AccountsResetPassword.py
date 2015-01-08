import flaskr as main
from flask import jsonify
import random
import threading
from threading import Timer
import util
import SendMail
import time
import Accounts
TWO_HOURS = 2*60*60
accountLock = threading.Lock()
tempPasswords = main.admindb.tempPasswords
accounts = main.admindb.accounts

def generateResetPasswordEmail(emailAddress,serverUrlPrefix, token):
    """
    Generate and send email. This is a thread since the SMTP timeout is 30 seconds
    """
    urlToClick = serverUrlPrefix + "/spectrumbrowser/resetPassword/" +emailAddress+ "?token="+str(token)
    util.debugPrint("URL to Click for reset password email" + urlToClick)
    message = "This is an automatically generated message from the Spectrum Monitoring System.\n"\
    +"You requested to reset your password to a password you entered into " + str(serverUrlPrefix) +"\n"\
    +"Please click here within 2 hours to reset your password\n"\
    +"(or ignore this mail if you did not originate this request):\n"\
    + urlToClick +"\n"
    util.debugPrint(message)
    SendMail.sendMail(message,emailAddress, "reset password link")


def storePasswordAndEmailUser(emailAddress,newPassword,urlPrefix):
    
    accountLock.acquire()
    
    try:
        print "storePasswordAndEmailUser", emailAddress,newPassword,urlPrefix
        # JEK: Search for email, if found send email for user to activate reset password.
        # TODO -- invoke external account manager here (such as LDAP).
        existingAccount = accounts.find_one({"emailAddress":emailAddress})
        if existingAccount == None:
            util.debugPrint("Email not found as an existing user account")
            return jsonify({"status":"INVALUSER"})
        else:
            # JEK: Note: we really only need to check the password and not the email here
            # Since we will email the user and know soon enough if the email is invalid.
            if not Accounts.isPasswordValid(newPassword) :
                util.debugPrint("Password invalid")
                return jsonify({"status":"INVALPASS"})
            else:
                util.debugPrint("Password valid")
                tempPasswordRecord = tempPasswords.find_one({"emailAddress":emailAddress})
                if tempPasswordRecord == None:
                    util.debugPrint("Email not found")
                    random.seed()
                    token = random.randint(1,100000)
                    expireTime = time.time()+TWO_HOURS
                    util.debugPrint("set temp record")
                    #since this is only stored temporarily for a short time, it is ok to have a temp plain text password
                    tempPasswordRecord = {"emailAddress":emailAddress,"password":newPassword,"expireTime":expireTime,"token":token}
                    tempPasswords.insert(tempPasswordRecord)
                    retval = {"status": "OK"}
                    util.debugPrint("OK")
                    t = threading.Thread(target=generateResetPasswordEmail,args=(emailAddress,urlPrefix, token))
                    t.daemon = True
                    t.start()
                    return jsonify(retval)
                else:
                    print "Email found"
                    # Password reset is already pending for this email.
                    return jsonify({"status":"PENDING"})


    except:
        retval = {"status": "NOK"}
        print "NOK"
        return jsonify(retval)
    finally:
        accountLock.release()
        
def activatePassword(email, token):
    util.debugPrint("called active password sub")
    accountLock.acquire()
    try:
        tempPassword = tempPasswords.find_one({"emailAddress":email, "token":token})
        if tempPassword == None:
            util.debugPrint("Email and token not found; invalid request")
            return False
        else:
            util.debugPrint("Email and token found in temp passwords")
            # TODO -- invoke external account manager here (such as LDAP).
            existingAccount = accounts.find_one({"emailAddress":email})
            if existingAccount == None:
                util.debugPrint("Account does not exist, cannot reset password")
                return False
            else:
                util.debugPrint("Email found in existing accounts")
                existingAccount["password"] = tempPassword["password"]
                existingAccount["time"] = time.time()
                accounts.update({"_id":existingAccount["_id"]},{"$set":existingAccount},upsert=False)
                util.debugPrint("Resetting account password")
                tempPasswords.remove({"_id":tempPassword["_id"]})
                return True
    except:       
        return False
    finally:
        accountLock.release()

Accounts.removeExpiredRows(tempPasswords)

