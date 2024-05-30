from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    questions_answers = {
         "說話程式": "print('Hello, world!')",
        "兩數相加程式": "# Store input numbers\nnum1 = input('Enter first number: ')\nnum2 = input('Enter second number: ')\n\n# Add two numbers\nsum = float(num1) + float(num2)\n\n# Display the sum\nprint('The sum of {0} and {1} is {2}'.format(num1, num2, sum))",
        "交換變數": "# Python program to swap two variables\n\nx = 5\ny = 10\n\n# To take inputs from the user\n#x = input('Enter value of x: ')\n#y = input('Enter value of y: ')\n\n# create a temporary variable and swap the values\ntemp = x\nx = y\ny = temp\n\nprint('The value of x after swapping: {}'.format(x))\nprint('The value of y after swapping: {}'.format(y))",
        "隨機數字": "import random\n\nprint(random.randint(0,9))",
        "解二次方程式": "import cmath\n\na = 1\nb = 5\nc = 6\n\n# calculate the discriminant\nd = (b**2) - (4*a*c)\n\n# find two solutions\nsol1 = (-b-cmath.sqrt(d))/(2*a)\nsol2 = (-b+cmath.sqrt(d))/(2*a)\n\nprint('The solution are {0} and {1}'.format(sol1,sol2))",
        "發牌程式": "# Python program to shuffle a deck of card\n\n# importing modules\nimport itertools, random\n\n# make a deck of cards\ndeck = list(itertools.product(range(1,14),['Spade','Heart','Diamond','Club']))\n\n# shuffle the cards\nrandom.shuffle(deck)\n\n# draw five cards\nprint('You got:')\nfor i in range(5):\n    print(deck[i][0], 'of', deck[i][1])",
        "顯示日歷": "import calendar\n\nyy = 2014  # year\nmm = 11    # month\n\n# To take month and year input from the user\n# yy = int(input('Enter year: '))\n# mm = int(input('Enter month: '))\n\n# display the calendar\nprint(calendar.month(yy, mm))",
        "質數檢查": "# Program to check if a number is prime or not\n\nnum = 29\n\n# To take input from the user\n#num = int(input('Enter a number: '))\n\n# define a flag variable\nflag = False\n\nif num == 1:\n    print(num, 'is not a prime number')\nelif num > 1:\n    # check for factors\n    for i in range(2, num):\n        if (num % i) == 0:\n            # if factor is found, set flag to True\n            flag = True\n            # break out of loop\n            break\n\n# check if flag is True\nif flag:\n    print(num, 'is not a prime number')\nelse:\n    print(num, 'is a prime number')",
        "檢查是否是閏年": "# Python program to check if year is a leap year or not\n\nyear = 2000\n\n# To get year (integer input) from the user\n# year = int(input('Enter a year: '))\n\n# divided by 100 means century year (ending with 00)\n# century year divided by 400 is leap year\nif (year % 400 == 0) and (year % 100 == 0):\n    print('{0} is a leap year'.format(year))\n\n# not divided by 100 means not a century year\n# year divided by 4 is a leap year\nelif (year % 4 == 0) and (year % 100 != 0):\n    print('{0} is a leap year'.format(year))\n\n# if not divided by both 400 (century year) and 4 (not century year)\n# year is not leap year\nelse:\n    print('{0} is not a leap year'.format(year))",
        "找出因數": "# Python program to find the factorial of a number provided by the user.\n\n# change the value for a different result\nnum = 7\n\n# To take input from the user\n#num = int(input('Enter a number: '))\n\nfactorial = 1\n\n# check if the number is negative, positive or zero\nif num < 0:\n    print('Sorry, factorial does not exist for negative numbers')\nelif num == 0:\n    print('The factorial of 0 is 1')\nelse:\n    for i in range(1,num + 1):\n        factorial = factorial*i\n    print('The factorial of',num,'is',factorial)",
        "是否大於零": "num = float(input('Enter a number: '))\nif num > 0:\n    print('Positive number')\nelif num == 0:\n    print('Zero')\nelse:\n    print('Negative number')",
        "十進位轉二進位": "# Function to print binary number using recursion\n\ndef convertToBinary(n):\n    if n > 1:\n        convertToBinary(n//2)\n    print(n % 2,end = '')\n\n# decimal number\ndec = 34\n\nconvertToBinary(dec)\nprint()",
        "找出最大數": "# Python program to find the largest number among the three input numbers\n\n# change the values of num1, num2 and num3\n# for a different result\nnum1 = 10\nnum2 = 14\nnum3 = 12\n\n# uncomment following lines to take three numbers from user\n#num1 = float(input('Enter first number: '))\n#num2 = float(input('Enter second number: '))\n#num3 = float(input('Enter third number: '))\n\nif (num1 >= num2) and (num1 >= num3):\n    largest = num1\nelif (num2 >= num1) and (num2 >= num3):\n    largest = num2\nelse:\n    largest = num3\n\nprint('The largest number is', largest)"
    }
    if msg in questions_answers:
        #print(f"{english_word} 的中文翻譯是：{words_dict[english_word]}")
    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(questions_answers[msg]))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
       
         

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
