import sys,os
import argparse
import unittest
import configparser
from time import sleep
import subprocess

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.comparisons import levenshtein_distance

from flask import Flask, redirect, url_for, request, render_template
from flask_cors import CORS

globalParameter = {}

#Enable command jarvis
globalParameter['PathJarvis'] = "C:\\Jarvis\\Jarvis.py"
globalParameter['PathExecutable'] = "python"

#Loading in GetCorrectPath()
globalParameter['Path'] = None
globalParameter['PathBackgroud'] = None
globalParameter['PathAgentReaction'] = None

globalParameter['InternalPathBackgroud'] = "bot/background/"
globalParameter['InternalPathAgentReaction'] = "bot/agent/"

globalParameter['LocalPort'] = 8821
globalParameter['LocalIp'] = "0.0.0.0"
globalParameter['MAINWEBSERVER'] = True
globalParameter['PathDB'] = "db.sqlite3"
globalParameter['maximum_similarity_threshold'] = 0.80

globalParameter['BotImgReaction'] = []
globalParameter['BotReactionTranslations'] = []

app = Flask(__name__, static_url_path="/External", static_folder='External')
CORS(app)

class TestCases(unittest.TestCase):
    def test_dump(self):
        check = True
        self.assertTrue(check)

class MyChatBot():
    def __init__(self):
        noob = False        
        if os.path.isfile(str(globalParameter['PathDB'])) == False:
            noob = True
            print('mode noob')
        else:
            print('mode noob off')
        
        self.chatbot = ChatBot(
            'Jarvis',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///' + str(globalParameter['PathDB']),
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Não entendi',
                    'maximum_similarity_threshold': globalParameter['maximum_similarity_threshold']
                }
            ]
        )

        if noob == True:
            self.training4memory()
		
    def __del__(self):
        pass

    def training4conversation(self, conversation):
        #conversation = ["oi","olá", "Tchau","Até logo", "=)","Legal"]
        trainer = ListTrainer(self.chatbot)
        trainer.train(conversation)
    
    def training4memory(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        #trainer.train("chatterbot.corpus.english")
        #trainer.train("chatterbot.corpus.portuguese")

        print('training4memory')
        if(os.path.exists("pt")==True):
            trainer.train("pt")
            print('training4memory pt')
        else:
            trainer.train("chatterbot.corpus.portuguese")
            print('training4memory corpus.portuguese')

    def response(self, ask):
        if(str(ask).lower().find('[learn]') >= 0 and str(ask).lower().find('[answer]') >= 0):
            answer = ask.split('[answer]')[1]
            ask = ask.split('[answer]')[0].replace('[learn]','')            
            self.training4conversation([ask, str(answer)])          

        res = self.chatbot.get_response(ask)

        return res            

def BotResponse(ask):
    bot = MyChatBot()
    ask = ask.replace('_', ' ')
    #print(ask)
    res = bot.response(ask)   
    print(res) 
    return str(res)

def ChatBotLoop(Learn = False):    
    bot = MyChatBot()
    loop = True    
    
    while(loop):
        ask = input(">")
        
        if(ask == None):
            print('...')
            continue

        res = bot.response(ask)

        print(res)

        if(Learn==True and str(res) == "Não entendi"):
            print("Deseja que eu aprenda?")
            res = input(">")
            if(res == 'sim'):
                print(ask)
                res4train = input(">")
                bot.training4conversation([ask, str(res4train)])          
        else:
            pass

        if(ask == 'tchau'):
            loop = False
            break
    pass 

@app.route('/botresponse',methods = ['POST', 'GET'])
def botresponse():
    if request.method == 'POST':
        data = request.get_json(force=True)  
        #ask = str(data[0])
        #print(ask)
        return BotResponse(data['ask'])
    else:
        ask = request.args.get('ask')
        return BotResponse(ask)

@app.route('/')
def index():
    return str(Main.__doc__) + " | ip server : " +  str(globalParameter['LocalIp']) + ":" + str(globalParameter['LocalPort'])

@app.route('/bot')
def makePageBot():
    ext_bootstrap_css = 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css'
    ext_jquery_js = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'
    ext_bootstrap_js = 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js'    
    background = 'External/bot/background/1.png'
    img_max_height_mobile = '80%'
    img_max_height_web = '100%'
    chat_height = '3em'
    
    PAGE_HEAD = '<head>'
    PAGE_STYLE = '<style>html, body {background: url("' + background + '") no-repeat center center fixed; -webkit-background-size: cover;-moz-background-size: cover;-o-background-size: cover;background-size: cover;}#responsive-imgs img {display: block;margin: 1px auto;max-width: 100%;}@media screen and (max-width: 600px) {.responsive-imgs-resp img { max-height: ' + img_max_height_mobile + ';}} @media screen and (min-width: 600px) {.responsive-imgs-resp img { max-height: ' + img_max_height_web + ';}} .effect1 {animation-name:img-ani1;animation-duration: 2s; animation-timing-function: ease-in;}.effect2 {animation-name:img-ani2;animation-duration: 2s; animation-timing-function: ease-in;}@keyframes img-ani1 {from{opacity:0;}to{opacity: 1;}}@keyframes img-ani2 {from{opacity:0;}to{opacity: 1;}}.chat {z-index: 1500;display: block;margin: 20px auto;max-width: 90%;} #input-chat, #buttonchat {line-height: ' + chat_height + ';} </style>'
    PAGE_STYLE += '<link href="' + ext_bootstrap_css + '" rel="stylesheet" crossorigin="anonymous"><script src="' + ext_jquery_js + '"></script>'
    PAGE_HEAD = PAGE_HEAD + PAGE_STYLE + '</head>'

    PAGE_BODY = '<body><div id="responsive-imgs" class="responsive-imgs-resp"><img id="agent" class="fixed-bottom"></div><div class="chat fixed-bottom"><div class="input-group input-space"><input type="text" id="input-chat" class="form-control" placeholder="chat with me" aria-label="chat with me" aria-describedby="basic-addon2"><div class="input-group-append"><span class="input-group-text" id="basic-addon2"><a id="buttonchat" href="#" onclick="SendChat();return false;">chat</a></span></div></div></div></body>'

    PAGE_SPRIPT = '<script src="' + ext_bootstrap_js + '" crossorigin="anonymous"></script>'
    PAGE_SPRIPT += '''<script>var img_agent_reaction = [];var dict_img_agent_reaction_lenghts = []; var list_reaction_translations = []; var time_out_reaction;var time_out_reaction_delay = 20000;$(document).ready(function(){$("input:text").focus(function() { $(this).select(); } );var img_agent = document.getElementById("agent");var chat = document.getElementById("input-chat");'''
    PAGE_SPRIPT += 'img_agent_reaction.push(["normal","External/bot/agent/normal.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["normal","External/bot/agent/normal_2.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["normal","External/bot/agent/normal_3.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["happy","External/bot/agent/happy.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["happy","External/bot/agent/happy_2.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["happy","External/bot/agent/happy_3.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["angry","External/bot/agent/angry.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["angry","External/bot/agent/angry_2.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["sad","External/bot/agent/sad.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["sad","External/bot/agent/sad_2.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["surprised","External/bot/agent/surprised.png"]);'
    PAGE_SPRIPT += 'img_agent_reaction.push(["surprised","External/bot/agent/surprised_2.png"]);'
    PAGE_SPRIPT += 'list_reaction_translations.push(["kkk","happy"]);'
    PAGE_SPRIPT += 'list_reaction_translations.push([":P","happy"]);'
    PAGE_SPRIPT += 'list_reaction_translations.push(["fdp","angry"]);'
    PAGE_SPRIPT += 'list_reaction_translations.push(["sexy","surprised"]);'

    PAGE_SPRIPT += '''for (id in img_agent_reaction) {if(img_agent_reaction[id][0] in dict_img_agent_reaction_lenghts){var value = dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]];dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]] = value + 1;}else{dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]] = 1;}}img_agent.src = GetImageReaction("normal"); time_out_reaction = setTimeout(function(){ SetImageReaction("normal"); }, time_out_reaction_delay); });'''
    PAGE_SPRIPT += '''\nfunction GetWindowsCenter(target){return Math.max(0, (($(window).width() - $(target).outerWidth()) / 2) + $(window).scrollLeft());}'''
    PAGE_SPRIPT += '''\nfunction SetImageReaction(feeling){console.log(feeling);clearTimeout(time_out_reaction);var img_agent = document.getElementById("agent");img_agent.src = GetImageReaction(feeling); time_out_reaction = setTimeout(function(){ SetImageReaction("normal"); }, time_out_reaction_delay);  img_agent.style.marginLeft = (GetWindowsCenter(img_agent)*(GetNewPosition()/100)).toString() + "px";if(img_agent.classList.contains("effect1") == false){img_agent.classList.remove("effect2");img_agent.classList.add("effect1");}else{img_agent.classList.remove("effect1");img_agent.classList.add("effect2");}}'''
    PAGE_SPRIPT += '''\nfunction GetImageReaction(feeling){var max = dict_img_agent_reaction_lenghts[feeling];var number = MakeRand(0,max-1);var result = img_agent_reaction[0][1];var count = 0;for (id in img_agent_reaction) {if(img_agent_reaction[id][0] == feeling){if(count == number){result = img_agent_reaction[id][1];break;}count = count + 1;}}return result;}'''
    PAGE_SPRIPT += '''\nfunction GetReactionTranslations(text){var result = "normal";for (id in list_reaction_translations) {if(text.toString().indexOf(list_reaction_translations[id][0]) != -1){result = list_reaction_translations[id][1];break;}}return result;}'''
    PAGE_SPRIPT += '''\nfunction GetNewPosition(){return MakeRand(20,50);}'''
    PAGE_SPRIPT += '''\nfunction MakeRand(min, max) {return Math.floor(Math.random() * (max - min + 1) + min);}'''
    PAGE_SPRIPT += '''\nfunction SendChat() {SendMessageBot();}'''
    PAGE_SPRIPT += '''\nfunction SendChat() {SendMessageBot();}function SendMessageBot(){var img_agent = document.getElementById("agent");  var chat = document.getElementById("input-chat"); if(chat.value == "" ||  chat.value == "hum"){chat.value = "hum";}var xhr = new XMLHttpRequest();var data = '{"ask": "' + chat.value + '"}';xhr.open("POST", "''' + str(request.base_url) + '''response''' + '''", true);xhr.setRequestHeader("Accept", "application/json");xhr.setRequestHeader("Content-Type", "application/json");xhr.setRequestHeader("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PUT");xhr.setRequestHeader("Access-Control-Allow-Origin", "''' + str(request.base_url) + '''");xhr.onreadystatechange = function() { if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {	chat.value = xhr.responseText; feeling = GetReactionTranslations(xhr.responseText);SetImageReaction(feeling); chat.focus();}};xhr.send(data);}'''

    PAGE_SPRIPT += '''</script>'''

    res = '<html>' + PAGE_HEAD + PAGE_BODY + PAGE_SPRIPT + '</html>'
    return res

def GetCorrectPath():
    global globalParameter

    globalParameter['PathExecutable'] = sys.executable

    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    os.chdir(dir_path)

    globalParameter['Path'] = dir_path
    globalParameter['PathBackgroud'] = globalParameter['Path'] + '\\External\\bot\\background'
    globalParameter['PathAgentReaction'] = globalParameter['Path'] + '\\External\\bot\\agent'   

    print(globalParameter['Path']) 
    print(globalParameter['PathBackgroud']) 
    print(globalParameter['PathAgentReaction']) 

    ini_file = dir_path + '\\config.ini'
    if(os.path.isfile(ini_file) == True):
        with open(ini_file) as fp:
            config = configparser.ConfigParser()
            config.read_file(fp)
            sections = config.sections()
            if('Parameters' in sections):
                if('PathJarvis' in config['Parameters']):
                    globalParameter['PathJarvis'] = config['Parameters']['PathJarvis']
                if('PathExecutable' in config['Parameters']):
                    globalParameter['PathExecutable'] = config['Parameters']['PathExecutable']
            if('BotImgReaction' in sections):                    
                for key in config['BotImgReaction']:
                    #reaction_xxx = image  
                    globalParameter['BotImgReaction'].append([str(key).split("_")[0], str(config['BotImgReaction'][key])])
                    print([str(key).split("_")[0], str(config['BotImgReaction'][key])])
                    pass  
            if('BotReactionTranslations' in sections):                    
                for key in config['BotReactionTranslations']:
                    #reaction_xxx = expression  
                    globalParameter['BotReactionTranslations'].append([str(key).split("_")[0], str(config['BotReactionTranslations'][key])])
                    print([str(key).split("_")[0], str(config['BotReactionTranslations'][key])])
                    pass                          
                
    jarvis_file = globalParameter['PathJarvis']
    if(os.path.isfile(jarvis_file) == False):
        globalParameter['PathJarvis'] = None
    else:
        print("Jarvis command enabled")

def Run(command, parameters=None, wait=False):
    
    if(globalParameter['PathJarvis'] == None):
        return

    if(parameters != None):
    	proc = subprocess.Popen([command, parameters], stdout=subprocess.PIPE, shell=None)
    else:
    	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=None)

    if(wait == True):
        proc.communicate()

def RunJarvis(tags):
	Run(globalParameter['PathExecutable'] + ' ' + globalParameter['PathJarvis'] + ' ' + tags, None, True)  

def Main():
    """interface chat bot aiml (/bot) | Optional parameters: -p (--port) to select target port"""

    global globalParameter

    GetCorrectPath()

    try:
        if(globalParameter['MAINWEBSERVER'] == True):
            #app.run(host = str(globalParameter['LocalIp']),port=globalParameter['LocalPort'], ssl_context='adhoc') 
            app.run(host = str(globalParameter['LocalIp']),port=globalParameter['LocalPort']) 
        pass
    except:
        print('error webservice')
    
if __name__ == '__main__':   
    #os.chdir(os.path.dirname('C:\\Jarvis\\Output\\'))   

    parser = argparse.ArgumentParser(description=Main.__doc__)
    parser.add_argument('-d','--description', help='Description of program', action='store_true')
    parser.add_argument('-u','--tests', help='Execute tests', action='store_true')
    parser.add_argument('-t','--train', help='Active autotrain', action='store_true')
    parser.add_argument('-l','--bootloop', help='Chatbot in loop', action='store_true')
    parser.add_argument('-r','--bootresponse', help='Chatbot response input', action='store_true')
    parser.add_argument('-p','--port', help='Service running in target port')
    parser.add_argument('-a','--address', help='Service running in target address')    
    
    
    args, unknown = parser.parse_known_args()
    args = vars(args)
    train = False 

    param = ' '.join(unknown)
    dialog = ' '.join(unknown)
    
    if args['description'] == True:
        print(Main.__doc__)
        sys.exit()

    if args['tests'] == True:       
        suite = unittest.TestSuite()
        suite.addTest(TestCases("test_dump")) 
        runner = unittest.TextTestRunner()
        runner.run(suite)          
        sys.exit()     

    if args['train'] == True:       
        train = True 

    if args['bootloop'] == True:       
        ChatBotLoop(train)
        sys.exit()           

    if args['bootresponse'] == True:       
        print(BotResponse(dialog))
        sys.exit()                             

    if args['port'] is not None:
        print('TargetPort: ' + args['port'])
        globalParameter['LocalPort'] = args['port']       

    if args['address'] is not None:
        print('TargetAddress: ' + args['address'])
        globalParameter['LocalIp'] = args['address']                    

    Main()