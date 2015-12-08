#! /usr/bin/perl

$nogpu = 1;
if ($ARGV[0] eq "-nogpu")
{
    $nogpu = 1;
}
while (1)
{
	$c0 = `sysctl dev.cpu.0.temperature`;
	$c1 = `sysctl dev.cpu.1.temperature`;
	$c2 = `sysctl dev.cpu.2.temperature`;
	$c3 = `sysctl dev.cpu.3.temperature`;
	$c4 = `sysctl dev.cpu.4.temperature`;
	$c5 = `sysctl dev.cpu.5.temperature`;
	$c6 = `sysctl dev.cpu.6.temperature`;
	$c7 = `sysctl dev.cpu.7.temperature`;
	$z0 = `sysctl hw.acpi.thermal.tz0.temperature`;
    if (!$nogpu)
    {
	    $g0 = `nvidia-settings -q \[gpu:0\]/GPUCoreTemp -c :0`;
    }
	$f0 = `sysctl dev.cpu.0.freq`;
	$_ = $f0;
	m/[^ ]*:\ (.*)/;
	print "CPU 0: ".$1." MHz\n";
	$_ = $c0;	
	m/[^ ]+:\s+(\d+\.\d+)C$/;
	# $c1 = m/.*[0..9]$/;
	# print $c0;
	print "CPU 0: ".$1." C\n";
	$c1 =~ /[^ ]*:\ *(\d+\.\d+)C$/;
	# print $c1;
	print "CPU 1: ".$1." C\n";
	$c2 =~ /[^ ]*:\ *(\d+\.\d+)C$/;
	print "CPU 2: ".$1." C\n";
	$c3 =~ /[^ ]*:\ *(\d+\.\d+)C$/;
	print "CPU 3: ".$1." C\n";
	$c4 =~ /[^ ]*:\ *(\d+\.\d+)C$/;
	print "CPU 4: ".$1." C\n";
	$c5 =~ /[^ ]*:\ *(\d+\.\d+)C$/;
	print "CPU 5: ".$1." C\n";
	$c6 =~ /[^ ]*:\ *(\d+\.\d+)C$/;
	print "CPU 6: ".$1." C\n";
	$c7 =~ /[^ ]*:\ *(\d+\.\d+)C$/;
	print "CPU 7: ".$1." C\n";
	#print $c1;
	$_ = $z0;
	/[^ ]+\s+([\d.]+)C/;
	print "Thermal Zone 0: ".$1." C\n";
#	$_ = $z1;
#	/[^ ]+\s+([\d.]+)C$/;
#	print "Thermal Zone 1: ".$1." C\n";
    if (!$nogpu)
    {
	    $g0 =~ /[^)]*\):\s*(.*)\./;
	    print "GPU 0: ".$1." C\n";
    }
	print "----------------\n";
	sleep 1;	
} 
