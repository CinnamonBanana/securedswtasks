<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form method="GET">
    Логин <input name="username" type="text" required><br>
    Пароль <input name="password" type="password" required><br>
    <input name="Login" type="submit" value="Login">
    </form>
    
    <?php
    $maxattempts = 5;
    $timeout = 5;
    function dbcon()
    {
        try {
            require_once ('dbCredentials.php');
            return new PDO($strHostName, $strUserName, $strPassword, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        } catch (PDOException $e) {
            die($e->getMessage());
        } 
    }

    function setattempts($pdo, $user, $attempts)
    {
        $sql = 'UPDATE public.users SET attempts = :attempts, last_call = :lasttime WHERE username = :user';
        $sth = $pdo->prepare($sql);
        $sth->bindParam(':user', $user, PDO::PARAM_STR );
        $sth->bindParam(':attempts', $attempts, PDO::PARAM_STR );
        $sth->bindParam(':lasttime', time(), PDO::PARAM_STR );
        $sth->execute();
    }

    if(isset($_GET['Login']))
    {

        $pdo = dbcon();
        $user = stripslashes($_GET[ 'username' ]);
        $password = stripslashes($_GET[ 'password' ]);

        $sql = 'SELECT * FROM public.users WHERE username = :user LIMIT 1';
        $sth = $pdo->prepare($sql);
        $sth->bindParam(':user', $user, PDO::PARAM_STR );
        $sth->execute();
        $field = $sth->fetch();

        if($field['attempts']<$maxattempts && time()-$field['last_call']>3 && count($field))
        {
            $pass = hash('sha256', $field['salt'].$password);

            if ($pass == $field['pwd'])
            {
                echo "<p>Welcome to the password protected area</p>";
                setattempts($pdo, $user, 0);
            }
            else
            {
                echo "<p><br />Username and/or password incorrect.</p>";
                setattempts($pdo, $user, $field['attempts']+1);
            }
        }
        elseif(count($field) == 0)
        {
            echo "<p><br />Username and/or password incorrect.</p>";
        }
        else
        {
            echo "<p>Слишком много попыток входа.</p>";
            $remain = 60*$timeout-(time()-$field['last_call']);
            echo "<p>Осталось ".intval($remain/60)." минут ".($remain%60)." секунд.</p>";
            echo "<p>RAW: ".$remain."</p>";
            if ($field['attempts']>=$maxattempts && $remain<=0)
            {
                setattempts($pdo, $user, $field['attempts']-3);
            }
        }
        

    }
    ?>
</body>
</html>