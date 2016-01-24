SDK_DIR=/home/katie/Android/Sdk
ADB=$SDK_DIR/platform-tools/adb
RUN_ID=($($ADB shell "ls data/data/com.jprodevelopment.unscrabble/files/unscrabble" | sed 's/\([0-9]*\).*/\1/' | sort -r))
$ADB shell "ls data/data/com.jprodevelopment.unscrabble/files/unscrabble" | grep $RUN_ID | $(sed 's/\(.*\)/data\/data\/com.jprodevelopment.unscrabble\/files\/unscrabble\/\1/') | xargs $ADB pull

