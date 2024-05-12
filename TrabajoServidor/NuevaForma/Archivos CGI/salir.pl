#!/usr/bin/perl


use strict;
use warnings;

use CGI;
#instalar este paquete
use CGI::Session;
use DBI;


my $session = new CGI::Session;
$session->load();
$session->delete();
$session->fflush();
print $session->header(.location => "../login.html");
