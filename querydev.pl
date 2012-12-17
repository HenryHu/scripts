#!/usr/bin/perl

sub query_dev
{
	my ($name) = @_;
	$namelen = 0;
	$ret = "";
	$devs = `gpart list | grep Name`;
	foreach $i (split(/\n/, $devs))
	{
		$i =~ m/.*?Name: (.*)$/;
		$dev = $1;
		$j =`glabel status $dev 2>&1`;
		if ($? eq 0)
		{
			foreach $line (split(/\n/, $j))
			{
				if ($line =~ m/^$name /)
				{
					if (substr($line, 0, $namelen) == $name)
					{
						# In fact, maybe there are several
						# devices with the same label...
						# But what can we do...
						$ret = $dev;
					}
				}
				elsif ($line =~ m/^( *Name) *Status *Components$/)
				{
					$namepart = $1;
					$namelen = length($namepart);
				}
			}
		}
	}
	return $ret;
}

print(query_dev("msdosfs/IPOD"));
