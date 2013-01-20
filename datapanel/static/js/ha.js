(function() {
    var _haq = (function(_haq) {
        _haq.push = function(a) {
            if(_haq.func[a[0]]){
                _haq.func[a[0]] && _haq.func[a[0]].apply(_haq.func, a.slice(1));
            }else{
                _haq.func['run'] && _haq.func['run'].apply(_haq.func, a);
            }
        }
        _haq.func = {
            domain: '127.0.0.1:8000',
            token: '',
            config: {},
            init: function(token, config) {
                if(token && !this.token) {
                    this.token = token;
                }
                if(config){
                    this.config = config;
                }
            },
            track: function(e, p) {
                var data = {
                    'k': this.token,
                    'a': 'track',
                    'e': e,
                    'r': this.referrer()
                };
                if(p) {
                    data['p'] = p;
                }
                this._send(data);
            },
            run: function(f, p) {
                var data = {
                    'k': this.token,
                    'a': 'run',
                    'f': f,
                };
                if(p) {
                    data['p'] = p;
                }
                this._send(data);
            },
            _send: function(data){
                var url = 'http://' + this.domain + '/a/?data=' + this.zip(this.json2str(data))
                var now = "i=" + new Date().getTime();
                url += (url.indexOf("?") + 1) ? "&" : "?";
                url += now;
                if(this.config['debug']){
                    console.log(data);
                    console.log(url);
                }
                this._insert(url);
            },
            _insert: function(a, b) {
                if(a) {
                    var c = document.createElement("script");
                    c.type = "text/javascript";
                    c.async = true;
                    c.src = a;
                    c.id = b;
                    var d = document.getElementsByTagName("script")[0];
                    d.parentNode.insertBefore(c, d);
                    return c
                }
            },
            referrer: function() {
                var referrer_obj = {
                    'd': '',
                    'kw': ''
                }

                function getQueryStringRegExp(name, url) {
                    var reg = new RegExp("(^|\\?|&)" + name + "=([^&]*)(\\s|&|$)", "i");
                    if(reg.test(url)) return unescape(RegExp.$2.replace(/\+/g, " "));
                    return "";
                }
                var referrer = document.referrer;
                if(!referrer) {
                    try {
                        if(window.opener) {
                            // IE下如果跨域则抛出权限异常
                            // Safari和Chrome下window.opener.location没有任何属性
                            referrer = window.opener.location.href;
                        }
                    } catch(e) {}
                }

                if(referrer) {
                    var rf_domain = referrer.split('/')[2];
                } else {
                    var rf_domain = '';
                }
                if(rf_domain.indexOf('baidu') >= 0) {
                    referrer_obj['d'] = 'baidu';
                    if(referrer.indexOf('&wd=') >= 0 || referrer.indexOf('?wd=') >= 0) {
                        referrer_obj['kw'] = getQueryStringRegExp("wd", referrer);
                    } else if(referrer.indexOf('&word=') >= 0 || referrer.indexOf('?word=') >= 0) {
                        referrer_obj['kw'] = getQueryStringRegExp("word", referrer);
                    }
                    //document.write(key);
                } else if(rf_domain.indexOf('soso') >= 0) {
                    referrer_obj['d'] = 'soso';
                    referrer_obj['kw'] = getQueryStringRegExp("w", referrer);
                } else if(rf_domain.indexOf('sogou') >= 0) {
                    referrer_obj['d'] = 'sogou';
                    referrer_obj['kw'] = getQueryStringRegExp("query", referrer);
                } else if(rf_domain.indexOf('youdao') >= 0) {
                    referrer_obj['d'] = 'youdao';
                    referrer_obj['kw'] = getQueryStringRegExp("q", referrer);
                } else if(rf_domain.indexOf('bing') >= 0) {
                    referrer_obj['d'] = 'bing';
                    referrer_obj['kw'] = getQueryStringRegExp("q", referrer);
                } else if(rf_domain.indexOf('google') >= 0) {
                    referrer_obj['d'] = 'google';
                    referrer_obj['kw'] = getQueryStringRegExp("q", referrer);
                }
                return referrer_obj;
            },
            json2str: function(obj) {
                var THIS = this;
                switch(typeof(obj)) {
                case 'string':
                    return '"' + escape(obj.replace(/(["\\])/g, '\\$1')) + '"';
                case 'array':
                    return '[' + obj.map(this.json2str).join(',') + ']';
                case 'object':
                    if(obj instanceof Array) {
                        var strArr = [];
                        var len = obj.length;
                        for(var i = 0; i < len; i++) {
                            strArr.push(this.json2str(obj[i]));
                        }
                        return '[' + strArr.join(',') + ']';
                    } else if(obj == null) {
                        return 'null';
                    } else {
                        var string = [];
                        for(var property in obj) string.push(this.json2str(property) + ':' + this.json2str(obj[property]));
                        return '{' + string.join(',') + '}';
                    }
                case 'number':
                    return obj;
                case false:
                    return obj;
                }
            },
            zip: function(a) {
                // base64 compress
                var b, d, j, e, i = 0,
                    h = 0,
                    g = "",
                    g = [];
                if(!a) return a;
                do b = a.charCodeAt(i++), d = a.charCodeAt(i++), j = a.charCodeAt(i++), e = b << 16 | d << 8 | j, b = e >> 18 & 63, d = e >> 12 & 63, j = e >> 6 & 63, e &= 63, g[h++] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(b) + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(d) + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(j) + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(e);
                while(i < a.length);
                g = g.join("");
                switch(a.length % 3) {
                case 1:
                    g = g.slice(0, -2) + "==";
                    break;
                case 2:
                    g = g.slice(0, -1) + "="
                }
                return g
            }
        }
        return _haq;
    })(window._haq || []);
    _haq = _haq.reverse()
    while(_haq.length > 0) {
        var foo = _haq.pop();
        _haq.push(foo);
    }
})();
