#!usr/bin/perl


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

# Procesar formulario de recuperación de contraseña
if ($cgi->param('submit')) {
    my $email = $cgi->param('email');
    
    # Verificar que el correo electrónico sea válido (puedes agregar más validaciones)
    if ($email =~ /\w+\@\w+\.\w+/) {
        # Generar token único
        my $token = generate_token();
        
        # Almacenar el token en la base de datos junto con el correo electrónico del usuario
        
        #
        #
        #
        #
        #
        #
        #


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
    my $token = $cgi->param('token');
    
    if ($token) {
        # Aquí deberías verificar si el token es válido en tu base de datos
        #Vamos a la base de datos y se accede
            #Se comparan el token, y si es el mismo entonces se accederá    




        # Si el token es válido, mostrar el formulario de restablecimiento de contraseña
        print $cgi->header;
        print $cgi->start_html(-title => 'Restablecimiento de Contraseña');
        print "<h2>Restablecimiento de Contraseña</h2>";
        print "<form method='post' action='restablecer_contrasenia.pl'>";
        print "Nueva Contraseña: <input type='password' name='nueva_contrasenia'><br>";
        print "Confirmar Nueva Contraseña: <input type='password' name='confirmar_contrasenia'><br>";
        print "<input type='hidden' name='token' value='$token'>"; # Incluir el token como campo oculto
        print "<input type='submit' name='submit' value='Restablecer'>";
        print "</form>";
        print $cgi->end_html;
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
    

    #Aqui pon el correo que sea
    
    my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'upsauniversidaddevalladolid@gmail.com',
                                                 -pass=>'paol ulvc mcbo gxkx');

    my $message = "Haz clic en el siguiente enlace para restablecer tu contraseña: ";
    $message .= "http://example.com/reset_password.pl?token=$token";
 
    $mail->send(-to=>$email, -subject=>'Usuario Creado', -body=>$message,
            -attachments=>'full_path_to_file');
 
    $mail->bye;
}
