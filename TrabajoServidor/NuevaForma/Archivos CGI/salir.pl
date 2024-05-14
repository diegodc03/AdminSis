#!/usr/bin/perl


use strict;
use warnings;
use CGI;
use CGI::Session;
use DBI;


my $session = new CGI::Session;
$session->load();
$session->delete();
$session->fflush();
print $cgi->header();
print "Su sesion ha finalizado</br>";
print "</br>Sera redireccionado en 3 segundos</br>";
print "<meta http-equiv='refresh' content='3; /index.html'>";
#print $session->header(.location => "../login.html");
