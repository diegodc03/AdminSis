#!bin/bash

while true
do 
	
	/usr/bin/perl /usr/sbin/ficherosPerl/eliminarUsuario.pl
	/usr/bin/perl /usr/sbin/ficherosPerl/modificarContrasenia.pl
	/usr/bin/perl /usr/sbin/ficherosPerl/crearUsuario.pl
#	/usr/bin/perl /usr/sbin/simpleDaemon/actDesPagPersonales.pl
	sleep 6;
done
