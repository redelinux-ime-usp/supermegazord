/^host/ { 
	gsub(/;/, "");
	print $2 "-" $6 "-" $8
}
