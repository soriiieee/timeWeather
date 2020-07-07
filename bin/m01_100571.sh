#!/bin/bash
# get_CROSS.sh
# based by Maki OKADA(2018/08/21)
#            sorimachi.y(2019/10/07)  #remake
#-----------------------------------------------------------------------
#=======================================================================
# Set Local Function
#=======================================================================
PRINT_ERR(){
  echo "!!! " $1 " NG. EXIT."
}


#=======================================================================
# Set Environment
#=======================================================================
DIR=`dirname $0`
. ${DIR}/com.conf
. ${DIR}/prod.conf

SETMIC
SETCHOKI

COM=`basename $0`

ulimit -s unlimited

#RUN_MODE="UNYO" #"UNYO" / "RETRY" / "local_mode"
RUN_MODE="RETRY" #"UNYO" / "RETRY" / "local_mode"

#=======================================================================
# Set Time
#=======================================================================
##NOW_J=`date +%Y%m%d%H` #JST
#>>>>>>>>>>>>>>>>>>>>>>>test
ID1=100571
MONTH=$1
LOGGER=$2


#honban unyou
INI_J0=${MONTH}"010000"
#debug

# INI_J0=${MONTH}"010000" #only test
INI_J1=`${TOOL}/dtinc_com $INI_J0 3 -1` #JST->UTC
INI_U0=`${TOOL}/dtinc_com $INI_J1 4 -9` #JST->UTC

# echo $NOW_U
# exit
#=======================================================================
# Get data
#=======================================================================

[ ! -e $DAT/${ID1} ] && mkdir -p $DAT/${ID1}
# rm -f $LOG100571
rm -f $DAT/*_nan.dat #init
rm -f $DAT/${ID1}/* #init
rm -f ../log/${ID1}_deco_syusei.log #init
# echo $OUT1
# exit
# <SHELL>
for DD in `seq 0 32`;do
INI_U1=`${TOOL}/dtinc_com $INI_U0 3 $DD`
# END=`date +%Y%m%d%H%M`  #JST

for HH in `seq 0 23`;do
INI_U2=`${TOOL}/dtinc_com $INI_U1 4 $HH`
for MI in 00 10 20 30 40 50 ;do
INI_U3=`${TOOL}/dtinc_com $INI_U2 5 $MI`
INI_J3=`${TOOL}/dtinc_com $INI_U3 4 9`

echo "python $SRC/100571_deco_shusei.py $DAT/${ID1} $INI_U3 $MONTH $SYS" >> $LOGGER
cd $SRC
python 100571_deco_shusei.py $DAT/${ID1} $INI_U3 $INI_J3 $MONTH $SYS
# exit
done #10min
done #hour
# exit
#logger
END=`date +%Y%m%d%H%M`  #JST
echo "END $ID1 $END $INI_U1 " >> $LOGGER
done #day
