#!/usr/bin/perl
#Aplicar cuota a un usuario
#------------------------------------------------------------
# Script to create a Quota in Linux (debian 12)

#Author:    Diego de Castro Merillas    [diegodecatro@usal.es]

# We are going to use Cpan.

# First, if we have not downloaded the usermod library...
# sudo apt install cpanminus
# cpanm install Quota



use strict;
use warnings;
use Linux::usermod;
use File::Copy;
use Quota;


#First, we list the mount table
#Mandatory to list the mount table, this reset or opens the mount table
Quota::setmntent();

my $device = 0;
my @mounts;
#We get the nest entry in the system mount table
while(my($dev, $path, $type, $opts) = Quota::getmntent()){
    #We print the entry only the file system can we apply the quotas
    
    if($type =~ /^ext*/ || $type eq "XFS" || $type eq "ReiserFS" || $type eq "JFS" || $type eq "Btrfs" || $type eq "ZFS" || $type eq "zfs"   ){
        print "\n";
        print "Number to elect: $device\n";
        print "Device: $dev\n";
        print "Path: $path\n";
        print "Type: $type\n";
        print "Options: $opts\n";
        print "\n";
        push(@mounts, $dev);
        $device = $device + 1;
    }
    
}

#Close the mount table
Quota::endmntent();


#We ask the user for the device and the path
print "Enter the device: ";
$device = <STDIN>;
;
if($device >= 0 && $device < scalar(@mounts)){
    $device = $mounts[$device];
    print "The path is $device\n";
}


#We ask the user for the username
my @users;

print "This is the users list\n";
    
    setpwent();
    # Iterate over each entry in the passwd file
    while (my ($username, undef, $uid, $gid) = getpwent()) {
    # Check if the GID is greater than 1000
        if ($gid >= 1000 && $uid >= 1000 && $gid < 60000 && $uid < 60000) {
            print "$username $uid $gid\n";
            push(@users, [$username, $uid, $gid]);
            
        }
    }
    endpwent();

print "Enter the username to apply the quota: ";
my $username = <STDIN>;
chomp($username);
my $aux = 0;
my $electedUID;
foreach my $listUser (@users){
    if($username eq @{$listUser}[0]){
        print "The user exists\n";
        $electedUID = @{$listUser}[1];
        $aux = 1;
    }
}

if($aux == 0){
    print "The user does not exist\n";
    exit();
}

print "If you do not apply any limit, enter 0\n";
#We ask the user for the quota hard limit
print "Enter the quota in MB: ";
my $hard = <STDIN>;


#We ask the user for the quota soft limit
print "Enter the soft limit in MB: ";
my $soft = <STDIN>;

#We ask the number of inodes soft
print "Enter the number of inodes: ";
my $softInodes = <STDIN>;

#We ask the number of inodes hard
print "Enter the number of inodes: ";
my $hardInodes = <STDIN>;

#We apply the quota
my ($block_set, $inode_set) = Quota::setqlim($device, $electedUID, $soft, $hard, $softInodes, $hardInodes, 0, 0);


if ($block_set && $inode_set) {
    print "Cuotas establecidas correctamente para $username .\n";
} else {
    print "Error al establecer las cuotas para $username: $!\n";
}






