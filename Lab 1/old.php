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
        $pass = hash('sha256', $field['salt'].$password);

        if ($pass == $field['pwd'])
        {
            echo "<p>Welcome to the password protected area</p>";
        }
        else
        {
            echo "<p><br />Username and/or password incorrect.</p>";
        }
    }
    ?>
</body>
</html>