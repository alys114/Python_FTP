# Author: Vincent.chan
# Blog: http://blog.alys114.com

import common
import constConfig

# 用户授权信息
data = {
	'user1':['e10adc3949ba59abbe56e057f20f883e','20MB'],
	'user2':['e10adc3949ba59abbe56e057f20f883e','20MB']
}
common.jsonDump(data,constConfig.USER_DB)


