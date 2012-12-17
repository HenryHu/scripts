#!/usr/bin/perl

sub playfile {
	my($file, $sub, $encoding, $args) = @_;
	if ($file =~ m/.*\.wmv/) {
		$args .= " -subdelay -5 "
	}
	if ($encoding eq "")
	{
		system("mplayer \"$file\" -sub \"$sub\" -utf8 $args");
	} else {
#		system("iconv -f $encoding -c \"$sub\" | mplayer \"$file\" -sub - -utf8 $args");
		system("iconv -f $encoding -c \"$sub\" > /tmp/subtitle.sub");
		system("mplayer \"$file\" -ass -sub /tmp/subtitle.sub -utf8 $args");
		system("rm -f /tmp/subtitle.sub");
	}
}

@exts = ('srt','ssa','ass', '[VeryCD.com].ssa');

@langs = ('en','Eng','chs','Chs','cn','sc_v2', 'sc','SC','uni_gb','gb','GBK','GB','cht','tc','TC','uni_big5','neta');

if ($#ARGV == -1)
{
	print "Usage: subwrap <filename>\n";
	exit 1;
}

$fname = $ARGV[0];

$argstr = "";

for ($i = 1; $i <= $#ARGV; $i = $i + 1)
{
	$argstr = $argstr . $ARGV[$i] . " ";
}

if (!(-e $fname))
{
	print "Cannot find specified file.\n";
	exit 2;
}

if ($ENV{'SUBFILE'})
{
	$subname = $ENV{'SUBFILE'};
	goto FOUND;
}

if (!($fname =~ m/(.*)\.(.*)/))
{
	print "Cannot find . in filename.\n";
	exit 1;
}


for ($way = 0; $way < 3; $way++)
{
	if ($way == 0)
	{
		$fname =~ m/(.*)\.(.*)/;
		$basename = $1;
	} elsif ($way == 1) {
		$fname =~ m/(.*)\[.*\]\.(.*)/;
		$basename = $1;
	} elsif ($way == 2) {
		$fname =~ m/(.*)\.\[.*\]\.(.*)/;
		$basename = $1;
	}

	# First let's try only extensions
	foreach $i (@exts)
	{
		$subname = $basename . "." . $i;
		if (-e $subname)
		{
			goto FOUND;
		}
	}

	# Now let's try extensions with languages
	foreach $i (@langs)
	{
		foreach $j (@exts)
		{
			$subname = $basename . "." . $i . "." . $j;
			if (-e $subname)
			{
				goto FOUND;
			}
		}
	}
}
	
# We failed!
print "Cannot found subtitles in (@exts) or (@langs) . (@exts).\n";
exit 2;

FOUND:

$filetype = `file "$subname"`;
print "Found sub file: $subname\n";

if ($filetype =~ m/ISO-8859/ or $filetype =~ m/extended-ASCII/)
{
	# GBK file
	print "Converting from GBK encoding\n";
	playfile($fname, $subname, "gbk", $argstr);
} elsif ($filetype =~ m/UTF-16/) {
	# UTF-16 file
	if ($filetype =~ m/Little-endian/)
	{
		# UTF-16 Little Endian
		print "Converting from UTF-16LE encoding\n";
		playfile($fname, $subname, "utf-16le", $argstr);
	} else {
		# UTF-16 Big Endian
		print "Converting from UTF-16BE encoding\n";
		playfile($fname, $subname, "utf-16be", $argstr);
	}
} else {
	playfile($fname, $subname, "", $argstr);
}

