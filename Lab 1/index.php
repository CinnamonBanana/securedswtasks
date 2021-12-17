<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form method="POST">
    Логин <input name="username" type="text" required><br>
    Пароль <input name="password" type="password" required><br>
    <input name="Login" type="submit" value="Войти">
    </form>
    
    <?php
    $maxattempts = 5;
    function dbcon()
    {
        try {
            $dsn = "pgsql:host=127.0.0.1;port=5432;dbname=mydb;";
            $pdo = new PDO($dsn, 'postgres', '', [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
            return $pdo;
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

    if(isset($_POST['Login']))
    {

        $pdo = dbcon();
        $user = stripslashes($_POST[ 'username' ]);
        $password = stripslashes($_POST[ 'password' ]);

        $sql = 'SELECT * FROM public.users WHERE username = :user LIMIT 1';
        $sth = $pdo->prepare($sql);
        $sth->bindParam(':user', $user, PDO::PARAM_STR );
        $sth->execute();
        $field = $sth->fetch();

        if($field['attempts']<$maxattempts && time()-$field['last_call']>3)
        {
            $sql = 'SELECT username, pwd FROM public.users WHERE username = :user and pwd = :pwd';
            $sth = $pdo->prepare($sql);
            $sth->bindParam(':user', $user, PDO::PARAM_STR );
            $pass = hash('sha256', $field['salt'].$password);
            $sth->bindParam(':pwd', $pass, PDO::PARAM_STR );
            $sth->execute();
            $result= $sth->fetchAll();

            if (count($result) == 1)
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
        else
        {
            echo "<p>Слишком много попыток входа.</p>";
            $remain = 60*5-(time()-$field['last_call']);
            echo "<p>Осталось ".intval($remain/60)." минут ".($remain%60)." секунд.</p>";
            if ($field['attempts']>$maxattempts && time()-$field['last_call']>10*60)
            {
                setattempts($pdo, $user, $field['attempts']-3);
            }
        }
        

    }
    ?>
</body>
</html>