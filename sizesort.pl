#!/usr/bin/env perl

%multipler = ('K' => 1000, 'M' => 1000000, 'G' => 1000000000, 'T' => 1000000000000);
@objs = ();

while (<>)
{
	if (/\s*([0-9.]+)([KMGT])/)
	{
		$number = $1;
		$unit = $2;
		$mult = $multipler{$2};
		
		$obj = { size => $number * $mult, line => $_};

		push(@objs, $obj);
	}
}

@sorted = sort { $a->{size} <=> $b->{size} } @objs;

# print @sorted;

foreach $element (@sorted)
{
	print $element->{line};
}
