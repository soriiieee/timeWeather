#!/bin/bash
# get_CROSS.sh
# based by Maki OKADA(2018/08/21)
#            sorimachi.y(2020/01/30)  #remake
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


ulimit -s unlimited

#=======================================================================
# Set Time
#=======================================================================
##NOW_J=`date +%Y%m%d%H` #JST
#>>>>>>>>>>>>>>>>>>>>>>>test
# ex)2019.01.14 00Z -> 2019011414と記入
# DAY=`$TOOL/dtcomp_com 20190131000 $INI_J0 3`
MONTH=$1
COM=`basename $0`
LOGGER=${LOG}/${COM}.log

DAYS=`cat $TBL/month.tbl | awk '$1 == '$MONTH' {print $2}'`

#testnomi
# DAYS=10 #test
DD=$(( $DAYS*6*24 + 1))

# echo $DD
# echo $DAYS
# exit

# exit
# sfc
rm -f $OUT/*.dat
[ ! -e $OUT/sfc ] && mkdir -p $OUT/sfc
[ ! -e $OUT/amd ] && mkdir -p $OUT/amd 

echo "----m02--------setting ----------------" >> $LOGGER
echo "IMAD path $OUT/sfc" >> $LOGGER
echo "ISFC path $OUT/amd" >> $LOGGER

#=======================================================================
# make sfc
#=======================================================================

echo "`date`STRT  sfc data ---------" >> $LOGGER
START=`date`
rm -f $OUT/sfc/*.csv
python $SRC/make_sfc3.py $MONTH $DAYS $SYS #int
# mv $CSV/sfc*.csv $OUT/sfc/
echo "`date`END  sfc data ---------" >> $LOGGER

#=======================================================================
# make amd
#=======================================================================

echo "`date`STRT  amd data ---------" >> $LOGGER
START=`date`
# rm -f $OUT/*.dat
rm -f $OUT/amd/*.csv
python $SRC/make_amd3.py $MONTH $DAYS $SYS
mv $CSV/amd*.csv $OUT/amd/

echo "`date`END  amd data ---------" >> $LOGGER
exit