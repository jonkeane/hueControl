#! /bin/sh

###############################################################
# Proximity detection
# Make changes below
# MAC address of each device to watch. Don't leave blank.
# For security purposes, if your router requires a password, even if someone could clone the MAC of your
# phone, they would still require the password of your network to link to your router.
# Updated 3/29/13 by Xathros

macdevice1="70:3E:AC:11:8D:CD" # jon's phone
macdevice2="B8:E8:56:EF:97:49" # ted's phone
macdevice3="D8:96:95:0C:AF:EB" # keith's phone
macdevice4="6C:40:08:9C:CB:DE" # jon's computer

#Sleep delays to prevent constant querying of the arp table
delay_occupied=15
delay_unoccupied=10



###############################################
#          do not change below here           #
###############################################

sleep
#initialize internal variables
# status of each MAC. 0=disconnected. 1=offline, but without timeout passing 2=connected.  -1 initially forces first loop update

macconnected1=-1
maccurrent1=0
timeout1=0

macconnected2=-1
maccurrent2=0
timeout2=0

macconnected3=-1
maccurrent3=0
timeout3=0

connected=-1

# total number of currently conencted devices.   
currentconnected=0

# Main loop.  
while true; do

# reset current status to 0. Two variables are used for each device.  The past known status and the current
# status.  Only a change is reported to.  Otherwise, it would constantly be updating with the current status
# creating unnecessary traffic for the router
maccurrent1=0
maccurrent2=0
maccurrent3=0

# Look for devices in the arp table
arpout=$(arp -n)
mac1seen=$(echo $arpout | grep -c $macdevice1 )
if [ $mac1seen -gt 0 ]; then
   maccurrent1=2
   timeout1=0
else
	if [ $timeout1 -gt -10 ]; then
	   maccurrent1=1
	   timeout1=$(($timeout1 - 1 ))
   else
	   maccurrent1=0
	   timeout1=-10 
   fi
fi

mac2seen=$(echo $arpout | grep -c $macdevice2 )
if [ $mac2seen -gt 0 ]; then
   maccurrent2=2
   timeout2=0
else
	if [ $timeout2 -gt -10 ]; then
	   maccurrent2=1
	   timeout2=$(($timeout2 - 1 ))
   else
	   maccurrent2=0
	   timeout2=-10 
   fi
fi

mac3seen=$(echo $arpout | grep -c $macdevice3 )
if [ $mac3seen -gt 0 ]; then
   maccurrent3=2
   timeout3=0
else
	if [ $timeout3 -gt -10 ]; then
	   maccurrent3=1
	   timeout3=$(($timeout3 - 1 ))
   else
	   maccurrent3=0
	   timeout3=-10 
   fi
fi

pres1=0
pres2=0
pres3=0
if [ $maccurrent1 -ge 1 ]; then
	pres1=1
fi
if [ $maccurrent2 -ge 1 ]; then
	pres2=1
fi
if [ $maccurrent3 -ge 1 ]; then
	pres3=1
fi

#grab the previous connected number for reporting.
connectedPrev=$connected

# Total up the number of devices connected.
connected=$(($pres1 + $pres2 + $pres3))

# Look for a change in status from the old known to the current status.
# If it changed, if the new state is 0 or 2: if the old state was 1, and the new state is 2 ignore the change, otherwise update.
if [ "$macconnected1" -ne "$maccurrent1" ] && [ "$maccurrent1" -ne 1 ] && !( [ "$maccurrent1" -eq 2 ] && [ "$macconnected1" -eq 1 ] ); then 
	wget -q "http://bet.trojka.us/hueProx?mac=$macdevice1&state=$maccurrent1&devices=$connected&devicesPrev=$connectedPrev"
    echo "$(date) $macdevice1 status: $maccurrent1 timeout: $timeout1 State changed"
fi
if [ "$macconnected2" -ne "$maccurrent2" ] && [ "$maccurrent2" -ne 1 ] && !( [ "$maccurrent2" -eq 2 ] && [ "$macconnected2" -eq 1 ] ); then 
	wget -q "http://bet.trojka.us/hueProx?mac=$macdevice2&state=$maccurrent2&devices=$connected&devicesPrev=$connectedPrev"
    echo "$(date) $macdevice2 status: $maccurrent2 timeout: $timeout2 State changed"
fi
if [ "$macconnected3" -ne "$maccurrent3" ] && [ "$maccurrent3" -ne 1 ] && !( [ "$maccurrent3" -eq 2 ] && [ "$macconnected3" -eq 1 ] ); then 
	wget -q "http://bet.trojka.us/hueProx?mac=$macdevice3&state=$maccurrent3&devices=$connected&devicesPrev=$connectedPrev"
    echo "$(date) $macdevice3 status: $maccurrent3 timeout: $timeout3 State changed"
fi

# Update the known status from the current.  Ready for the next loop.
macconnected1="$maccurrent1"
macconnected2="$maccurrent2"
macconnected3="$maccurrent3"

# Delay (sleep) depending on the connection status.
# No devices connected could delay less.  Once a device is connected, it could delay longer.
if [ $connected -gt 0 ]; then
   sleep $delay_occupied
else
   sleep $delay_unoccupied
fi
   
done  #end of main loop