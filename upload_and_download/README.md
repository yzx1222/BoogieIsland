# 个人报告（待完善）

~~这里主要记录一下各个文件的用途和我完成的部分的工作流程大人们整合的时候可以看情况改~~ ~~完整的报告还在写......~~

---

### 大致流程

#### <table><tr><td bgcolor=d0dfe0>上传</td></tr></table>

+ __开始上传文件__  
  - 前端：限制文件格式   
  *（对应 `documents/frontend/scr/components/FileUpload.vue`中的第`3`行和第`29-33`行）*

+ __加密文件__  
  - 前端：随机生成对称密钥并对文件进行加密，并加密对称密钥  
  *（对应 `documents/frontend/scr/components/FileUpload.vue`中的第`35-50`行）*  

+ __上传文件到后端__
  - 前端
    *（对应 `documents/frontend/scr/components/FileUpload.vue`中的第`53-64`行）*  

+ __后端接收并验证是否登录__  
  - 后端：使用`jwt_required`修饰器验证 
  *（对应 `/backend/app.py`）* 

+ __限制加密后文件大小__  
  - 后端 *（看 */backend/app.py*）*  

+ __存储到数据库__  
  - 后端 *（对应 */backend/app.py* 中的第`99-111`行）* 



#### <table><tr><td bgcolor=d0dfe0>下载</td></tr></table>

##### 已登录用户 
+ __下载请求__   
  - 前端访问download接口 *(`documents/scr/components/FileDownload.vue`)* ~~后面就只标文件了大人们翻一下~~
  - 后端检测是否存在文件、是否属于该用户，符合要求的话把加密后文件发送给前端 *（app.py)*  

+ __前端解密__   
  - 先解密对称密钥
  - 再解密文件内容 *(`documents/scr/components/FileDownload.vue`

--
  
  
##### 未登录用户
+ __下载请求__
  - 前端访问download_original接口
  - 后端检测是否存在文件，存在的话把加密文件发送给前端

+ __前端提供下载__


---

~~没提到的文件大多数都是创建Vue项目的时候自动生成的大人们可以不用管~~

---

![解释说明](%E8%A7%A3%E9%87%8A%E8%AF%B4%E6%98%8E%E6%B8%85%E5%8D%95.png)

+ 加解密在上面解释过了
+ 同一个用户不同文件使用不同的对称加密密钥，每次都随机生成一个，并使用AES-ECB,Master Key来加密对称密钥