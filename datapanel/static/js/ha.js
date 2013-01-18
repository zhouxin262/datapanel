(function() {
    var _haq = (function(_haq) {
        _haq.push = function(a) {
            _haq.func[a[0]] && _haq.func[a[0]].apply(_haq.func, a.slice(1));
        }
        _haq.func = {
            token: '',
            init: function(token) {
                if(token && !this.token) {
                    this.token = token;
                }
            },
            test: function() {
                alert(this.token);
            },
            Z: function(a) {
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
    })(_haq || []);
    _haq = _haq.reverse()
    while(_haq.length > 0) {
        var foo = _haq.pop();
        _haq.push(foo);
    }
})();