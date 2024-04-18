# A cheap and sleazy version of ps
use Proc::ProcessTable;
 
my $FORMAT = "%-6s %-10s %-8s %-24s %s\n";
my $t = Proc::ProcessTable->new;
printf($FORMAT, "PID", "TTY", "STAT", "START", "COMMAND"); 
foreach my $p ( @{$t->table} ){
  printf($FORMAT, 
         $p->pid, 
         $p->ttydev, 
         $p->state, 
         scalar(localtime($p->start)), 
         $p->cmndline);
}
 
 
# Dump all the information in the current process table
use Proc::ProcessTable;
 
my $t = Proc::ProcessTable->new;
 
foreach my $p (@{$t->table}) {
 print "--------------------------------\n";
 foreach my $f ($t->fields){
   print $f, ":  ", $p->{$f}, "\n";
 }
}