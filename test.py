
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)


INTRODUCTION,CPU, BUDGET, ENDINTRO, USECASE = range(5)

updater = Updater(token='enter_toke_here')

dispatcher = updater.dispatcher

reply_start_keyboard = [['Yes', 'No']]
reply_explanation_keyboard = [['Skip Intro', 'Continue']]
reply_budget_keyboard = [['200-400', '400-600'],['600-800','800-1000']]
reply_continue_keyboard = [['continue']]
reply_usecase_keyboard= [['Gaming', 'Basic'],['Video editing']]

markup_start = ReplyKeyboardMarkup(reply_start_keyboard, one_time_keyboard=True)
markup_explanation =ReplyKeyboardMarkup(reply_explanation_keyboard, one_time_keyboard=True)
markup_budget =ReplyKeyboardMarkup(reply_budget_keyboard, one_time_keyboard=True)
markup_continue =ReplyKeyboardMarkup(reply_continue_keyboard, one_time_keyboard=True)
markup_usecase=ReplyKeyboardMarkup(reply_usecase_keyboard, one_time_keyboard=True)

def start(bot, update):
 bot.send_message(chat_id=update.message.chat_id, text="Hello! My name is Max. I am here to help you learn about computers and choose one of your own! Would you like a non-technical introduction into how computers work?",reply_markup=markup_start)
 return INTRODUCTION
 
def intro(bot,update):
 bot.send_message(chat_id=update.message.chat_id, text="Computers are quite easy to understand, especially if we can think about them as if they were people!",reply_markup=markup_explanation) 
 return CPU

def cpu(bot,update):
 bot.send_message(chat_id=update.message.chat_id, text="The CPU, or Central Processing Unit, is like the brain of the computer. It keeps track of information and decides what processes to execute.",reply_markup=markup_explanation)
 return ENDINTRO

def endintro(bot,update):  
 bot.send_message(chat_id=update.message.chat_id, text="Now you understand the basics of how a computer works! Let's begin helping you choose one.",reply_markup=markup_continue)
 return ENDINTRO

def budget(bot,update, user_data):
	bot.send_message(chat_id=update.message.chat_id, text="How much can you spend on this computer?", reply_markup=markup_budget)
	return BUDGET 
	
def usecase(bot,update, user_data):
	bot.send_message(chat_id=update.message.chat_id, text="What will you use your computer for?", reply_markup=markup_usecase)
	text = update.message.text
	user_data['budget'] = text
	return USECASE 

def gaming(bot,update, user_data):
	bot.send_message(chat_id=update.message.chat_id, text="With the budget of 800-1000 euros, I found this PC for gaming\n https://www.pccomponentes.com/pccom-silver-pro-i5-7500-16gb-ram-120gb-ssd-1tb-gtx-1060-3gb")
	return ConversationHandler.END
def unknown(bot, update):
 bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
 
 
#HANDLER DEFINITIONS

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
		 INTRODUCTION: [RegexHandler('^(Yes)$',
                                    intro),
                       RegexHandler('^(No)$',
                                    budget,pass_user_data=True),
                       ],
		 CPU:			[RegexHandler('^(Continue)$',
                                    cpu),
                       RegexHandler('^(Skip Intro)$',
                                    budget,pass_user_data=True),
						],
		 ENDINTRO:	   [RegexHandler('^(Continue)$',
                                    endintro),
                       RegexHandler('^(continue)$',
                                    budget,pass_user_data=True),							
                       ],	
		 BUDGET:        [RegexHandler('^(200-400|400-600|600-800|800-1000)$',
                                           usecase,
                                           pass_user_data=True),
                        ],	
		
	    USECASE:			[RegexHandler('^(Gaming)$',
                                    gaming,pass_user_data=True),
                       RegexHandler('^(Video editing)$',
                                    budget,pass_user_data=True),							
                        ],
            
        },

        fallbacks=[]
    )

dispatcher.add_handler(conv_handler)

#LAST HANDLER ALWAYS
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
updater.idle()

