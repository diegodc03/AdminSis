#!/usr/bin/perl

use strict;
use warnings;
 
use Email::Send::SMTP::Gmail;

print "tu pu";
 
my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'upsauniversidaddevalladolid@gmail.com',
                                                 -pass=>'paol ulvc mcbo gxkx');
 
print "session error: $error" unless ($mail!=-1);
 
$mail->send(-to=>'diegodecastromerillas@gmail.com', -subject=>'Hello!', -body=>'Just testing it',
            -attachments=>'full_path_to_file');
 
$mail->bye;
