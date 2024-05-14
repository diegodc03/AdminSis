#!/usr/bin/perl


#Aqui deberemos meter como vamos a hacer el inicio de sesión, es decir, tenemos que hacer de alguna manera que ffuera podemos añadir algo
    # Es decir, yo en la web de recuperacion de contraseña pongo mi correo, y se ele vía un correo al ususrio
    # Estonces, va al correo, y le redirige a un link

    # COmo hago que cuando redifirgja tenga los datos del correo anteriormente mandado


use strict;
use warnings;
use CGI;
use DBI;
use Email::Send::SMTP::Gmail;

my $cgi = CGI->new;


#Declaramos las variables de la base de datos
    my $root = "adminBase";
    my $pass = "123456";
    my $host = "localhost";
    my $db_name = "usuarios";

    # Nos conectamos a la base de datos
    my $db = DBI->connect("DBI:MariaDB:database=$db_name;host=$host", $root, $pass, { RaiseError => 1, PrintError => 0 });

    my $email = $cgi->param('email');

# Procesar formulario de recuperación de contraseña
if ($cgi->param('submit')) {

    
    
    # Verificar que el correo electrónico sea válido (puedes agregar más validaciones)
    if ($email =~ /\w+\@\w+\.\w+/) {
        # Generar token único
        my $token = generate_token();
        
        # Almacenar el token en la base de datos junto con el correo electrónico del usuario
        my $consulta = $db->prepare("INSERT INTO recuperacion_contrasenia(email, token) VALUES (?, ?)");
        
        
        $consulta->execute($email, $token);
        #guardado en la base de datos
        

        # Enviar correo electrónico al usuario con el enlace de restablecimiento de contraseña
        send_password_reset_email($email, $token);
        
        print $cgi->header;
        print "<h3>Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.</h3>";

    } else {
        print $cgi->header;
        print "<h3>Correo electrónico no válido. Por favor, ingresa un correo electrónico válido.</h3>";
    }
} else {
    # Verificar el token en la URL
    # Cuando se pulse el link, al no haber botón de submit irán por el else, sabremos que han recibido el correo, y lo único que hay que hacer es hacer que el parametro de la bd sea igual que el token
    my $token = $cgi->param('token');
    
    if ($token) {
        
        #Vamos a la base de datos y se accede
            #Se comparan el token, y si es el mismo entonces se accederá    
            # Almacenar el token en la base de datos junto con el correo electrónico del usuario
            $consulta = $db->prepare("SELECT * from recuperacion_contrasenia where email=? and token = ? ")
        
            $consulta->execute($email, $token);

            # Obtenemos el número de filas coincidentes
            my ($num_filas) = $consulta->fetchrow_array;

            # Verificamos si el usuario ya existe
            if ($num_filas == 0) {
                
                print $q->header(-type => "text/html");
                print "<h3>La solicitud de coambio de contraseña no existe</h3>";
                print "Redirigiendo en 3 segundos";
                print "<meta http-equiv='refresh' content='3; ../Registrarse.html'>";
                $db->disconnect;

            }else{
            
                # Si el token es válido, mostrar el formulario de restablecimiento de contraseña
                print $cgi->header;
                print $cgi->start_html(-title => 'Restablecimiento de Contraseña');
                print "<h2>Restablecimiento de Contraseña</h2>";
                print "<form method='post' action='recordarContraseniaSesion.cgi'>";
                print "Nueva Contraseña: <input type='password' name='nueva_contrasenia'><br>";
                print "Confirmar Nueva Contraseña: <input type='password' name='confirmar_contrasenia'><br>";
                print "<input type='hidden' name='token' value='$token'>"; # Incluir el token como campo oculto
                print "<input type='submit' name='submit' value='Restablecer'>";
                print "</form>";
                print $cgi->end_html;
            
            
            }

        
    } else {
        # Si el token no está presente en la URL o no es válido, mostrar un mensaje de error
        print $cgi->header;
        print "<h3>Error: Token inválido o no proporcionado.</h3>";
    }
}

# Función para generar un token único
sub generate_token {
    my @chars = ('A'..'Z', 'a'..'z', 0..9);
    my $token = '';
    $token .= $chars[rand @chars] for 1..32;
    return $token;
}

# Función para enviar correo electrónico de restablecimiento de contraseña
sub send_password_reset_email {
    
    my ($email, $token) = @_;
    #Aqui pon el correo que sea
    
    my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'servicioscondeydiego@gmail.com',
                                                 -pass=>'gyjn owfz lqlq htzv');

    my $message = "Haz clic en el siguiente enlace para restablecer tu contraseña: ";
    $message .= "http://example.com/reset_password.pl?token=$token";
 
    $mail->send(-to=>$email, -subject=>'Cambio de Contraseña', -body=>$message,
            -attachments=>'full_path_to_file');
 
    $mail->bye;
    

}
