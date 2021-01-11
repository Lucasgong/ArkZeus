###
 # @Description: 
 # @Author: zgong
 # @Date: 2020-10-27 19:19:03
 # @LastEditTime: 2020-10-27 19:44:58
 # @LastEditors: zgong
 # @FilePath: /ArkZeus/ark.sh
 # @Reference: 
### 
alias adb="/usr/local/bin/adb"
cd `dirname $0` || exit 1
/Users/zgong/miniconda3/bin/python run.py >> log/run.log 2>&1