# -*- coding: utf-8 -*-
from linepy import *
from os.path import join, dirname
import os
from var_dump import var_dump
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

EMAIL = os.environ.get("LINE_EMAIL")
PASSW = os.environ.get("LINE_PASSW")

line = LINE(EMAIL, PASSW)
#line = LINE('AUTHTOKEN')

line.log("Auth Token : " + str(line.authToken))

# Initialize OEPoll with LINE instance
oepoll = OEPoll(line)
# Receive messages from OEPoll
config = {
    "autoreadMsg": True
}


def RECEIVE_MESSAGE(op):
    msg = op.message

    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from

    # Check content only text message
    if msg.contentType == 0:
        if text == "gid":
            # gid = line.getGroupIdsByName('Illuminati Cendol')
            # line.sendMessage(sender, "Iluminati Cendol gid: {}".format(gid))
            line.getGroups()
            var_dump(line.getProfileDetail(os.environ.get("ADMIN_MID")))
        else:
            if config["autoread"]:
                line.sendChatChecked(sender, msg_id)
            else:
                line.sendMessage(sender, text)

        # Check only group chat
        if msg.toType == 2:
            # Get sender contact
            contact = line.getContact(sender)

            txt = '[%s] %s' % (contact.displayName, text)
            # Send a message
            # line.sendMessage(receiver, 'sender:'+sender+' response:'+text)
            # Print log
            line.log(txt)


def NOTIFIED_READ_MSG(op):
    try:
        var_dump(op)
    except Exception as e:
        line.log(str(e))


def TYPING(op):
    var_dump(op)


# Add function to OEPoll
oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_READ_MESSAGE: NOTIFIED_READ_MSG
})

while True:
    oepoll.trace()
