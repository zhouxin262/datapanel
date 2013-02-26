var _haq = (function(_haq) {
    _haq.push = function(a) {
        if(_haq.func[a[0]]){
            _haq.func[a[0]] && _haq.func[a[0]].apply(_haq.func, a.slice(1));
        }else{
            _haq.func['run'] && _haq.func['run'].apply(_haq.func, a);
        }
    }
    _haq.func = {
        domain: 'tongji.haoems.com',
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
            data = {'k': this.token, 'u': document.location.href, 'r': this.referrer()},
            data['a'] = 'track';
            data['e'] = e;
            if(p) {
                data['p'] = p;
            }
            this._send(data);
        },
        run: function(f, p) {
            data = {'k': this.token, 'u': document.location.href, 'r': this.referrer()},
            data['a'] = 'run';
            data['f'] = f;
            if(p) {
                data['p'] = p;
            }
            this._send(data);
        },
        _send: function(data){
            var url = 'http://' + this.domain + '/a/?data=' + this.zip(this.json2str(data))
            var now = "i=" + new Date().getTime();
            url += "&" + now;
            if(this.config['debug']){
                console.log(this.json2str(data));
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
            r = document.referrer;
            if(this.config['debug']){
                r = 'http://www.baidu.com/s?wd=%B2%E2%CA%D4&rsv_bp=0&rsv_spt=3&rsv_sug3=3&rsv_sug=0&rsv_sug1=2&rsv_sug4=110&inputT=629';
            }
            if(!r) {
                try {
                    if(window.opener) {
                        // IE下如果跨域则抛出权限异常
                        // Safari和Chrome下window.opener.location没有任何属性
                        r = window.opener.location.href;
                    }
                } catch(e) {}
            }
            if(!r){r=''}
            return r;
        },
        json2str: function(obj) {
            var THIS = this;
            switch(typeof(obj)) {
                case 'string':
                     return '"' + encodeURI(obj.replace(/(["\\])/g, '\\$1')) + '"';
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
                    } else if(obj == true) {
                        return 1;
                    } else if(obj == false) {
                        return 0;
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


/* deprecated */
// referrer: function() {
//     var r = {
//         'd': null,
//         'kw': null,
//         'url': null
//     }

//     function getQueryStringRegExp(name, url) {
//         var reg = new RegExp("(^|\\?|&)" + name + "=([^&]*)(\\s|&|$)", "i");
//         if(reg.test(url)) return unescape(RegExp.$2.replace(/\+/g, " "));
//         return "";
//     }

//     r['url'] = document.referrer;
//     if(this.config['debug']){
//         r['url'] = 'http://www.baidu.com/s?wd=测试&rsv_bp=0&rsv_spt=3&rsv_sug3=4&rsv_sug=0&rsv_sug4=469&inputT=823';
//     }
//     if(!r['url']) {
//         try {
//             if(window.opener) {
//                 // IE下如果跨域则抛出权限异常
//                 // Safari和Chrome下window.opener.location没有任何属性
//                 r['url'] = window.opener.location.href;
//             }
//         } catch(e) {}
//     }

//     if(r['url']) {
//         var rf_domain = r['url'].split('/')[2];
//     } else {
//         var rf_domain = '';
//     }
//     if(rf_domain.indexOf('baidu') >= 0) {
//         r['d'] = 'baidu';
//         if(r['url'].indexOf('&wd=') >= 0 || r['url'].indexOf('?wd=') >= 0) {
//             r['kw'] = getQueryStringRegExp("wd", r['url']);
//         } else if(r['url'].indexOf('&word=') >= 0 || r['url'].indexOf('?word=') >= 0) {
//             r['kw'] = getQueryStringRegExp("word", r['url']);
//         }
//         //document.write(key);
//     } else if(rf_domain.indexOf('soso') >= 0) {
//         r['d'] = 'soso';
//         r['kw'] = getQueryStringRegExp("w", r['url']);
//     } else if(rf_domain.indexOf('sogou') >= 0) {
//         r['d'] = 'sogou';
//         r['kw'] = getQueryStringRegExp("query", r['url']);
//     } else if(rf_domain.indexOf('youdao') >= 0) {
//         r['d'] = 'youdao';
//         r['kw'] = getQueryStringRegExp("q", r['url']);
//     } else if(rf_domain.indexOf('bing') >= 0) {
//         r['d'] = 'bing';
//         r['kw'] = getQueryStringRegExp("q", r['url']);
//     } else if(rf_domain.indexOf('google') >= 0) {
//         r['d'] = 'google';
//         r['kw'] = getQueryStringRegExp("q", r['url']);
//     } else {
//         r['d'] = rf_domain;
//         r['kw'] = '';
//     }
//     return r;
// },
