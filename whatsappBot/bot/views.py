from random import choice
from django.shortcuts import render
from django.http import HttpResponse
from .models import Expenses
import datetime
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
SID = "AC5fbf4210c96041ee3d73ce239a505235"
TOKEN ="259233a6d0489e17b7c3e133ab761a4d"
from twilio.rest import Client

account_sid = 'AC5fbf4210c96041ee3d73ce239a505235'
auth_token = TOKEN
client = Client(account_sid, auth_token)

greetings = ['hi', 'hello']
greetingsReply = ['Hey, how can I help you today?', 'What\'s up?', "Hello from the other side", 'What\'s popping?']
BODY = "Hi {},\n1. Add new expense (1 <amount>,<category>,<desc>,<YYYY-MM-DD>\n2. Show expenses of Current Month\n3. Show Previous Month Expenses\n4. Show Spend Till Date this Month\n5. Show Spend Till Date last Month"
sep = "234567tr8vbufg7gf"

activeUsers = {}


ladder = {

    1:  lambda x, y: addExpenseInit(x, y),
    2:  lambda x:currentMonth,
    3:lambda x:previousMonth,
}

def addExpenseInit(user, message):
    print("Add expense got {}".format(message[1:]))
    try:
        print(message[1:].split(","))
        if("-" in message):
            amount, category, desc,ts = message[1:].split(',')
        else:
            ts = None   
            amount, category, desc = message[1:].split(',')
        print("ADDING")
        Expenses.objects.create(user = user.number, amount = amount, category = category, desc = desc, timestamp = ts if ts else datetime.datetime.now()).save()
        message = "Adding expense of Rs. \"{}\" in the category \"{}\" with desc \"{}\"".format(amount, category, desc)
    except Exception as e:
        message = "Invalid input {} {}".format(message, e)
    sendMessage(message, user.number)
    # return state+[1]
    pass


class User:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.lastMessage = "0"
def sumQS(QS):
    return "Rs. " +str(sum([int(x.amount) for x in QS]))
def sendMessage(text, no):
    print("Sending {}".format(text))
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=' ' + text,
        to=no
        )
    print("SENT MESSAGE {} TO {} with SID {}".format(text,no, message.sid))
    return True

def removeFromActiveUser(no):
    print("Removing {} from active users.".format(no))
    if(no in activeUsers):
        del activeUsers[no]

def sendQS(QS):
    return "\n".join([str(x) for x in QS])
def getNextFun(state):
    level = 0
    currentLevel = ladder
    print(state)
    for i in state[1:]:
        currentLevel = currentLevel[int(i)]
    print(currentLevel)
    return currentLevel
nums = [x for x in range(10)]
def driver(user, message):

    state = user.lastMessage.split(sep)[0]
    state = state.split(".")
    print(state)
    try:
        if(int(message.split()[0]) in nums):
            state.append(message)
        print("No exception? {} state {}".format(int(message.split()[0]) in nums, state))
    except Exception as e:
        print(e)
        pass
    if(state[-1] == '0'):
        sendMessage(BODY.format(user.name), user.number)
    # fun = getNextFun(state)
    if(state[-1][0] == '1'):
        addExpenseInit(user, message)
    elif(state[-1][0] == '2'):
        sendMessage(sendQS(Expenses.getCurrentMonth(user.number)), user.number)
    elif(state[-1][0] == '3'):
        sendMessage(sendQS(Expenses.getPreviousMonth(user.number)), user.number)
    elif(state[-1][0] == '4'):
        sendMessage(sumQS(Expenses.getCurrentMonth(user.number)), user.number)
    elif(state[-1][0] == '5'):
        sendMessage(sumQS(Expenses.getPreviousMonth(user.number)), user.number)
    # sendMessage(str(fun), user.number)



@csrf_exempt
def bot(request):
    message = request.POST['Body']
    user = request.POST['ProfileName']
    no = request.POST['From']
    print(no)
    # sendMessage("REPLYING", no)
    if(no not in activeUsers):
        obj = User( no, user)
        activeUsers[no] = obj
    driver(activeUsers[no], message)
    return HttpResponse("HELO")

    # 3AAH2BQ6USL9CHTE1JRF3L6T