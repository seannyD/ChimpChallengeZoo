#!/bin/sh
# write the files in a source folder to a destination 
# folder on a USB drive when it's connected
# scans the volumes folder for drives that are not
# listed in hard_drives, and attempts to write to it


sourceFolder="/home/think/Desktop/chimp-869990b/src/results/"  # folder to copy from
targetFolder="ZooResults/"  #folder to write to on USB (makes this if not present)
hard_drives1="cdrom" # hard drives not to write to, seperated by space.
hard_drives2="cdrom0"
volumesFolder='/media/'  # Where mounted devices appear

sleep_time="10s" # time between tests

writtenLately=false # variable to keep track of writing so files are ony written once per mounting
noTarget=true # has the for loop discovered a target to write to?

while true
do
echo 'testing'
noTarget=true
for i in `ls $volumesFolder`; do
	
	# if not one of the standard hard drives
#  if ! [[ $hard_drives =~ $i ]]; then
  if [ $i != $hard_drives1 ]; then
    if [ $i != $hard_drives2 ]; then
      echo "External drive present: $i $hard_drives1" 
      
      noTarget=false
      if [ $writtenLately = false ]; then
      
        writeTime=`date +%m_%d%_%H_%M_%S`
        curTargetFolder=$volumesFolder$i'/'$targetFolder$writeTime
        mkdir $volumesFolder$i'/'$targetFolder
        mkdir $curTargetFolder
        if cp -r $sourceFolder $curTargetFolder; then
            echo 'written'
        	writtenLately=true
        fi
      fi
   fi
  fi
done

if $noTarget; then
  writtenLately=false
fi
sleep $sleep_time

done