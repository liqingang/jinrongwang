# 湘能物业接口测试用例

> 基于 `swagger2.0.json` 生成  
> BasePath: `/smarthome`  
> 公共请求头：`X-Lemonban-Media-Type`、`Content-Type`、`Authorization`（v2/v3 必填）  
> 成功约定：HTTP 200 且 `code="0"`，`msg` 为操作成功类提示

**鉴权说明（用例默认 v2，除非特别标注）：**
- v1：无鉴权
- v2：需 `Authorization: Bearer {token}`
- v3：需 token + timestamp + RSA(token前50位+时间戳) 签名

---

| 用例ID | 接口 | 测试场景 | 输入数据 | 预期响应状态 | 预期关键返回 |
|--------|------|---------|----------|-------------|------------|
| TC-001 | POST /user/register | 正常注册 | Headers: `X-Lemonban-Media-Type=lemonban.v1`, `Content-Type=application/json`; Body: `{"userName":"测试用户","pwd":"1234567a","rePwd":"1234567a","phone":"18650512136","verificationCode":"611203"}` | 200 | `code=0`，返回 UserVO（含 id、userName、phone） |
| TC-002 | POST /user/register | 缺少必填参数 userName | Body: `{"pwd":"1234567a","rePwd":"1234567a","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，提示用户名相关错误 |
| TC-003 | POST /user/register | 缺少必填参数 pwd | Body: `{"userName":"测试用户","rePwd":"1234567a","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，提示密码相关错误 |
| TC-004 | POST /user/register | 缺少验证码 | Body: `{"userName":"测试用户","pwd":"1234567a","rePwd":"1234567a","phone":"18650512136"}` | 200 | `code!=0`，提示验证码必填 |
| TC-005 | POST /user/register | 用户名长度边界-过短(3位) | Body: `{"userName":"abc","pwd":"1234567a","rePwd":"1234567a","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，用户名长度须 4~6 |
| TC-006 | POST /user/register | 用户名长度边界-过长(7位) | Body: `{"userName":"abcdefg","pwd":"1234567a","rePwd":"1234567a","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，用户名长度须 4~6 |
| TC-007 | POST /user/register | 用户名长度边界-最小合法(4位) | Body: `{"userName":"abcd","pwd":"1234567a","rePwd":"1234567a","phone":"18650519999","verificationCode":"有效验证码"}` | 200 | `code=0`，注册成功 |
| TC-008 | POST /user/register | 用户名长度边界-最大合法(6位) | Body: `{"userName":"abcdef","pwd":"1234567a","rePwd":"1234567a","phone":"18650518888","verificationCode":"有效验证码"}` | 200 | `code=0`，注册成功 |
| TC-009 | POST /user/register | 密码长度边界-过短(7位) | Body: `{"userName":"测试甲","pwd":"123456a","rePwd":"123456a","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，密码长度须 8~16 |
| TC-010 | POST /user/register | 密码长度边界-过长(17位) | Body: `{"userName":"测试甲","pwd":"1234567890123456a","rePwd":"1234567890123456a","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，密码长度须 8~16 |
| TC-011 | POST /user/register | 密码仅数字无字母 | Body: `{"userName":"测试甲","pwd":"12345678","rePwd":"12345678","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，密码须数字和字母组成 |
| TC-012 | POST /user/register | 两次密码不一致 | Body: `{"userName":"测试甲","pwd":"1234567a","rePwd":"1234567b","phone":"18650512136","verificationCode":"611203"}` | 200 | `code!=0`，提示两次密码不一致 |
| TC-013 | POST /user/register | 手机号格式非法 | Body: `{"userName":"测试甲","pwd":"1234567a","rePwd":"1234567a","phone":"12345","verificationCode":"611203"}` | 200 | `code!=0`，提示手机号非法 |
| TC-014 | POST /user/register | 手机号为空字符串 | Body: `{"userName":"测试甲","pwd":"1234567a","rePwd":"1234567a","phone":"","verificationCode":"611203"}` | 200 | `code!=0`，提示手机号必填/非法 |
| TC-015 | POST /user/register | 验证码错误 | Body: `{"userName":"测试甲","pwd":"1234567a","rePwd":"1234567a","phone":"18650512136","verificationCode":"000000"}` | 200 | `code!=0`，提示验证码错误 |
| TC-016 | POST /user/register | 参数类型错误-phone为数字 | Body: `{"userName":"测试甲","pwd":"1234567a","rePwd":"1234567a","phone":18650512136,"verificationCode":"611203"}` | 200 | `code!=0` 或参数解析失败 |
| TC-017 | POST /user/login | 正常登录 | Headers: `X-Lemonban-Media-Type=lemonban.v1`, `Content-Type=application/json`; Body: `{"userName":"猪八戒","pwd":"1234567a"}` | 200 | `code=0`，data 含 token_info.token |
| TC-018 | POST /user/login | 缺少 userName | Body: `{"pwd":"1234567a"}` | 200 | `code!=0`，提示用户名必填 |
| TC-019 | POST /user/login | 缺少 pwd | Body: `{"userName":"猪八戒"}` | 200 | `code!=0`，提示密码必填 |
| TC-020 | POST /user/login | 用户名不存在 | Body: `{"userName":"不存在用户xyz","pwd":"1234567a"}` | 200 | `code!=0`，提示用户名或密码错误 |
| TC-021 | POST /user/login | 密码错误 | Body: `{"userName":"猪八戒","pwd":"wrongpwd1"}` | 200 | `code!=0`，提示用户名或密码错误 |
| TC-022 | POST /user/login | 空用户名/空密码 | Body: `{"userName":"","pwd":""}` | 200 | `code!=0`，参数校验失败 |
| TC-023 | GET /verificationCode/message | 正常获取验证码 | Headers: `X-Lemonban-Media-Type=lemonban.v1`; Query: `phone=18650512136` | 200 | `code=0`，data 为验证码字符串或发送成功提示 |
| TC-024 | GET /verificationCode/message | 缺少 phone | 不传 phone | 200 | `code!=0`，提示手机号必填 |
| TC-025 | GET /verificationCode/message | phone 为空 | Query: `phone=` | 200 | `code!=0`，提示手机号非法 |
| TC-026 | GET /verificationCode/message | phone 格式非法 | Query: `phone=abc` | 200 | `code!=0`，提示手机号格式错误 |
| TC-027 | GET /verificationCode/message | phone 长度边界-过短 | Query: `phone=1380013800`（10位） | 200 | `code!=0`，手机号格式错误 |
| TC-028 | GET /verificationCode/message | phone 长度边界-过长 | Query: `phone=138001380001`（12位） | 200 | `code!=0`，手机号格式错误 |
| TC-029 | POST /file/upload | 正常上传 jpg≤100KB | Headers: `X-Lemonban-Media-Type=lemonban.v2`, `Authorization=Bearer {token}`；formData: 合法 jpg 文件 | 200 | `code=0`，data 为文件 URL |
| TC-030 | POST /file/upload | 正常上传 png≤100KB | formData: 合法 png 文件 | 200 | `code=0`，data 为文件 URL |
| TC-031 | POST /file/upload | 缺少 file | 不传 file | 200 | `code!=0`，提示文件必填 |
| TC-032 | POST /file/upload | 文件类型非法(txt) | formData: `.txt` 文件 | 200 | `code!=0`，仅支持 jpg/png |
| TC-033 | POST /file/upload | 文件大小边界-超过100KB | formData: 101KB 的 jpg | 200 | `code!=0`，提示文件过大 |
| TC-034 | POST /file/upload | 文件大小边界-恰好100KB | formData: 100KB 的 jpg | 200 | `code=0`，上传成功 |
| TC-035 | POST /file/upload | 鉴权异常-无 Token(v2) | Headers: `X-Lemonban-Media-Type=lemonban.v2`，无 Authorization | 401/200 | 鉴权失败，`code!=0` 或未授权 |
| TC-036 | POST /file/upload | 鉴权异常-非法 Token | `Authorization=Bearer invalid_token` | 401/200 | 鉴权失败 |
| TC-037 | POST /file/upload | 鉴权异常-过期 Token | `Authorization=Bearer {expired_token}` | 401/200 | 鉴权失败，提示 token 过期 |
| TC-038 | PUT /merchant/complete | 正常完善公司信息 | Headers: v2+Token+JSON；Body: `{"merchantName":"青海文梅科技有限公司","merchantType":2,"address":"湖南省长沙市岳麓区xx街道","tel":"18888888888","legalPerson":"韩信","licenseCode":"xh430646464sdfa","licenseUrl":"http://127.0.0.1/smarthome/aaa.jpg","registerAuthority":"城中区派出所","establishDate":"2021-04-02","validityDate":"2033-05-02","userId":1}` | 200 | `code=0`，返回 MerchantDto |
| TC-039 | PUT /merchant/complete | 缺少必填字段 merchantName | Body 去掉 merchantName | 200 | `code!=0`，提示公司名必填 |
| TC-040 | PUT /merchant/complete | merchantName 长度边界-过长(21) | `merchantName` 为 21 个字符 | 200 | `code!=0`，长度须 1~20 |
| TC-041 | PUT /merchant/complete | legalPerson 长度边界-过长(6) | `legalPerson":"六个字的名"` | 200 | `code!=0`，法人长度须 1~5 |
| TC-042 | PUT /merchant/complete | licenseCode 长度边界-过短(14) | `licenseCode` 14 位 | 200 | `code!=0`，证件号长度须 15~18 |
| TC-043 | PUT /merchant/complete | licenseCode 长度边界-过长(19) | `licenseCode` 19 位 | 200 | `code!=0`，证件号长度须 15~18 |
| TC-044 | PUT /merchant/complete | merchantType 非法值 | `merchantType":9` | 200 | `code!=0`，类型仅允许 2/3 |
| TC-045 | PUT /merchant/complete | 日期格式非法 | `establishDate":"2021/04/02"` | 200 | `code!=0`，日期须 yyyy-MM-dd |
| TC-046 | PUT /merchant/complete | address 长度边界-过长(31) | address 31 字符 | 200 | `code!=0`，地址长度不能大于 30 |
| TC-047 | PUT /merchant/complete | tel 格式非法 | `tel":"123"` | 200 | `code!=0`，手机号非法 |
| TC-048 | PUT /merchant/complete | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-049 | POST /community/add | 正常添加小区 | Body: `{"communityName":"八家湾小区","address":"青海省西宁市城东区格兰小镇","nearbyLandmarks":"王府井","userId":1}` | 200 | `code=0`，返回 Community |
| TC-050 | POST /community/add | 缺少 communityName | Body 无 communityName | 200 | `code!=0`，小区名称必填 |
| TC-051 | POST /community/add | communityName 长度边界-过短(4) | `communityName":"八家湾小"` | 200 | `code!=0`，名称长度须 5~10 |
| TC-052 | POST /community/add | communityName 长度边界-过长(11) | `communityName` 11 字符 | 200 | `code!=0`，名称长度须 5~10 |
| TC-053 | POST /community/add | communityName 最小合法(5) | `communityName":"八家湾小区"` | 200 | `code=0` |
| TC-054 | POST /community/add | address 长度边界-空 | `address":""` | 200 | `code!=0`，地址长度须 1~30 |
| TC-055 | POST /community/add | address 长度边界-过长(31) | address 31 字符 | 200 | `code!=0` |
| TC-056 | POST /community/add | nearbyLandmarks 长度边界-过长(11) | 地标 11 字符 | 200 | `code!=0`，地标长度须 1~10 |
| TC-057 | POST /community/add | userId 类型错误 | `userId":"abc"` | 200 | `code!=0` 或类型错误 |
| TC-058 | POST /community/add | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-059 | POST /community/examine | 正常审核通过 | Body: `{"communityId":1,"state":1,"remark":"资料齐全，审核通过"}` | 200 | `code=0` |
| TC-060 | POST /community/examine | 正常审核不通过 | Body: `{"communityId":1,"state":2,"remark":"地址不清晰"}` | 200 | `code=0` |
| TC-061 | POST /community/examine | 缺少 communityId | Body: `{"state":1,"remark":"通过"}` | 200 | `code!=0` |
| TC-062 | POST /community/examine | state 非法值 | `state":9` | 200 | `code!=0`，仅允许 1/2 |
| TC-063 | POST /community/examine | remark 为空 | `remark":""` | 200 | `code!=0`，原因必填 |
| TC-064 | POST /community/examine | communityId 不存在 | `communityId":999999` | 200 | `code!=0`，小区不存在 |
| TC-065 | POST /community/in | 正常申请入驻 | Query: `communityId=1&userId=1`（文档说明可不设 Content-Type） | 200 | `code=0`，返回 CommuMember |
| TC-066 | POST /community/in | 缺少 communityId | Query: `userId=1` | 200 | `code!=0` |
| TC-067 | POST /community/in | 缺少 userId | Query: `communityId=1` | 200 | `code!=0` |
| TC-068 | POST /community/in | 参数类型错误 | Query: `communityId=abc&userId=1` | 200 | `code!=0` |
| TC-069 | POST /community/in | 不存在的小区 | Query: `communityId=999999&userId=1` | 200 | `code!=0` |
| TC-070 | POST /community/in | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-071 | POST /community/in/examine | 正常审核入驻 | Body: `{"commuMemberId":1,"state":1,"remark":"同意入驻"}` | 200 | `code=0` |
| TC-072 | POST /community/in/examine | 缺少 commuMemberId | Body: `{"state":1,"remark":"同意"}` | 200 | `code!=0` |
| TC-073 | POST /community/in/examine | state 非法 | `state":0` | 200 | `code!=0`，仅允许 1/2 |
| TC-074 | POST /community/in/examine | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-075 | POST /building/add | 正常添加楼栋 | Body: `{"buildingName":"1号楼","buildingNum":"001","communityId":1,"floorage":300.0,"remark":"这是第一栋楼","userId":1}` | 200 | `code=0`，返回 BuildingVO |
| TC-076 | POST /building/add | 缺少 buildingName | Body 无 buildingName | 200 | `code!=0` |
| TC-077 | POST /building/add | buildingName 长度边界-过长(11) | buildingName 11 字符 | 200 | `code!=0`，长度不能大于 10 |
| TC-078 | POST /building/add | buildingName 最大合法(10) | buildingName 10 字符 | 200 | `code=0` |
| TC-079 | POST /building/add | buildingNum 非数字 | `buildingNum":"abc"` | 200 | `code!=0`，只能是数字 |
| TC-080 | POST /building/add | floorage 边界-等于0 | `floorage":0` | 200 | `code!=0`，须大于 0 |
| TC-081 | POST /building/add | floorage 边界-负数 | `floorage":-1` | 200 | `code!=0` |
| TC-082 | POST /building/add | floorage 边界-极小正数 | `floorage":0.01` | 200 | `code=0` |
| TC-083 | POST /building/add | remark 长度边界-过长(51) | remark 51 字符 | 200 | `code!=0`，备注不能大于 50 |
| TC-084 | POST /building/add | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-085 | GET /building/{page}/{size}/list | 正常分页列表 | Path: `/building/1/10/list` | 200 | `code=0`，data 含 records/total/current/size |
| TC-086 | GET /building/{page}/{size}/list | 按 buildingId 筛选 | `/building/1/10/list?buildingId=1` | 200 | `code=0`，结果匹配 buildingId |
| TC-087 | GET /building/{page}/{size}/list | 按 buildingNum 筛选 | `?buildingNum=001` | 200 | `code=0` |
| TC-088 | GET /building/{page}/{size}/list | 按 buildingName 筛选 | `?buildingName=1号楼` | 200 | `code=0` |
| TC-089 | GET /building/{page}/{size}/list | page 边界-第1页 | `/building/1/10/list` | 200 | `code=0`，current=1 |
| TC-090 | GET /building/{page}/{size}/list | page 边界-0或负数 | `/building/0/10/list` | 200 | `code!=0` 或空数据/异常 |
| TC-091 | GET /building/{page}/{size}/list | size 边界-1 | `/building/1/1/list` | 200 | `code=0`，至多 1 条 |
| TC-092 | GET /building/{page}/{size}/list | size 边界-超大 | `/building/1/9999/list` | 200 | `code=0` 或受限提示 |
| TC-093 | GET /building/{page}/{size}/list | page/size 类型错误 | `/building/abc/10/list` | 200/400 | 参数类型错误 |
| TC-094 | GET /building/{page}/{size}/list | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-095 | POST /unit/add | 正常添加单元 | Body: `{"buildingId":1,"unitNum":"001","floorage":160.0,"layerCount":22,"lift":1,"remark":"这是一个备注","userId":3}` | 200 | `code=0`，返回 UnitVO |
| TC-096 | POST /unit/add | 缺少 buildingId | Body 无 buildingId | 200 | `code!=0` |
| TC-097 | POST /unit/add | unitNum 非数字 | `unitNum":"A01"` | 200 | `code!=0`，只能是数字 |
| TC-098 | POST /unit/add | floorage≤0 | `floorage":0` | 200 | `code!=0`，须大于 0 |
| TC-099 | POST /unit/add | layerCount 边界-0 | `layerCount":0` | 200 | `code!=0`，须正整数 |
| TC-100 | POST /unit/add | layerCount 负数 | `layerCount":-1` | 200 | `code!=0` |
| TC-101 | POST /unit/add | lift 非法值 | `lift":3` | 200 | `code!=0`，仅允许 1/2 |
| TC-102 | POST /unit/add | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-103 | POST /room/add | 正常添加房屋 | Body: `{"communityId":1,"unitId":1,"roomNum":"001","layer":15,"builtUpArea":90.0,"roomStyle":"三室一厅","remark":"这是一个备注","userId":1}` | 200 | `code=0`，返回 RoomVO |
| TC-104 | POST /room/add | 缺少必填 roomNum | Body 无 roomNum | 200 | `code!=0` |
| TC-105 | POST /room/add | roomNum 非数字 | `roomNum":"A01"` | 200 | `code!=0`，须为大于 0 的数字 |
| TC-106 | POST /room/add | builtUpArea≤0 | `builtUpArea":0` | 200 | `code!=0` |
| TC-107 | POST /room/add | roomStyle 长度边界-过短(3) | `roomStyle":"三室"` | 200 | `code!=0`，长度须 4~8 |
| TC-108 | POST /room/add | roomStyle 长度边界-过长(9) | roomStyle 9 字符 | 200 | `code!=0` |
| TC-109 | POST /room/add | roomStyle 最小合法(4) | `roomStyle":"一室一"` | 200 | `code=0`（若业务允许）或格式校验 |
| TC-110 | POST /room/add | layer 类型错误 | `layer":"十五"` | 200 | `code!=0` |
| TC-111 | POST /room/add | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-112 | POST /owner/add | 正常添加业主 | Body: `{"ownerName":"张三","age":20,"sex":0,"phone":"16612345678","communityId":1,"userId":1,"idCard":"430665200011034156","remark":"这是一个备注"}` | 200 | `code=0`，返回 OwnerVO |
| TC-113 | POST /owner/add | 缺少 ownerName | Body 无 ownerName | 200 | `code!=0` |
| TC-114 | POST /owner/add | ownerName 长度边界-过长(11) | ownerName 11 字符 | 200 | `code!=0`，不能大于 10 |
| TC-115 | POST /owner/add | age 边界-0 | `age":0` | 200 | `code!=0`，须为正整数且 <200 |
| TC-116 | POST /owner/add | age 边界-199 | `age":199` | 200 | `code=0` |
| TC-117 | POST /owner/add | age 边界-200 | `age":200` | 200 | `code!=0`，须小于 200 |
| TC-118 | POST /owner/add | age 负数 | `age":-1` | 200 | `code!=0` |
| TC-119 | POST /owner/add | sex 非法值 | `sex":2` | 200 | `code!=0`，仅允许 0/1 |
| TC-120 | POST /owner/add | phone 格式非法 | `phone":"123"` | 200 | `code!=0` |
| TC-121 | POST /owner/add | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-122 | POST /owner/bind | 正常绑定业主 | Body: `{"communityId":1,"communityName":"八家湾","ownerName":"张三","phone":"15674589632","pwd":"1234567a","msgCode":"123456","idCard":"430661200105067412"}` | 200 | `code=0` |
| TC-123 | POST /owner/bind | 缺少 msgCode | Body 无 msgCode | 200 | `code!=0` |
| TC-124 | POST /owner/bind | 验证码错误 | `msgCode":"000000"` | 200 | `code!=0` |
| TC-125 | POST /owner/bind | pwd 长度边界-过短(7) | `pwd":"123456a"` | 200 | `code!=0`，长度须 8~16 |
| TC-126 | POST /owner/bind | pwd 长度边界-过长(17) | pwd 17 字符 | 200 | `code!=0` |
| TC-127 | POST /owner/bind | 缺少 communityId | Body 无 communityId | 200 | `code!=0` |
| TC-128 | POST /owner/bind | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-129 | POST /owner/login | 正常业主登录 | Body: `{"phone":"13312345678","pwd":"1234567a"}` | 200 | `code=0`，data 含 token 信息 |
| TC-130 | POST /owner/login | 缺少 phone | Body: `{"pwd":"1234567a"}` | 200 | `code!=0` |
| TC-131 | POST /owner/login | 缺少 pwd | Body: `{"phone":"13312345678"}` | 200 | `code!=0` |
| TC-132 | POST /owner/login | 手机号不存在 | `phone":"19900000000"` | 200 | `code!=0` |
| TC-133 | POST /owner/login | 密码错误 | 正确 phone + 错误 pwd | 200 | `code!=0` |
| TC-134 | POST /owner/login | phone 为空 | `phone":""` | 200 | `code!=0` |
| TC-135 | POST /owner/checkIn | 正常入住 | Body: `{"ownerId":1,"roomId":1,"userId":1}` | 200 | `code=0`，返回 OwnerRoomVO |
| TC-136 | POST /owner/checkIn | 缺少 ownerId | Body 无 ownerId | 200 | `code!=0` |
| TC-137 | POST /owner/checkIn | 缺少 roomId | Body 无 roomId | 200 | `code!=0` |
| TC-138 | POST /owner/checkIn | 不存在的 roomId | `roomId":999999` | 200 | `code!=0` |
| TC-139 | POST /owner/checkIn | 参数类型错误 | `ownerId":"abc"` | 200 | `code!=0` |
| TC-140 | POST /owner/checkIn | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-141 | GET /owner/room/{userId} | 正常查询我的房屋 | Path: `/owner/room/1` | 200 | `code=0`，data 为 RoomVO 列表 |
| TC-142 | GET /owner/room/{userId} | userId 不存在 | `/owner/room/999999` | 200 | `code=0` 且空列表，或 `code!=0` |
| TC-143 | GET /owner/room/{userId} | userId 类型错误 | `/owner/room/abc` | 200/400 | 参数类型错误 |
| TC-144 | GET /owner/room/{userId} | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-145 | GET /owner/room/{userId} | 权限不足-查他人房屋 | 用 A 用户 token 访问 `/owner/room/{B的userId}` | 401/200 | 权限不足或无数据 |
| TC-146 | POST /junkRequirement/publish | 正常发布旧货出售 | Body: `{"type":2,"classification":2,"communityId":1,"context":"出售二手冰箱","publishUserLink":"15808569874","referencePrice":200.0,"userId":10}` | 200 | `code=0`，返回 JunkRequirementVO |
| TC-147 | POST /junkRequirement/publish | 正常发布需求 | Body: `{"type":3,"classification":8,"communityId":1,"context":"求购一张书桌","publishUserLink":"15808569874","referencePrice":200.0,"userId":10}` | 200 | `code=0` |
| TC-148 | POST /junkRequirement/publish | 缺少 context | Body 无 context | 200 | `code!=0` |
| TC-149 | POST /junkRequirement/publish | context 长度边界-空 | `context":""` | 200 | `code!=0`，长度须 1~200 |
| TC-150 | POST /junkRequirement/publish | context 长度边界-过长(201) | context 201 字符 | 200 | `code!=0` |
| TC-151 | POST /junkRequirement/publish | context 最大合法(200) | context 200 字符 | 200 | `code=0` |
| TC-152 | POST /junkRequirement/publish | referencePrice≤0 | `referencePrice":0` | 200 | `code!=0`，须大于 0 |
| TC-153 | POST /junkRequirement/publish | type 非法值 | `type":9` | 200 | `code!=0`，仅允许 2/3 |
| TC-154 | POST /junkRequirement/publish | classification 非法值 | `classification":1` | 200 | `code!=0`，仅允许 2/8 |
| TC-155 | POST /junkRequirement/publish | 联系电话非法 | `publishUserLink":"123"` | 200 | `code!=0` |
| TC-156 | POST /junkRequirement/publish | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-157 | POST /rent/room/publish | 正常发布出租 | Body: `{"roomId":1,"communityId":1,"communityName":"八家湾小区","ownerName":"张三","ownerTel":"15765417896","rentTitle":"豪华三房，拎包入住！","rentDesc":"家电齐全，周边配套齐全","price":800.0,"rentingType":1,"paymentType":2,"checkIn":1}` | 200 | `code=0`，返回 RentVO |
| TC-158 | POST /rent/room/publish | 缺少 rentTitle | Body 无 rentTitle | 200 | `code!=0` |
| TC-159 | POST /rent/room/publish | rentTitle 长度边界-过短(4) | rentTitle 4 字符 | 200 | `code!=0`，长度须 5~30 |
| TC-160 | POST /rent/room/publish | rentTitle 长度边界-过长(31) | rentTitle 31 字符 | 200 | `code!=0` |
| TC-161 | POST /rent/room/publish | rentTitle 最小合法(5) | rentTitle 5 字符 | 200 | `code=0` |
| TC-162 | POST /rent/room/publish | rentingType 非法 | `rentingType":9` | 200 | `code!=0`，仅允许 1/2 |
| TC-163 | POST /rent/room/publish | paymentType 非法 | `paymentType":9` | 200 | `code!=0`，仅允许 1/2/3 |
| TC-164 | POST /rent/room/publish | checkIn 非法 | `checkIn":9` | 200 | `code!=0`，仅允许 1/2 |
| TC-165 | POST /rent/room/publish | price 边界-0 | `price":0` | 200 | `code!=0` 或业务拒绝 |
| TC-166 | POST /rent/room/publish | price 负数 | `price":-100` | 200 | `code!=0` |
| TC-167 | POST /rent/room/publish | ownerTel 非法 | `ownerTel":"abc"` | 200 | `code!=0` |
| TC-168 | POST /rent/room/publish | 无 Token(v2) | 不带 Authorization | 401/200 | 鉴权失败 |
| TC-169 | POST /user/login | 鉴权版本 v2 登录后拿 token | Headers: `X-Lemonban-Media-Type=lemonban.v2`；Body 合法账号 | 200 | `code=0`，返回 token，后续接口可用 |
| TC-170 | 公共鉴权 | v2 带错误格式 Authorization | `Authorization=token_without_Bearer` | 401/200 | 鉴权失败（须 `Bearer ` 前缀+空格） |
| TC-171 | 公共鉴权 | v3 无 sign/timestamp | Media-Type=lemonban.v3，仅带 Token | 401/200 | 鉴权失败 |
| TC-172 | 公共鉴权 | POST 缺少 Content-Type | POST JSON 接口不设 Content-Type | 200/415 | 请求体解析失败或媒体类型错误 |

---

## 覆盖说明

| 模块 | 接口数 | 用例范围 |
|------|--------|----------|
| 用户注册/登录 | 2 | TC-001 ~ TC-022, TC-169 |
| 短信验证码 | 1 | TC-023 ~ TC-028 |
| 文件上传 | 1 | TC-029 ~ TC-037 |
| 商户信息 | 1 | TC-038 ~ TC-048 |
| 小区相关 | 4 | TC-049 ~ TC-074 |
| 楼栋相关 | 2 | TC-075 ~ TC-094 |
| 单元相关 | 1 | TC-095 ~ TC-102 |
| 房屋相关 | 1 | TC-103 ~ TC-111 |
| 业主相关 | 5 | TC-112 ~ TC-145 |
| 旧货/需求 | 1 | TC-146 ~ TC-156 |
| 出租相关 | 1 | TC-157 ~ TC-168 |
| 公共鉴权 | - | TC-170 ~ TC-172 |

**合计：172 条用例**，覆盖正常流程、参数缺失、类型错误、边界值、鉴权异常。

> 注：文档未给出全部业务错误码明细（见「通用返回码」docx）。业务失败统一以 HTTP 200 + `code!=0` 断言；若实际环境对鉴权失败返回 401，以实际为准调整「预期响应状态」。
