#!/usr/bin/perl

$splitsize = 3800;

$srcname = $ARGV[0];

if ($#ARGV >= 1)
{
	$encoding = $ARGV[1];
}

print "Splitting $srcname\n";
print "Split unit: $splitsize bytes\n";

$filetype = `file "$srcname"`;

if ($filetype =~ m/ISO-8859/ or $filetype =~ m/extended-ASCII/)
{
	# GBK file
	$srcenc = "gbk";
} elsif ($filetype =~ m/UTF-16/) {
	# UTF-16 file
	if ($filetype =~ m/Little-endian/)
	{
		# UTF-16 Little Endian
		$srcenc = "utf-16le";
	} else {
		# UTF-16 Big Endian
		$srcenc = "utf-16be";
	}
} else {
	if ($encoding eq "")
	{
		$srcenc = "utf-8";
	} else {
		$srcenc = $encoding;
	}
}

print "Detected encoding: $srcenc\n";

system("iconv -c -f $srcenc -t utf-16le \"$srcname\" > /tmp/ipodsplit.tmp");

$srcsize = -s "/tmp/ipodsplit.tmp";

$sfxlen = 1;
$maxsize = 26 * $splitsize;

while ($srcsize > $maxsize)
{
	$sfxlen++;
	$maxsize = $maxsize * 26;
}

$pagecount = int($srcsize / $splitsize) + 1;
$pagelen = length($pagecount);

print "Split to files...\n";

system("split -b $splitsize -a $sfxlen /tmp/ipodsplit.tmp");

system("printf '\377\376' > /tmp/bom");

$pagenum = 1;

print "Start parsing...\n";

foreach (glob "x" . ("?" x $sfxlen))
{
	print ".";
	if ($pagenum % 50 == 0) {
		print "\n";
	}
	$name = $_;
	$next = ++$_;
	system("printf '<title>Page " . "0" x ($pagelen - length($pagenum)) . $pagenum . "</title>\n' | iconv -t utf-16le > /tmp/pageheader");
	$pagenum++;
	system("printf '\n<a href=\"$next.txt\">Page $pagenum</a>' | iconv -t utf-16le > /tmp/pagenum");
	system("cat /tmp/bom /tmp/pageheader $name /tmp/pagenum > $name.txt");
	system("rm $name");
}

system("rm /tmp/ipodsplit.tmp /tmp/bom /tmp/pagenum /tmp/pageheader");

$pagenum --;

if ($pagenum % 50 != 0) {
	print "\n";
}

print "Finished! Parsed $pagenum pages\n";
