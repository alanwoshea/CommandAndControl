#!/bin/bash

# Basic bash port scanner

argNum=$#
arg1=$1
arg2=$2
arg3=$3
arg4=$4
arg5=$5

function mode 
{ 
	case $argNum in 
		0) interactive ;;

		2) interactiveto	;; #find out what has two args

		3) autotimeout ;;

		5) manutimeout ;;

		*) printf "invalid argument input" 
	esac
}
function interactive 
{ 
			if [ -z "$timeout" ];
			then
				timeout=2
			else
				timeout=$timeout
			fi
			while true
				do
					read -p "Enter hostname: " varhost
					host=$varhost				
					if [ -z "$host" ]; 
					then
						echo "...No hostname entered, goodbye."
						exit 
					else
						read -p "Enter startport: " varstart
						startport=$varstart	
						read -p "Enter stopport: " varstop
						stopport=$varstop
					fi
					echo "________________________"
					pingcheck
					portcheck
					echo "________________________"
			done
}
function interactiveto 
{ 
	if [ $arg1 == "-t" ];
	then
		timeout=$arg2
		interactive
	else
		echo "Invalid argument"
	fi
}
function autotimeout
{
	timeout=2
	printf "\nAuto-Timeout Mode Active \n"
	echo "________________________"
	host=$arg1
	startport=$arg2
	stopport=$arg3
}
function manutimeout
{
	if [ $arg1 == "-t" ];
	then
		totrigger=$arg1
		printf "\nManual-Timeout Mode Active \n"
		echo "__________________________"
		timeout=$arg2		
		host=$arg3
		startport=$arg4
		stopport=$arg5
	else
		echo "Invalid argument" 
		exit
	fi
}

function pingcheck
{
ping=`ping -c 1 $host | grep bytes | wc -l`
if [ "$ping" -gt 1 ]; then
    echo "$host is up"
else
    echo "$host is down, quitting"
    exit
fi
}

function portcheck
{
for ((counter=$startport; counter<=$stopport; counter++))
do
    if timeout $timeout bash -c "echo >/dev/tcp/$host/$counter"
    then 
        echo "$counter open"
    else
        echo "$counter closed"
    fi
done
}
mode
# first, check that the host is alive
pingcheck
# next, loop through the ports
portcheck


