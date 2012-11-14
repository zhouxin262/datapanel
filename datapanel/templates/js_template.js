var host = '111.67.195.174';
var key = '{{params.key}}';

jx = {
    callback: function(obj) {
        var url = "/?" + this.json2url(obj);
        return this.load(url, null)
    },
    push: function(t, p) {
        if(!p.referrer) {
            p.referrer = document.referrer;
        }
        var params = this.params(p);
        var url = 'http://' + host + '/t/?k=' + key + '&t=' + encodeURIComponent(t) + '&p=' + encodeURIComponent(params);
        return this.load(url, null, 'jsonp');
    },
    //Create a xmlHttpRequest object - this is the constructor.
    getHTTPObject: function() {
        var http = false;
        //Use IE's ActiveX items to load the file.
        if(typeof ActiveXObject != 'undefined') {
            try {
                http = new ActiveXObject("Msxml2.XMLHTTP");
            } catch(e) {
                try {
                    http = new ActiveXObject("Microsoft.XMLHTTP");
                } catch(E) {
                    http = false;
                }
            }
            //If ActiveX is not available, use the XMLHttpRequest of Firefox/Mozilla etc. to load the document.
        } else if(window.XMLHttpRequest) {
            try {
                http = new XMLHttpRequest();
            } catch(e) {
                http = false;
            }
        }
        return http;
    },
    // This function is called from the user's script.
    //Arguments -
    //  url - The url of the serverside script that is to be called. Append all the arguments to
    //          this url - eg. 'get_data.php?id=5&car=benz'
    //  callback - Function that must be called once the data is ready.
    //  format - The return type for this function. Could be 'xml','json' or 'text'. If it is json,
    //          the string will be 'eval'ed before returning it. Default:'text'
    load: function(url, callback, format) {
        var http = this.init(); //The XMLHttpRequest object is recreated at every call - to defeat Cache problem in IE
        if(!http || !url) return;
        if(http.overrideMimeType) http.overrideMimeType('text/xml');

        if(!format) var format = "text"; //Default return type is 'text'
        format = format.toLowerCase();

        //Kill the Cache problem in IE.
        var now = "uid=" + new Date().getTime();
        url += (url.indexOf("?") + 1) ? "&" : "?";
        url += now;

        if(format == 'jsonp') {
            var head = document.getElementsByTagName ("head")[0] || document.documentElement;
            var script = document.createElement("script");
            script.src = url;
            script.charset = 'utf-8';
            head.insertBefore(script, head.firstChild);
            return undefined;
        }

        http.open("GET", url, true);
        http.onreadystatechange = function() { //Call a function when the state changes.
            if(http.readyState == 4) { //Ready State will be 4 when the document is loaded.
                if(http.status == 200 || http.status == 0) { // ==0 local
                    var result = "";
                    if(http.responseText) result = http.responseText;
                    //If the return is in JSON format, eval the result before returning it.
                    if(format.charAt(0) == "j") {
                        //\n's in JSON string, when evaluated will create errors in IE
                        result = result.replace(/[\n\r]/g, "");
                        result = eval('(' + result + ')');
                    }

                    //Give the data to the callback function.
                    if(callback) callback(result);
                } else { //An error occured
                    if(error) error(http.status);
                }
            }
        }
        http.send(null);
    },
    params: function(obj) {
        var THIS = this;
        switch(typeof(obj)) {
        case 'string':
            return '"' + obj.replace(/(["\\])/g, '\\$1') + '"';
        case 'array':
            return '[' + obj.map(this.params).join(',') + ']';
        case 'object':
            if(obj instanceof Array) {
                var strArr = [];
                var len = obj.length;
                for(var i = 0; i < len; i++) {
                    strArr.push(this.params(obj[i]));
                }
                return '[' + strArr.join(',') + ']';
            } else if(obj == null) {
                return 'null';
            } else {
                var string = [];
                for(var property in obj) string.push(this.params(property) + ':' + this.params(obj[property]));
                return '{' + string.join(',') + '}';
            }
        case 'number':
            return obj;
        case false:
            return obj;
        }
    },
    json2url: function(a1) {
        var u = [];
        for(x in a1) {
            if(a1[x] instanceof Array) u.push(x + "=" + encodeURI(a1[x].join(",")));
            else if(a1[x] instanceof Object) u.push(this.json2url(a1[x]));
            else u.push(x + "=" + encodeURI(a1[x]));
        }
        return u.join("&");
    },
    init: function() {
        return this.getHTTPObject();
    }
}
