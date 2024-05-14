#!/usr/bin/perl

use strict;
use warnings;
 
use Email::Send::SMTP::Gmail;

print "tu pu";
my $token = 3543543;

my $email = "diegodecastro\@usal.es";

my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'servicioscondeydiego@gmail.com',
                                                 -pass=>'gyjn owfz lqlq htzv');

    my $message = "Haz clic en el siguiente enlace para crear el usuario: ";
    $message .= "http://example.com/reset_password.pl?token=$token";
 
    $mail->send(-to=>$email, -subject=>'Creacion de usuario', -body=>$message,
            -attachments=>'full_path_to_file');
 
    $mail->bye;