import random
import globalsub
import glob
from pathlib import Path
from chatbot import *
   
#Enable command jarvis
globalParameter['BotCommandJarvis'] = "[Jarvis]"

#Loading in GetCorrectPath()
globalParameter['Path'] = None
globalParameter['PathBackground'] = None
globalParameter['PathAgentReaction'] = None
globalParameter['CurrentAgent'] = "agent-100"
globalParameter['CurrentBackground'] = "background-000"

globalParameter['LocalPort'] = 8821
globalParameter['LocalIp'] = "0.0.0.0"
globalParameter['MAINWEBSERVER'] = True
globalParameter['PathDB'] = "db.sqlite3"
globalParameter['maximum_similarity_threshold'] = 0.80
globalParameter['BotIp'] = None

globalParameter['BotImgReaction'] = []
globalParameter['BotReactionTranslations'] = []
globalParameter['CommonStatus'] = 'normal'

globalParameter['MenuLinks'] = []
globalParameter['MenuCommands'] = []

globalParameter['flaskstatic_folder'] = 'External'
globalParameter['background'] = None
globalParameter['img_max_height_mobile'] = '180%'
globalParameter['img_max_height_web'] = '100%'
globalParameter['img_max_width_mobile'] = '110%'
globalParameter['img_max_width_web'] = '100%'
globalParameter['chat_height_web'] = '2em'
globalParameter['chat_height_mobile'] = '2em'
globalParameter['chat_font_height_web'] = 'medium'
globalParameter['chat_font_height_mobile'] = 'xx-large'
globalParameter['max_width_web'] = '1200px'

def description2():
    return str(MainLocal.__doc__) + " | ip server : " +  str(globalParameter['LocalIp']) + ":" + str(globalParameter['LocalPort'])

@app.route('/reload')
def ReloadParameters():
    LoadVarsIni2()
    return 'ok'

@app.route('/bot')
def makePageBot():
    global globalParameter

    if(globalParameter['BotIp'] == None):
        globalParameter['BotIp'] = str(request.url_root)
    elif globalParameter['BotIp'].find("http") < 0:
        globalParameter['BotIp'] =  "http://" +  globalParameter['BotIp'] + "/"
        pass
    botresponse = globalParameter['BotIp'] + "botresponse" 
    botresponsecommand = str(request.url_root) + "/botresponsecommand"

    Randbackground()

    ext_bootstrap_css = 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css'
    ext_jquery_js = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'
    ext_bootstrap_js = 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js'    
    ext_font_awesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
    background = globalParameter['background']
    img_max_height_mobile = globalParameter['img_max_height_mobile']
    img_max_height_web = globalParameter['img_max_height_web']
    img_max_width_mobile = globalParameter['img_max_width_mobile']
    img_max_width_web = globalParameter['img_max_width_web']
    chat_height_web = globalParameter['chat_height_web']
    chat_height_mobile = globalParameter['chat_height_mobile']
    chat_font_height_web = globalParameter['chat_font_height_web']
    chat_font_height_mobile = globalParameter['chat_font_height_mobile']
    max_width_web = globalParameter['max_width_web']
    
    PAGE_HEAD = '<head>'
    PAGE_STYLE = '<style>'
    PAGE_STYLE += 'html, body {background: url("' + background + '") no-repeat center center fixed; -webkit-background-size: cover;-moz-background-size: cover;-o-background-size: cover;background-size: cover;} '
    PAGE_STYLE += '#responsive-imgs img {display: block;margin: 1px auto;} '
    PAGE_STYLE += '@media screen and (max-width: ' + max_width_web + ') {.responsive-imgs-resp img { max-width: ' + img_max_width_mobile + '; max-height: ' + img_max_height_mobile + ';} #input-chat, #buttonchat, #responsechat {line-height: ' + chat_height_mobile + ';font-size: ' + chat_font_height_mobile + ';} } '
    PAGE_STYLE += '@media screen and (min-width: ' + max_width_web + ') {.responsive-imgs-resp img { max-width: ' + img_max_width_web + '; max-height: ' + img_max_height_web + ';}  #input-chat, #buttonchat, #responsechat {line-height: ' + chat_height_web + ';font-size: ' + chat_font_height_web + ';} } '
    PAGE_STYLE += '.effect1 {animation-name:img-ani1;animation-duration: 2s; animation-timing-function: ease-in;}.effect2 {animation-name:img-ani2;animation-duration: 2s; animation-timing-function: ease-in;}@keyframes img-ani1 {from{opacity:0;}to{opacity: 1;}}@keyframes img-ani2 {from{opacity:0;}to{opacity: 1;}} '
    PAGE_STYLE += '.chat {z-index: 1500;display: block;margin: 20px auto;max-width: 90%;} '
    PAGE_STYLE += '.maxup {z-index: 3000}'
    PAGE_STYLE += '</style>'
    PAGE_STYLE += '<link href="' + ext_bootstrap_css + '" rel="stylesheet" crossorigin="anonymous"><script src="' + ext_jquery_js + '"></script>'
    PAGE_STYLE += '<link rel="stylesheet" href="' + ext_font_awesome + '">'
    PAGE_HEAD = PAGE_HEAD + PAGE_STYLE + '</head>'

    PAGE_BODY = '<body>'

    PAGE_BODY += '<div class="dropdown maxup">'

    #links
    PAGE_BODY += '<button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
    PAGE_BODY += '<i class="fa fa-bars"></i>'
    #PAGE_BODY += '<i class="fa fa-external-link" aria-hidden="true"></i>'
    PAGE_BODY += '</button>'
    PAGE_BODY += '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
    for list_links in globalParameter['MenuLinks']:
        PAGE_BODY += '<a class="dropdown-item" href="' + list_links[1] + '" target="_blank">' + list_links[0] + '</a>'  
    PAGE_BODY += '</div>'

    #command
    if(globalParameter['PathJarvis'] != None):
        PAGE_BODY += '<button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
        PAGE_BODY += '<i class="fa fa-terminal" aria-hidden="true"></i>'
        PAGE_BODY += '</button>'
        PAGE_BODY += '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'

        PAGE_BODY += """<a class="dropdown-item" onclick="SendMessageInputChat('[img] link_image [base|tags] db tags')" href="#">Example send image for db</a>"""
        PAGE_BODY += """<a class="dropdown-item" onclick="SendMessageInputChat('[jsonlink] link [base|tags] db tags')" href="#">Example send link json for db</a>"""
        PAGE_BODY += '<div class="dropdown-divider"></div>'
        for list_links in globalParameter['MenuCommands']:
            PAGE_BODY += """<a class="dropdown-item" onclick="SendMessageInputChat('"""+ globalParameter['BotCommandJarvis'] + """ """ + list_links[1] + """')" href="#">""" + list_links[0] + """</a>"""
        PAGE_BODY += '</div>'

    #points
    PAGE_BODY += '''
        <div style="margin-left: 80%; margin-right: 5%; position: relative; overflow-y: auto; max-height:70%;"> 
            <div style="height: 100px; background-color: rgba(255, 255, 255, 0.4);" id="score"> 
                score
            </div>
            &nbsp;
        </div>
    
    '''
    
    PAGE_BODY += '</div>'

    PAGE_BODY += '''
        <div id="responsive-imgs" class="responsive-imgs-resp">
            <img id="agent" class="fixed-bottom">
        </div>
        <div class="chat fixed-bottom">
            <div id="responsechat" style="background-color: rgba(255, 255, 255, 0.4);margin: 10px auto;"> 
                response
            </div>
            <div class="input-group input-space">
                <input type="text" id="input-chat" class="form-control" placeholder="chat with me" aria-label="chat with me" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <span class="input-group-text" id="basic-addon2">
                        <a id="buttonchat" href="#" onclick="SendChat();return false;">chat</a>
                    </span>
                </div>
            </div>
        </div>
    '''
    PAGE_BODY += '</body>'

    PAGE_SPRIPT = '<script src="' + ext_bootstrap_js + '" crossorigin="anonymous"></script>'
    PAGE_SPRIPT += '''<script>var img_agent_reaction = [];var dict_img_agent_reaction_lenghts = []; var list_reaction_translations = []; var time_out_reaction;var time_out_reaction_delay = 20000;$(document).ready(function(){$("input:text").focus(function() { $(this).select(); } );var img_agent = document.getElementById("agent");var chat = document.getElementById("input-chat");'''

    for list_img_reaction in globalParameter['BotImgReaction']:
        PAGE_SPRIPT += 'img_agent_reaction.push(["' + list_img_reaction[0] + '","' + list_img_reaction[1] + '"]);'    

    for list_reaction_translations in globalParameter['BotReactionTranslations']:
        PAGE_SPRIPT += 'list_reaction_translations.push(["' + list_reaction_translations[1] + '","' + list_reaction_translations[0] + '"]);'    

    PAGE_SPRIPT += '''for (id in img_agent_reaction) {if(img_agent_reaction[id][0] in dict_img_agent_reaction_lenghts){var value = dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]];dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]] = value + 1;}else{dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]] = 1;}}img_agent.src = GetImageReaction("normal"); time_out_reaction = setTimeout(function(){ SetImageReaction("normal"); }, time_out_reaction_delay); });'''
    PAGE_SPRIPT += '''\nfunction GetWindowsCenter(target){return Math.max(0, (($(window).width() - $(target).outerWidth()) / 2) + $(window).scrollLeft());}'''
    PAGE_SPRIPT += '''\nfunction SetImageReaction(feeling){console.log(feeling);clearTimeout(time_out_reaction);var img_agent = document.getElementById("agent");img_agent.src = GetImageReaction(feeling); time_out_reaction = setTimeout(function(){ SetImageReaction("normal"); }, time_out_reaction_delay);  img_agent.style.marginLeft = (GetWindowsCenter(img_agent)*(GetNewPosition()/100)).toString() + "px";if(img_agent.classList.contains("effect1") == false){img_agent.classList.remove("effect2");img_agent.classList.add("effect1");}else{img_agent.classList.remove("effect1");img_agent.classList.add("effect2");}}'''
    PAGE_SPRIPT += '''\nfunction GetImageReaction(feeling){var max = dict_img_agent_reaction_lenghts[feeling];var number = MakeRand(0,max-1);var result = img_agent_reaction[0][1];var count = 0;for (id in img_agent_reaction) {if(img_agent_reaction[id][0] == feeling){if(count == number){result = img_agent_reaction[id][1];break;}count = count + 1;}}return result;}'''
    PAGE_SPRIPT += '''\nfunction GetReactionTranslations(text){var result = "''' + globalParameter['CommonStatus'] +'''";for (id in list_reaction_translations) {if(text.toString().indexOf(list_reaction_translations[id][0]) != -1){result = list_reaction_translations[id][1];break;}}return result;}'''
    PAGE_SPRIPT += '''\nfunction GetNewPosition(){return MakeRand(20,50);}'''
    PAGE_SPRIPT += '''\nfunction MakeRand(min, max) {return Math.floor(Math.random() * (max - min + 1) + min);}'''
    PAGE_SPRIPT += '''\nfunction SendChat() {SendMessageBot();}'''
    PAGE_SPRIPT += '''\nfunction SendMessageInputChat(text) {document.getElementById("input-chat").value=text}'''
    PAGE_SPRIPT += '''\nfunction SendMessageBot(){var img_agent = document.getElementById("agent");  var chat = document.getElementById("input-chat"); var link = "''' + botresponse + '''"; if(chat.value == "" ||  chat.value == "hum"){chat.value = "hum";}; if(chat.value.indexOf("''' + globalParameter['BotCommandJarvis'] + '''") > -1) { link = "''' + botresponsecommand + '''";}; var xhr = new XMLHttpRequest();var data = '{"ask": "' + chat.value + '"}';xhr.open("POST", link, true);xhr.setRequestHeader("Accept", "application/json");xhr.setRequestHeader("Content-Type", "application/json");xhr.setRequestHeader("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PUT");xhr.setRequestHeader("Access-Control-Allow-Origin", link);xhr.onreadystatechange = function() { if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {	chat.value = xhr.responseText; feeling = GetReactionTranslations(xhr.responseText);SetImageReaction(feeling); chat.focus();chat.select();}};xhr.send(data);}'''

    PAGE_SPRIPT += '''</script>'''
    #PAGE_SPRIPT += '''<script>var input = document.getElementById("input-chat");input.addEventListener("keyup", function(event) {if (event.keyCode == 13) { SendChat();input.focus();}; if (event.keyCode == 8 || event.keyCode == 46) {input.value=''}; });</script>'''
    PAGE_SPRIPT += '''<script>var chat = document.getElementById("input-chat");chat.addEventListener("keyup", function(event) {if (event.keyCode == 13) { SendChat();}; });</script>'''

    res = '<html>' + PAGE_HEAD + PAGE_BODY + PAGE_SPRIPT + '</html>'
    return res

@app.route('/botresponsecommand',methods = ['POST', 'GET'])
def botresponsecommand():
    if request.method == 'POST':
        data = request.get_json(force=True)  
        print(data['ask'])

        if(globalParameter['PathJarvis'] == None):
            return 'Command not implemented'

        RunJarvis(str(data['ask']).replace(globalParameter['BotCommandJarvis'], ""))

        return 'Command accepted!'

def Randbackground():
    backgrounds = []
    for _background in glob.glob(os.path.join(globalParameter['PathBackground'], "*.png")):
        backgrounds.append(globalParameter['flaskstatic_folder'] + _background.split(globalParameter['flaskstatic_folder'])[1])
    globalParameter['background'] = backgrounds[random.randint(0, len(backgrounds)-1)].replace('\\','//')
    #print(globalParameter['background'])

def OrganizeParameters():    
    backgrounds = []

    print(globalParameter['PathBackground'])

    for _background in glob.glob(os.path.join(globalParameter['PathBackground'], "*.png")):
        backgrounds.append(globalParameter['flaskstatic_folder'] + _background.split(globalParameter['flaskstatic_folder'])[1])
    globalParameter['background'] = backgrounds[random.randint(0, len(backgrounds)-1)].replace('\\','//')
    #print(globalParameter['background'])


    for _imgReaction in glob.glob(os.path.join(globalParameter['PathAgentReaction'], "*.png")):
        filename = Path(_imgReaction).stem
        globalParameter['BotImgReaction'].append([str(filename).split("_")[0], str(globalParameter['flaskstatic_folder'] + _imgReaction.split(globalParameter['flaskstatic_folder'])[1].replace('\\','//'))])
    #print(globalParameter['BotImgReaction'])

def LoadVarsIni2(config,sections):
    global globalParameter

    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    os.chdir(dir_path)    

    globalParameter['Path'] = dir_path
    globalParameter['PathBackground'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentBackground'] )
    globalParameter['PathAgentReaction'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentAgent'])

    if('BotImgReaction' in sections):                    
        for key in config['BotImgReaction']:
            #reaction_xxx = image  
            #preference for loading image reactions
            globalParameter['BotImgReaction'].append([str(key).split("_")[0], str(config['BotImgReaction'][key])])
            print([str(key).split("_")[0], str(config['BotImgReaction'][key])])
            pass  
    if('BotReactionTranslations' in sections):                    
        for key in config['BotReactionTranslations']:
            #reaction_xxx = expression  
            globalParameter['BotReactionTranslations'].append([str(key).split("_")[0], str(config['BotReactionTranslations'][key])])
            print([str(key).split("_")[0], str(config['BotReactionTranslations'][key])])
            pass       

    if('MenuLinks' in sections):            
        globalParameter['MenuLinks'].clear()      
        for key in config['MenuLinks']:
            try:
                #my link = https:\\www.meulink.com.br
                globalParameter['MenuLinks'].append([str(key), str(config['MenuLinks'][key])])
                print([str(key), str(config['MenuLinks'][key])])
                pass
            except:
                pass                                      

    if('MenuCommands' in sections):            
        globalParameter['MenuCommands'].clear()      
        for key in config['MenuCommands']:
            #try:
            #my command = calc
            globalParameter['MenuCommands'].append([str(key), str(config['MenuCommands'][key])])
            print([str(key), str(config['MenuCommands'][key])])
            pass
            #except:
            #    pass  

def MainLocal():
    """interface chat bot aiml (/bot) | Optional parameters: -p (--port) to select target port"""

    global globalParameter

    globalsub.subs(LoadVarsIni, LoadVarsIni2)
    globalsub.subs(description, description2)    

    GetCorrectPath()

    OrganizeParameters()

    jarvis_file = globalParameter['PathJarvis']
    if(globalParameter['PathJarvis']!= None and os.path.isfile(jarvis_file) == False):
        globalParameter['PathJarvis'] = None
    else:
        print("Jarvis command enabled")

    try:
        if(globalParameter['MAINWEBSERVER'] == True):
            #app.run(host = str(globalParameter['LocalIp']),port=globalParameter['LocalPort'], ssl_context='adhoc') 
            app.run(host = str(globalParameter['LocalIp']),port=globalParameter['LocalPort']) 
        pass
    except:
        print('error webservice')


if __name__ == '__main__':   
    os.chdir(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(description=Main.__doc__)
    parser.add_argument('-d','--description', help='Description of program', action='store_true')
    parser.add_argument('-u','--tests', help='Execute tests', action='store_true')
    parser.add_argument('-t','--train', help='Active autotrain', action='store_true')
    parser.add_argument('-r','--bootresponse', help='Chatbot response input', action='store_true')
    parser.add_argument('-p','--port', help='Service running in target port')
    parser.add_argument('-a','--address', help='Service running in target address')    
    parser.add_argument('-c','--config', help='Config.ini file')    

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

    if args['bootresponse'] == True:       
        print(BotResponse(dialog))
        sys.exit()                             

    if args['port'] is not None:
        print('TargetPort: ' + args['port'])
        globalParameter['LocalPort'] = args['port']       

    if args['address'] is not None:
        print('TargetAddress: ' + args['address'])
        globalParameter['LocalIp'] = args['address']                    

    if args['config'] is not None:
        print('Config.ini: ' + args['config'])
        globalParameter['configFile'] = args['config']  

    MainLocal()