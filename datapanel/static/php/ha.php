<?php
class HA
{
    public $domain = "tongji.haoems.com";
    public $token = "";
    public $config = array();
    public function init($token, $config)
    {
        $this->token = $token;
        if(!empty($config)){
            $this->config = $config;
        }
    }
    public function track($event, $parameter)
    {
        $data = array("k"=>$this->token, "u"=>'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'],"r"=>$this->referrer());
        $data["a"] = "track";
        $data["e"] = $event;
        if(!empty($parameter)){
            $data['p'] = $parameter;
        }
        $this->_send($data);
    }
    public function run($function, $parameter)
    {
        $data = array("k"=>$this->token, "u"=>'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'],"r"=>$this->referrer());
        $data["a"] = "run";
        $data["f"] = $function;
        if(!empty($parameter)){
            $data['p'] = $parameter;
        }
        $this->_send($data);
    }
    public function referrer()
    {
        return $_SERVER['HTTP_REFERER'];
    }
    public function _send($data)
    {
        $url = 'http://' . $this->domain . '/a/?data=' . $this->zip($this->json2str($data));
        $now = "&i=" . time();
        $url .= $now;
        $this->_insert($url);
    }
    public function json2str($data)
    {
        return json_encode($data);
    }
    public function zip($data)
    {
        return base64_encode($data);
    }
    public function _insert($url)
    {
        if (function_exists('curl_init') == 1)
        {
            $curl = curl_init();
            curl_setopt ($curl, CURLOPT_URL, $url);
            curl_setopt ($curl, CURLOPT_HEADER,0);
            curl_setopt ($curl, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt ($curl, CURLOPT_USERAGENT,$_SERVER['HTTP_USER_AGENT']);
            curl_setopt ($curl, CURLOPT_TIMEOUT,8000);
            $get_content = curl_exec($curl);
            curl_close ($curl);
        }
    }
}
