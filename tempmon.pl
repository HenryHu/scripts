#! /usr/bin/perl
if ($ARGV[0] eq "-nogpu")
{
    $nogpu = 1;
}
while (1)
{
	$c0 = `sysctl dev.cpu.0.temperature`;
	$c1 = `sysctl dev.cpu.1.temperature`;
	$z0 = `sysctl hw.acpi.thermal.tz0.temperature`;
	$z1 = `sysctl hw.acpi.thermal.tz1.temperature`;
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
	#print $c1;
	$_ = $z0;
	/[^ ]+\s+([\d.]+)C/;
	print "Thermal Zone 0: ".$1." C\n";
	$_ = $z1;
	/[^ ]+\s+([\d.]+)C$/;
	print "Thermal Zone 1: ".$1." C\n";
    if (!$nogpu)
    {
	    $g0 =~ /[^)]*\):\s*(.*)\./;
	    print "GPU 0: ".$1." C\n";
    }
	print "----------------\n";
	sleep 1;	
} 
