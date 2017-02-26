#!/usr/bin/env perl
#$manpath = `manpath | sed -e "s/:/ /g"`
#foreach i ($TMANPATH)
#( ls -1 $i/man1 | sed s%\\.$1.\*\$%% > /dev/stdout ) 
#end

$manlist_tmp = "/tmp/manlist_tmp";
$manlist_uniq = "/tmp/manlist_uniq";
$manpath = `manpath`;
chop($manpath);

sub printsection($) {
    $section = shift;
    foreach $path (split(/:/, $manpath))
    {
        foreach $file (<$path/man$section/*>)
        {
            $file =~ s/.*\/(.*)\.$section.*/$1/;
            print $file, "\n";
        }
    }
}

if ($ARGV[0])
{
    printsection($ARGV[0]);
} else {
    if (-e "$manlist_uniq")
    {
        system("cat $manlist_uniq");
    }
    else
    {
        $oldstdout = open(MANLIST_TMP, ">", $manlist_tmp);
        select(MANLIST_TMP);
        foreach $section( qw(0 1 2 3 4 5 6 7 8 9 o n p l) )
        {
            printsection($section);
        }
        select($oldstdout);
        system("cat $manlist_tmp | uniq > $manlist_uniq");
        system("cat $manlist_uniq");
    }
}
