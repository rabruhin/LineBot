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
        "兩數相加程式": "# Store input numbers
                        num1 = input('Enter first number: ')
                        num2 = input('Enter second number: ')

                        # Add two numbers
                        sum = float(num1) + float(num2)

                        # Display the sum
                        print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))",
        "交換變數": "# Python program to swap two variables
                    
                    x = 5
                    y = 10
                    
                    # To take inputs from the user
                    #x = input('Enter value of x: ')
                    #y = input('Enter value of y: ')
                    
                    # create a temporary variable and swap the values
                    temp = x
                    x = y
                    y = temp
                    
                    print('The value of x after swapping: {}'.format(x))
                    print('The value of y after swapping: {}'.format(y))
                    ",
        "隨機數字": "import random

                    print(random.randint(0,9))",
        "解二次方程式": "import cmath
                    
                    a = 1
                    b = 5
                    c = 6
                    
                    # calculate the discriminant
                    d = (b**2) - (4*a*c)
                    
                    # find two solutions
                    sol1 = (-b-cmath.sqrt(d))/(2*a)
                    sol2 = (-b+cmath.sqrt(d))/(2*a)
                    
                    print('The solution are {0} and {1}'.format(sol1,sol2))",
        "發牌程式": "# Python program to shuffle a deck of card

                    # importing modules
                    import itertools, random

                    # make a deck of cards
                    deck = list(itertools.product(range(1,14),['Spade','Heart','Diamond','Club']))

                    # shuffle the cards
                    random.shuffle(deck)

                    # draw five cards
                    print("You got:")
                    for i in range(5):
                     print(deck[i][0], "of", deck[i][1])
                    ",
        "顯示日歷": "import calendar
                    
                    yy = 2014  # year
                    mm = 11    # month
                    
                    # To take month and year input from the user
                    # yy = int(input("Enter year: "))
                    # mm = int(input("Enter month: "))
                    
                    # display the calendar
                    print(calendar.month(yy, mm))",
        "質數檢查": "# Program to check if a number is prime or not
                    
                    num = 29
                    
                    # To take input from the user
                    #num = int(input("Enter a number: "))
                    
                    # define a flag variable
                    flag = False
                    
                    if num == 1:
                        print(num, "is not a prime number")
                    elif num > 1:
                        # check for factors
                        for i in range(2, num):
                            if (num % i) == 0:
                                # if factor is found, set flag to True
                                flag = True
                                # break out of loop
                                break
                    
                        # check if flag is True
                        if flag:
                            print(num, "is not a prime number")
                        else:
                            print(num, "is a prime number")",
        "檢查是否是閏年": "# Python program to check if year is a leap year or not
                            
                            year = 2000
                            
                            # To get year (integer input) from the user
                            # year = int(input("Enter a year: "))
                            
                            # divided by 100 means century year (ending with 00)
                            # century year divided by 400 is leap year
                            if (year % 400 == 0) and (year % 100 == 0):
                                print("{0} is a leap year".format(year))
                            
                            # not divided by 100 means not a century year
                            # year divided by 4 is a leap year
                            elif (year % 4 ==0) and (year % 100 != 0):
                                print("{0} is a leap year".format(year))
                            
                            # if not divided by both 400 (century year) and 4 (not century year)
                            # year is not leap year
                            else:
                                print("{0} is not a leap year".format(year))",
        "找出因數": "# Python program to find the factorial of a number provided by the user.
                    
                    # change the value for a different result
                    num = 7
                    
                    # To take input from the user
                    #num = int(input("Enter a number: "))
                    
                    factorial = 1
                    
                    # check if the number is negative, positive or zero
                    if num < 0:
                       print("Sorry, factorial does not exist for negative numbers")
                    elif num == 0:
                       print("The factorial of 0 is 1")
                    else:
                       for i in range(1,num + 1):
                           factorial = factorial*i
                       print("The factorial of",num,"is",factorial)
                    ",
        "": "num = float(input("Enter a number: "))
                                  if num > 0:
                                     print("Positive number")
                                            elif num == 0:
                                               print("Zero")
                                            else:
                                               print("Negative number")",
        "十進位轉二進位": "# Function to print binary number using recursion
                            def convertToBinary(n):
                                if n > 1:
                                     convertToBinary(n//2)
                                print(n % 2,end = '')
                                
                            # decimal number
                            dec = 34
                                
                            convertToBinary(dec)
                            print()",
        "找出最大數": "  # Python program to find the largest number among the three input numbers
                        
                        # change the values of num1, num2 and num3
                        # for a different result
                        num1 = 10
                        num2 = 14
                        num3 = 12
                        
                        # uncomment following lines to take three numbers from user
                        #num1 = float(input("Enter first number: "))
                        #num2 = float(input("Enter second number: "))
                        #num3 = float(input("Enter third number: "))
                        
                        if (num1 >= num2) and (num1 >= num3):
                           largest = num1
                        elif (num2 >= num1) and (num2 >= num3):
                           largest = num2
                        else:
                           largest = num3
                        
                        print("The largest number is", largest)
                        ",
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
