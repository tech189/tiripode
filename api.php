<?php
if($_GET["mode"] == "size") {
    try {
        $size = shell_exec("/var/www/html/tiripode/venv/bin/python /var/www/html/tiripode/query.py --" . $_GET['mode'] . " 2>&1");
        header('Content-type:application/json;charset=utf-8');
        echo("$size");
    }
    catch (exception $e) {
        echo("$e");
    }
}
elseif($_GET["mode"] == "parse") {
    try {
        // TODO sanitise with [a-z0-9]
        $parse = shell_exec("/var/www/html/tiripode/venv/bin/python /var/www/html/tiripode/query.py --parse " . $_GET['word'] . " 2>&1");
        header('Content-type:application/json;charset=utf-8');
        echo("$parse");
    }
    catch (exception $e) {
        echo("$e");
    }
}
elseif($_GET["mode"] == "lookup") {
    try {
        // TODO sanitise with [a-z0-9]
        $lookup = shell_exec("/var/www/html/tiripode/venv/bin/python /var/www/html/tiripode/query.py --lookup " . $_GET['word'] . " 2>&1");
        header('Content-type:application/json;charset=utf-8');
        echo("$lookup");
    }
    catch (exception $e) {
        echo("$e");
    }
}
else{
    $error = "{\"error\": \"please choose mode=size/parse\"}";
    header('Content-type:application/json;charset=utf-8');
    echo("$error");
}