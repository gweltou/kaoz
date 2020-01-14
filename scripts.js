let date = new Date(0);
let ajax = new XMLHttpRequest();
let update_interval = 2000;
let timer;
ajax.responseType = 'document';


ajax.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        /* MESSAGES RECEIVED ! */
        /*console.log(this.responseText);*/
        
        if (this.responseXML) {
            messages = this.responseXML.getElementsByTagName("message");
            for (let i = messages.length-1; i >= 0; i--) {
                /* childrens: id, type, message-container */
                let new_message = messages[i].children[4];
                appendMessage(new_message, messages[i].children[1].textContent);
                document.cookie = "last_id=" + messages[i].children[0].textContent;
            }
            if (messages.length > 0) {
                /* Peek more frequently */
                update_interval = Math.max(update_interval * 0.66, 200);
                w3CodeColor();    /* Code color highlighting */
            }
        }
    }
};


function appendMessage(message, content_type) {
    console.log(content_type);
    let frag = document.createRange().createContextualFragment(message.outerHTML);
    let messages = document.getElementById("kemennadennou");
    messages.insertBefore(frag, messages.childNodes[0]);
}


function updateKemennadennou(query_string) {
    ajax.open("GET", "kemennadennou" + query_string, true);
    ajax.send();
        
    /* Stretch update time interval */
    timer = window.setTimeout(updateKemennadennou, update_interval, "");
    update_interval = Math.floor(update_interval * 1.05);
}


function sendKemennadenn() {
        let pseudo = document.getElementById("pseudo-input").value
        /*date.setTime(Date.now() + 5*60*1000);*/
        /*let expires = "expires="+ date.toUTCString();*/
        document.cookie = "pseudo=" + encodeURIComponent(pseudo) /*+ ";" + expires;*/
        let query_string = "?p=";
        query_string += encodeURIComponent(pseudo);
        query_string += "&k=";
        query_string += encodeURIComponent(document.getElementById("kemennadenn-input").value);
        
        clearTimeout(timer);
        update_interval = 2000;
        updateKemennadennou(query_string);
        document.getElementById("kemennadenn-input").select();
      }
      
      function checkCookiesEnabled() {
        if (navigator.cookieEnabled == false) {
          window.alert("Cookies are not enabled");
        }
}


function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i = 0; i < ca.length; i++) {
          var c = ca[i];
          while (c.charAt(0) == ' ') {
            c = c.substring(1);
          }
          if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
          }
    }
    
    return "";
}


function pageInit() {
    checkCookiesEnabled();
    if (getCookie("pseudo") == "") {
            document.getElementById('karta').style.display='block';
            document.getElementById("pseudo-input").value = "pseudo" + Math.floor(Math.random()*1000).toString();
    } else {
        document.getElementById("pseudo-input").value = getCookie("pseudo");
    }
        
    document.cookie = "last_id=none"
    update_interval = 2000; /* UGLY */
    updateKemennadennou("");
}
      
      /*
      String.prototype.hashCode = function() {
        var hash = 0, i, chr;
        if (this.length === 0) return hash;
        for (i = 0; i < this.length; i++) {
          chr   = this.charCodeAt(i);
          hash  = ((hash << 5) - hash) + chr;
          hash |= 0; // Convert to 32bit integer
        }
        return hash;
      };*/


/* HTML Formatter
   https://stackoverflow.com/questions/26360414/javascript-how-to-correct-indentation-in-html-string

*/
/*
function process(str) {
    var div = document.createElement('div');
    div.innerHTML = str.trim();

    return format(div, 0).innerHTML;
}
*/

function format(node, level) {
    var indentBefore = new Array(level++ + 1).join('  '),
        indentAfter  = new Array(level - 1).join('  '),
        textNode;

    for (var i = 0; i < node.children.length; i++) {
        textNode = document.createTextNode('\n' + indentBefore);
        node.insertBefore(textNode, node.children[i]);

        format(node.children[i], level);

        if (node.lastElementChild == node.children[i]) {
            textNode = document.createTextNode('\n' + indentAfter);
            node.appendChild(textNode);
        }
    }

    return node;
}
