import random
import globalsub
import glob
from pathlib import Path
from chatbot import *
import json
import shutil
   
#Enable command jarvis
globalParameter['BotCommandJarvis'] = "[Jarvis]"
globalParameter['BotCommandLearn'] = "[learn]"

#Loading in GetCorrectPath()
globalParameter['Path'] = None
globalParameter['PathBackground'] = None
globalParameter['PathPhotobook'] = None
globalParameter['PathAgentReaction'] = None
globalParameter['CurrentAgent'] = "agent-100"
globalParameter['CurrentBackground'] = "background-000"
globalParameter['CurrentPhotobook'] = None

globalParameter['LocalPort'] = 8821
globalParameter['LocalIp'] = "0.0.0.0"
globalParameter['MAINWEBSERVER'] = True
globalParameter['PathDB'] = "db.sqlite3"
globalParameter['maximum_similarity_threshold'] = 0.80
globalParameter['BotIp'] = None

globalParameter['PhotobookImgs'] = []

globalParameter['BotImgReaction'] = []
globalParameter['BotReactionTranslations'] = []
globalParameter['BotReactionPoints'] = []
globalParameter['BotReactionLevels'] = []
globalParameter['CommonStatus'] = 'normal'
globalParameter['MinimumValueToAddTagInAsks'] = 100000000
globalParameter['HideChatIfButtons'] = True
globalParameter['GlobalTimerLimit'] = -1

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
    OrganizeParameters()
    return 'ok'

def BotReactionPoints2Text():
    global globalParameter

    points_text = ""
    for i in range(0,len(globalParameter['BotReactionPoints'])):
        if globalParameter['BotReactionPoints'][i][0] == globalParameter['CommonStatus']:
            continue

        points_text = points_text + " " + str(globalParameter['BotReactionPoints'][i][0]) + ": " + str(globalParameter['BotReactionPoints'][i][1]) + "<br>"

    return points_text

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
    botreactionpoints = str(request.url_root) + "/botreactionpoints" 

    Randbackground()

    ext_bootstrap_css = 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css'
    ext_jquery_js = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'
    ext_bootstrap_js = 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js'    
    ext_font_awesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
    ext_popper = 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js'    

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
    PAGE_STYLE += '.hidden {display: none;} '
    PAGE_STYLE += '.effect1 {animation-name:img-ani1;animation-duration: 2s; animation-timing-function: ease-in;}.effect2 {animation-name:img-ani2;animation-duration: 2s; animation-timing-function: ease-in;}@keyframes img-ani1 {from{opacity:0;}to{opacity: 1;}}@keyframes img-ani2 {from{opacity:0;}to{opacity: 1;}} '
    PAGE_STYLE += '.chat {z-index: 1500;display: block;margin: 20px auto;max-width: 90%;} '
    PAGE_STYLE += '.maxup {z-index: 3000}'
    PAGE_STYLE += '</style>'
    PAGE_STYLE += '<link href="' + ext_bootstrap_css + '" rel="stylesheet" crossorigin="anonymous">'
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

    #images
    PAGE_BODY += '<button class="btn btn-secondary" type="button" id="buttonmodal1">'
    PAGE_BODY += '<i class="fa fa-picture-o" aria-hidden="true"></i>'
    PAGE_BODY += '</button>'

    #points
    PAGE_BODY += '''
        <div style="margin-left: 80%; margin-right: 5%; position: relative; overflow-y: auto; max-height:70%;"> 
            <div style="background-color: rgba(255, 255, 255, 0.7);" id="score"> 
                ''' + BotReactionPoints2Text() + '''
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
            <div id="chat_button_3" class="input-group input-space" style="visibility:hidden;">
                <input type="button" id="button_3" class="form-control" value="3" onclick="SendChatButton('button_3');return false;">
            </div>
            <div id="chat_button_2" class="input-group input-space" style="visibility:hidden;">
                <input type="button" id="button_2" class="form-control" value="2" onclick="SendChatButton('button_2');return false;">
            </div>
            <div id="chat_button_1" class="input-group input-space" style="visibility:hidden;">
                <input type="button" id="button_1" class="form-control" value="1" onclick="SendChatButton('button_1');return false;">
            </div>
            <div id="chat_button_0" class="input-group input-space" onclick="SendChatButton('button_0');return false;" style="visibility:hidden;">
                <input type="button" id="button_0" class="form-control" value="0">
            </div>        
            <div id="responsechat" style="background-color: rgba(255, 255, 255, 0.4);margin: 10px auto;">                  
            </div>
            <div id="chat_input_00" class="input-group input-space">
                <input type="text" id="input-chat" class="form-control" placeholder="chat with me" aria-label="chat with me" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <span class="input-group-text" id="basic-addon2">
                        <a id="buttonchat" href="#">chat</a>
                    </span>
                </div>
            </div>
        </div>

    '''

    PAGE_BODY += '''    
        <div class="modal fade" id="modal1" style="z-index:10000" tabindex="1000 role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">Photos</div>
                    <div class="modal-body">
                        <div id="divmodal1">
                            <img id="imgmodal1" style="width:100%">

                            <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
                                <div class="carousel-indicators" id="carousel-indicators-000"> 

                                </div>
                                <div class="carousel-inner" id="carousel-inner-000">
                                                                                                           
                                </div>
                                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
                                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">Previous</span>
                                </button>
                                <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
                                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">Next</span>
                                </button>
                            </div>


                        </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
    '''

    PAGE_BODY += '''    
        <div class="modal fade" id="modal2" style="z-index:10000" tabindex="1000 role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header" id="txtmodal2">test</div>
                    <div class="modal-body">
                        <div id="divmodal2">
                            <img id="imgmodal2" style="width:100%">
                        </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
    '''

    PAGE_BODY += '</body>'

    PAGE_SPRIPT = '<script src="' + ext_popper + '" crossorigin="anonymous"></script>'
    PAGE_SPRIPT += '<script src="' + ext_bootstrap_js + '" crossorigin="anonymous"></script>'
    PAGE_SPRIPT += '<script src="' + ext_jquery_js + '"></script>'
    PAGE_SPRIPT += '''<script>
        var img_agent_reaction = [];
        var dict_img_agent_reaction_lenghts = [];
        var list_reaction_translations = [];
        var list_reaction_tags = [];
        var time_out_reaction;
        var time_out_reaction_delay = 20000;
        var top_reaction = '';

        var chat_animation = [];
        chat_animation.push(".....");
        chat_animation.push("·....");
        chat_animation.push(".·...");
        chat_animation.push("..·..");
        chat_animation.push("...·.");
        chat_animation.push("....·");
        var chat_animation_id = 0;

        $(document).ready(function(){$("input:text").focus(function() { $(this).select(); } );

        var img_agent = document.getElementById("agent");
        var chat = document.getElementById("input-chat");        
    '''

    if(len(globalParameter['PhotobookImgs'])>0):

        carouselIndicators = ""
        carouselInner = ""
        id = 0
        for photo in globalParameter['PhotobookImgs']:
            
            if(id == 0):
                carouselIndicators += '<button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="' + str(id) + '" class="active" aria-current="true" aria-label="Slide ' + str(id) + '"></button>'
                carouselInner +='<div class="carousel-item active">'
            else:
                carouselIndicators += '<button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="' + str(id) + '" aria-current="true" aria-label="Slide ' + str(id) + '"></button>'
                carouselInner +='<div class="carousel-item">'

            carouselInner +='<img src="' + photo + '" class="d-block w-100" alt="...">'
            carouselInner +='</div> '

            id = id+1

        PAGE_SPRIPT += '''
            document.getElementById("buttonmodal1").onclick = function() {
                $('#modal1').modal('show');
                document.getElementById("carousel-indicators-000").innerHTML=`''' + carouselIndicators + ''' `;
                                       
                document.getElementById("carousel-inner-000").innerHTML=`''' + carouselInner + '''`;
            }   
        '''

    for list_img_reaction in globalParameter['BotImgReaction']:
        PAGE_SPRIPT += 'img_agent_reaction.push(["' + list_img_reaction[0] + '","' + list_img_reaction[1] + '"]);'    
        PAGE_SPRIPT += 'list_reaction_tags.push("' + list_img_reaction[0] + '");'

    for list_reaction_translations in globalParameter['BotReactionTranslations']:
        PAGE_SPRIPT += 'list_reaction_translations.push(["' + list_reaction_translations[1] + '","' + list_reaction_translations[0] + '"]);'    

    PAGE_SPRIPT += '''for (id in img_agent_reaction) {if(img_agent_reaction[id][0] in dict_img_agent_reaction_lenghts){var value = dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]];dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]] = value + 1;}else{dict_img_agent_reaction_lenghts[img_agent_reaction[id][0]] = 1;}}img_agent.src = GetImageReaction("normal"); time_out_reaction = setTimeout(function(){ SetImageReaction("normal"); }, time_out_reaction_delay); });'''
    PAGE_SPRIPT += '''\nfunction GetWindowsCenter(target){return Math.max(0, (($(window).width() - $(target).outerWidth()) / 2) + $(window).scrollLeft());}'''
    PAGE_SPRIPT += '''\nfunction SetImageReaction(feeling){console.log(feeling);clearTimeout(time_out_reaction);var img_agent = document.getElementById("agent");img_agent.src = GetImageReaction(feeling); time_out_reaction = setTimeout(function(){ SetImageReaction("normal"); }, time_out_reaction_delay);  img_agent.style.marginLeft = (GetWindowsCenter(img_agent)*(GetNewPosition()/100)).toString() + "px";if(img_agent.classList.contains("effect1") == false){img_agent.classList.remove("effect2");img_agent.classList.add("effect1");}else{img_agent.classList.remove("effect1");img_agent.classList.add("effect2");}}'''
    PAGE_SPRIPT += '''\nfunction GetImageReaction(feeling){
        var max = dict_img_agent_reaction_lenghts[feeling];
        var number = MakeRand(0,max-1);
        var result = img_agent_reaction[0][1];
        var count = 0;
        for (id in img_agent_reaction) 
        {
            if(img_agent_reaction[id][0] == feeling)
            {
                if(count == number)
                {
                    result = img_agent_reaction[id][1];
                    break;
                }
                count = count + 1;
            }
        }return result;
    }'''
    PAGE_SPRIPT += '''\nfunction GetReactionTranslations(text)
    {
        var result = "''' + globalParameter['CommonStatus'] +'''";
        for (id in list_reaction_translations) 
        {
            if(text.toString().indexOf(list_reaction_translations[id][0]) != -1)
            {
                result = list_reaction_translations[id][1];
                break;
            }
        }

        if(result == "''' + globalParameter['CommonStatus'] +'''")
        {
            for (id in list_reaction_tags) 
            {
                if(text.toString().indexOf('[' + list_reaction_tags[id] + ']') != -1)
                {
                    result = list_reaction_tags[id];
                    break;
                }
            }
        }        
        return result;
    }'''

    PAGE_SPRIPT += '''\nfunction GetTags(text)
    {
        var result = text;

        for (id in list_reaction_tags) 
        {
            result = result.replace('[' + list_reaction_tags[id] + ']', "");
        }        

        //image
        var response = result.split("[image]");
        if(response.length>1)
        {
            result= response[0];
            image = response[1];
            document.getElementById("txtmodal2").innerHTML=result;
            document.getElementById("imgmodal2").src=image;
            $('#modal2').modal('show');
        }    

        //buttons
        buttonshow('chat_button_0');
        buttonshow('chat_button_1');
        buttonshow('chat_button_2');
        buttonshow('chat_button_3');        

        var response = result.split("[button]");
        if(response.length>1)
        {
        ''' 
    if(globalParameter["HideChatIfButtons"]==True):
        PAGE_SPRIPT += '''document.getElementById("chat_input_00").style.visibility = "hidden";'''
    
    PAGE_SPRIPT += '''
            buttons = response.slice(1);
            result= response[0];

            for (let i=0; i<Math.min(buttons.length,4); i++)  {
                buttonshow('chat_button_' + i.toString(), 'button_' + i.toString(), true, buttons[i]); 
            }
        }

        return result;
    }'''
    PAGE_SPRIPT += '''\nfunction SendChatButton(id){
        var text = document.getElementById(id).value;      
        document.getElementById("input-chat").value = text;
        SendChat();
    }'''
    PAGE_SPRIPT += '''\nfunction GetNewPosition(){return MakeRand(20,50);}'''
    PAGE_SPRIPT += '''\nfunction MakeRand(min, max) {return Math.floor(Math.random() * (max - min + 1) + min);}'''
    PAGE_SPRIPT += '''\nfunction SendChat() {SendMessageBot(); document.getElementById("chat_input_00").style.visibility = "visible";}'''
    PAGE_SPRIPT += '''\nfunction SendMessageInputChat(text) {document.getElementById("input-chat").value=text}'''
    PAGE_SPRIPT += '''
        function buttonshow(_div, _button="none", show=false, bt_value="button") {
        
            if(show==true)
            {
                document.getElementById(_div).style.visibility = "visible";
                document.getElementById(_button).value = bt_value;
            }
            else
            {
                document.getElementById(_div).style.visibility = "hidden";
            }
            //document.getElementById(id).style.width = "100%";
        }
    '''    
    PAGE_SPRIPT += '''\nfunction ChatAnimation()
    {
        var response_chat = document.getElementById("responsechat");

        response_chat.innerHTML = chat_animation[chat_animation_id];
        chat_animation_id = chat_animation_id + 1;
        //console.log(chat_animation_id);

        if(chat_animation.length <= chat_animation_id)
        {
            chat_animation_id = 0;
        }
    }
    '''

    PAGE_SPRIPT += '''\n
        function SendMessageBot(){
            var intervalId = setInterval(ChatAnimation, 500);
            var img_agent = document.getElementById("agent");  
            var chat = document.getElementById("input-chat"); 
            var response_chat = document.getElementById("responsechat");
            var link = "''' + botresponse + '''"; 
            if(chat.value == "" ||  chat.value == "hum"){chat.value = "hum";}; 
            if(chat.value.indexOf("''' + globalParameter['BotCommandJarvis'] + '''") > -1) 
            { link = "''' + botresponsecommand + '''";}; 
            var xhr = new XMLHttpRequest();
            var data = '{"ask": "' + chat.value + '", "acceptTags": "1", "tag": "' + top_reaction + '"}';
            if(chat.value.indexOf("''' + globalParameter['BotCommandLearn'] + '''") > -1 || top_reaction == '' ) 
            var data = '{"ask": "' + chat.value + '", "acceptTags": "1" }';    
            xhr.open("POST", link, true);
            xhr.setRequestHeader("Accept", "application/json");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PUT");
            xhr.setRequestHeader("Access-Control-Allow-Origin", link);
            xhr.onreadystatechange = function() { 
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
                {
                    clearInterval(intervalId);
                    response_chat.innerHTML = GetTags(xhr.responseText); 
                    feeling = GetReactionTranslations(xhr.responseText);
                    SetImageReaction(feeling); 
                    ReactionPoints(feeling);
                    chat.focus();
                    chat.select();
                }
            };
            xhr.send(data);
        }
    '''
    PAGE_SPRIPT += '''\n
        function ReactionPoints(feeling){
            var link = "''' + botreactionpoints + '''"; 
            var xhr = new XMLHttpRequest();
            var score = document.getElementById("score");  
            var ctx = document.getElementById('myChart');  
            
            var data = '{"feeling": "' + feeling + '"}';

            xhr.open("POST", link, true);
            xhr.setRequestHeader("Accept", "application/json");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PUT");
            xhr.setRequestHeader("Access-Control-Allow-Origin", link);
            xhr.onreadystatechange = function() { 
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
                {	
                    var data = JSON.parse(xhr.response);

                    if(data.hasOwnProperty('needreload')){
                        window.location.reload();
                    }
                    else
                    {
                        var points_text = "";
                        var biggest_key = "";
                        var biggest_value = ''' + str(globalParameter['MinimumValueToAddTagInAsks']) + ''';
                        for (let key in data) {
                            points_text = points_text + key + ": " + data[key] + "<br>";
                            console.log(key + ": "+ data[key])

                            var value = parseInt(data[key]);
                            if(value > biggest_value)
                            {
                                biggest_value = value;
                                biggest_key = key;
                            }
                        }
                        score.innerHTML = points_text;
                        top_reaction = biggest_key;
                        console.log("top feeling (after filter): " + biggest_key)
                    } 
                }
            };
            xhr.send(data);     
        }
    '''
    PAGE_SPRIPT += '''</script>'''
    #PAGE_SPRIPT += '''<script>var input = document.getElementById("input-chat");input.addEventListener("keyup", function(event) {if (event.keyCode == 13) { SendChat();input.focus();}; if (event.keyCode == 8 || event.keyCode == 46) {input.value=''}; });</script>'''
    PAGE_SPRIPT += '''<script>var chat = document.getElementById("input-chat");chat.addEventListener("keyup", function(event) {if (event.keyCode == 13) { SendChat();}; });</script>'''
    PAGE_SPRIPT += '''<script>var chatButton = document.getElementById("buttonchat");chatButton.addEventListener("click", function(event) {SendChat();});</script>'''


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

def SaveDataIni():
    ini_file = globalParameter['configFile']
    if(os.path.isfile(ini_file) == True):
        with open(ini_file) as fp:
            config = configparser.ConfigParser()
            config.read_file(fp)
            sections = config.sections()    

            for _botreactionpoints in globalParameter['BotReactionPoints']:
                config['BotReactionPoints'][_botreactionpoints[0]] = str(_botreactionpoints[1])
        
        with open(ini_file, 'w') as fp:
            config.write(fp) 

                            
@app.route('/botreactionpoints',methods = ['POST', 'GET'])
def botreactionpoints():
    global globalParameter

    data_res = {}
    needreload = False
    timer = -1

    if request.method == 'POST':
        data = request.get_json(force=True)  
        feeling = data['feeling']

        for i in range(0,len(globalParameter['BotReactionPoints'])):
            key = globalParameter['BotReactionPoints'][i][0]        

            if key == 'timer':
                count = globalParameter['BotReactionPoints'][i][1]
                globalParameter['BotReactionPoints'][i] = [key,count+1]
                timer = count + 1               

            if key == globalParameter['CommonStatus']:
                continue

            if key == feeling:
                count = globalParameter['BotReactionPoints'][i][1]
                globalParameter['BotReactionPoints'][i] = [key,count+1]
        
            data_res[globalParameter['BotReactionPoints'][i][0]] = globalParameter['BotReactionPoints'][i][1]

        if(timer < 0):
            globalParameter['BotReactionPoints'].append(['timer', 1])

        if(int(globalParameter['GlobalTimerLimit'])>0 and timer>int(globalParameter['GlobalTimerLimit'])):
            #globalreset
            for i in range(0,len(globalParameter['BotReactionPoints'])):
                key = globalParameter['BotReactionPoints'][i][0]
                count = 0
                globalParameter['BotReactionPoints'][i] = [key,count]
            needreload=True
            SaveDataIni()
            GetCorrectPath()

        SaveDataIni()
        
        if(Checklevel()==True):
            needreload = True

        if(needreload == True):
            data_res["needreload"] = 1
            OrganizeParameters()

        pass   
    else:
        pass
    
    result = app.response_class(
        response=json.dumps(data_res),
        status=200,
        mimetype='application/json'
    )

    return result

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

    globalParameter['BotImgReaction'].clear()
    _imgReactionList = glob.glob(os.path.join(globalParameter['PathAgentReaction'], "*.png"))
    _imgReactionList.extend(glob.glob(os.path.join(globalParameter['PathAgentReaction'], "*.gif")))
    _imgReactionList.extend(glob.glob(os.path.join(globalParameter['PathAgentReaction'], "*.jpg")))
    for _imgReaction in _imgReactionList:
        filename = Path(_imgReaction).stem
        globalParameter['BotImgReaction'].append([str(filename).split("_")[0], str(globalParameter['flaskstatic_folder'] + _imgReaction.split(globalParameter['flaskstatic_folder'])[1].replace('\\','//'))])
    
        findReactionPoint = False
        for _botreactionpoints in globalParameter['BotReactionPoints']:
            if _botreactionpoints[0] == str(filename).split("_")[0].split("_")[0]:
                findReactionPoint = True
                break
        
        if(findReactionPoint == False):
            globalParameter['BotReactionPoints'].append([str(filename).split("_")[0].split("_")[0], 0])

    print(globalParameter['BotReactionPoints'])        
    #print(globalParameter['BotImgReaction'])

    globalParameter['PhotobookImgs'].clear()
    _imgPhotobookList = glob.glob(os.path.join(globalParameter['PathPhotobook'], "*.png"))
    _imgPhotobookList.extend(glob.glob(os.path.join(globalParameter['PathPhotobook'], "*.gif")))
    _imgPhotobookList.extend(glob.glob(os.path.join(globalParameter['PathPhotobook'], "*.jpg")))
    for _imgPhotobook in _imgPhotobookList:
        globalParameter['PhotobookImgs'].append(str(globalParameter['flaskstatic_folder'] + _imgPhotobook.split(globalParameter['flaskstatic_folder'])[1].replace('\\','//')))        

def Checklevel():
    global globalParameter

    needReorganize = False

    CurrentBackground = globalParameter['CurrentBackground']
    CurrentAgent = globalParameter['CurrentAgent']
    CurrentPhotobook = globalParameter['CurrentPhotobook']

    for _botreactionlevel in globalParameter['BotReactionLevels']:
        botreactionlevel_feeling = _botreactionlevel[0]
        botreactionlevel_points = _botreactionlevel[1]
        botreactionlevel_target = _botreactionlevel[2]
        botreactionlevel_value = _botreactionlevel[3]
        for _botreactionpoint in globalParameter['BotReactionPoints']:
            botreactionpoint_feeling = _botreactionpoint[0]
            botreactionpoint_points = _botreactionpoint[1]
            
            if(botreactionlevel_feeling != botreactionpoint_feeling):
                continue

            if(int(botreactionlevel_points) > int(botreactionpoint_points)):
                continue

            if(botreactionlevel_target.lower() == "CurrentAgent".lower()):
                globalParameter['CurrentAgent'] = botreactionlevel_value

            if(botreactionlevel_target.lower() == "CurrentBackground".lower()):
                globalParameter['CurrentBackground'] = botreactionlevel_value

            if(botreactionlevel_target.lower() == "CurrentPhotobook".lower()):
                globalParameter['CurrentPhotobook'] = botreactionlevel_value                

    if(CurrentBackground != globalParameter['CurrentBackground'] or CurrentAgent != globalParameter['CurrentAgent'] or CurrentPhotobook != globalParameter['CurrentPhotobook']):
        print('needReorganize')
        globalParameter['PathBackground'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentBackground'] )
        globalParameter['PathAgentReaction'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentAgent'])
        globalParameter['PathPhotobook'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentPhotobook'])
        needReorganize = True

    return needReorganize

def LoadVarsIni2(config,sections):
    global globalParameter

    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    os.chdir(dir_path)    

    globalParameter['Path'] = dir_path
    globalParameter['PathBackground'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentBackground'] )
    globalParameter['PathAgentReaction'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentAgent'])
    globalParameter['PathPhotobook'] = os.path.join(globalParameter['Path'],'External','bot',globalParameter['CurrentPhotobook'])

    if('BotImgReaction' in sections):      
        globalParameter['BotImgReaction'].clear()              
        for key in config['BotImgReaction']:
            #reaction_xxx = image  
            #preference for loading image reactions
            globalParameter['BotImgReaction'].append([str(key).split("_")[0], str(config['BotImgReaction'][key])])
            print([str(key).split("_")[0], str(config['BotImgReaction'][key])])
            pass  
 
    if('BotReactionTranslations' in sections):  
        globalParameter['BotReactionTranslations'].clear()                    
        for key in config['BotReactionTranslations']:
            #reaction_xxx = expression  
            globalParameter['BotReactionTranslations'].append([str(key).split("_")[0], str(config['BotReactionTranslations'][key])])
            print([str(key).split("_")[0], str(config['BotReactionTranslations'][key])])
            pass   

    if('BotReactionPoints' in sections):    
        globalParameter['BotReactionPoints'].clear()                
        for key in config['BotReactionPoints']:
            findReactionPoint = False
            for _botreactionpoints in globalParameter['BotReactionPoints']:
                if _botreactionpoints[0] == key:
                    findReactionPoint = True
                    break
            
            if(findReactionPoint == False):
                globalParameter['BotReactionPoints'].append([key, int(config['BotReactionPoints'][key])])
            pass  
    
    if('BotReactionLevels' in sections):    
        globalParameter['BotReactionLevels'].clear()                
        for key in config['BotReactionLevels']:
            #reaction_xxx = expression  
            globalParameter['BotReactionLevels'].append([str(key).split("_")[0], str(key).split("_")[1], str(key).split("_")[2], str(config['BotReactionLevels'][key])])
            print(globalParameter['BotReactionLevels'][-1])
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
    Checklevel()
    OrganizeParameters()
    globalParameter['TriggerTagsList'] = str(globalParameter['TriggerTags']).split(',')    

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

    fileConfiName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    fileConfiNameDefault = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini.default")

    if(os.path.isfile(fileConfiName) == False):
        if(os.path.isfile(fileConfiNameDefault) == True):
            shutil.copyfile(fileConfiNameDefault, fileConfiName)
            pass

    if args['config'] is not None:
        print('Config.ini: ' + args['config'])
        globalParameter['configFile'] = args['config']  

    MainLocal()