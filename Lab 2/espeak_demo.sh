
# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
now=$(date +"%T")
echo $now
espeak -ven+f2 -k5 -s150 --stdout  $now | aplay
 
