<template>
  <div >
    <div class="bt" >

      <el-button type="text" size="medium" icon="el-icon-arrow-left" @click="back" v-if="path=='/'?false:true">返回上一级</el-button>
      <el-button type="primary" size="medium" icon="el-icon-upload2" @click="dialogVisible = true">上传文件</el-button>
      <el-button  size="medium" @click="addfolder = true">新建文件夹</el-button>

      <el-dialog
        title="输入文件名字"
        :visible.sync="addfolder"
        width="20%"
       >
        <el-input v-model="input" placeholder="请输入内容"></el-input>
        <span slot="footer" class="dialog-footer">
    <el-button @click="addfolder = false">取 消</el-button>
    <el-button type="primary" @click="newfolder">确 定</el-button>
  </span>
      </el-dialog>
      <el-dialog
        title="上传"
        :visible.sync="dialogVisible"
        width="30%"
        :before-close="handleClose">
        <el-upload
          class="upload-demo"
          drag
          action="upload"
          :before-upload="beforeUpload"
          multiple

          v-loading="loading"
          element-loading-text="正在上传"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip"></div>
        </el-upload>
        <span slot="footer" class="dialog-footer">
  </span>
      </el-dialog>
      <div id="search"><input placeholder="请输入内容" class="search" v-model="keywords"/><i class="el-icon-search"></i>
      </div>
    </div>
    <el-table :data="search(keywords)"  :height="height">
      <el-table-column prop="name" label="文件名" width="800">
        <template slot-scope="{row}">
          <img :src="'../../static/img/'+row.img" alt="" style="cursor: default;
display: block;
height: 26px;
width: 26px;
position: absolute;
left:0px;
top: 10px;">
          <a href="javascript:void(0)" style="position: absolute;
left:40px;top: 12px;" @click="next(row.name)">{{row.name}}</a>

        </template>
      </el-table-column >
      <el-table-column prop="size" label="大小" width="270">
      </el-table-column>
      <el-table-column prop="time" label="修改日期" width="220">
      </el-table-column>
      <el-table-column>
        <template slot-scope="{row,$index}">
        <el-tooltip class="item" effect="dark" content="下载" placement="bottom-start">
          <el-button type="text"><i class="el-icon-download" @click="download(row.name)" ></i></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="删除" placement="bottom-start" >
          <el-button type="text"><i class="el-icon-delete" @click="del(row.name,$index)" ></i></el-button>
        </el-tooltip>

        </template>
      </el-table-column>
    </el-table>

  </div>

</template>

<script>
import { Button ,Dialog, Input, Upload,Table,TableColumn} from 'element-ui';
  export default {
    name: 'Right',
    data() {
      return {
        input:'',
        height: window.innerHeight -62 -80 -40 ,
        tableData: [],
        keywords: '',
        dialogVisible: false,
        loading:false,
        path:'/',
        username:localStorage.getItem('name'),
        addfolder:false
      }
    },
    components: {
    'el-button': Button, 
    'el-dialog': Dialog,
    'el-input' : Input,
    'el-upload': Upload,
    'el-table' : Table,
    'el-table-column' :TableColumn
  },
    created() {

this.init()
    },
    methods: {
      init(){
        localStorage.setItem('path','/')
        this.$http.post(this.$HOST + 'v2/filelist', this.$qs.stringify({
          sign: this.$sign,
          username:localStorage.getItem('name')
        })).then(res => {

          res.data.data.dir.forEach(item => {
            if (item.size == '') {
              var size = '-'
            } else {
              if (item.size < 1048576) {
                var size = (item.size / 1024).toFixed(2) + 'KB'
              } else if (item.size > 1048576 && item.size < 1073741824) {
                var size = (item.size / 1024 / 1024).toFixed(2) + 'MB'
              } else if (item.size > 1073741824) {
                var size = (item.size / 1024 / 1024 / 1024).toFixed(2) + 'GB'
              }
            }
            this.tableData.push({name: item.name, time: item.mtime, img: item.img, size: size})
          })
          res.data.data.file.forEach(item => {
            if (item.size == '') {
              var size = '-'
            } else {
              if (item.size < 1048576) {
                var size = (item.size / 1024).toFixed(2) + 'KB'
              } else if (item.size > 1048576 && item.size < 1073741824) {
                var size = (item.size / 1024 / 1024).toFixed(2) + 'MB'
              } else if (item.size > 1073741824) {
                var size = (item.size / 1024 / 1024 / 1024).toFixed(2) + 'GB'
              }
            }
            this.tableData.push({name: item.name, time: item.mtime, img: item.img, size: size})
          })
        })
      },
      search(key) {
        //搜索
        var newlist = []
        this.tableData.forEach(item => {
          if (item.name.indexOf(key) != -1) {
            newlist.push(item)
          }
        })
        return newlist
      },
      handleClose(done) {
        done();
        // this.$confirm('确认关闭？')
        //   .then(_ => {
        //     done();
        //   })
        //   .catch(_ => {
        //   });
      },
        beforeUpload(file){
          this.loading=true
    let fd = new FormData();
    fd.append('file',file);//传文件
    fd.append('sign',this.$sign);//传其他参数
    fd.append('username',localStorage.getItem('name'));//传其他参数
    fd.append('path',localStorage.getItem('path'));//传其他参数
          var that=this
    this.$http.post(this.$HOST+'v2/upload',fd).then(res=>{

     if(res.data.code=='0'){
       this.dialogVisible=false
       that.tableData=[]
       that.$message({
         showClose: true,
         message: '上传成功',
         type: 'success'
       });
       that.loading=false
       this.init()
     }
    else if(res.data.code=='2'){
       that.$message({
         showClose: true,
         message: '文件已存在',
         type: 'warning'
       });
     }
      that.loading=false
    })
  },
      del(name,index){
        this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.tableData.splice(index,1)
          this.$http.post(this.$HOST+'v2/delfile',this.$qs.stringify({
            sign:this.$sign,
            name:localStorage.getItem('path')+name,
            username:this.username
          })).then(res=>{
            if(res.data.code==0){
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            }
            else{
              this.$message({
                type: 'warning',
                message: '删除失败!'
              });
            }

          })

        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      },
      download(name){
        window.location.href=this.$HOST+'v2/download?username='+this.username+'&name='+name
      },
      newfolder(){
        this.$http.post(this.$HOST+'v2/newfolder',this.$qs.stringify({
          sign:this.$sign,
          username:this.username,
          path:localStorage.getItem('path'),
          fname:this.input
        })).then(res=>{
            if(res.data.code==0){
              this.addfolder=false
              this.input=''

              this.next('')
              this.$alert('创建文件夹成功', '提示', {
                confirmButtonText: '确定',
                callback: action => {
                  this.$message({
                    type: 'info',
                    message:"再见"
                  });
                }
              });
            }
            else{
              this.$alert('创建是失败，文件夹已存在', '提示', {
                confirmButtonText: '确定',
                callback: action => {
                  this.$message({
                    type: 'info',
                    message:"再见"
                  });
                }
              });
            }
        })
      },
      next(name)  {
        var newpath=localStorage.getItem('path')+name+'/'
        this.path=newpath
        this.$http.post(this.$HOST + 'v2/filelist', this.$qs.stringify({
          sign: this.$sign,
          username:localStorage.getItem('name'),
          path:newpath

        })).then(res => {
          localStorage.setItem('path',newpath)
          this.tableData=[]
          res.data.data.dir.forEach(item => {
            if (item.size == '') {
              var size = '-'
            } else {
              if (item.size < 1048576) {
                var size = (item.size / 1024).toFixed(2) + 'KB'
              } else if (item.size > 1048576 && item.size < 1073741824) {
                var size = (item.size / 1024 / 1024).toFixed(2) + 'MB'
              } else if (item.size > 1073741824) {
                var size = (item.size / 1024 / 1024 / 1024).toFixed(2) + 'GB'
              }
            }
            this.tableData.push({name: item.name, time: item.mtime, img: item.img, size: size})
          })
          res.data.data.file.forEach(item => {
            if (item.size == '') {
              var size = '-'
            } else {
              if (item.size < 1048576) {
                var size = (item.size / 1024).toFixed(2) + 'KB'
              } else if (item.size > 1048576 && item.size < 1073741824) {
                var size = (item.size / 1024 / 1024).toFixed(2) + 'MB'
              } else if (item.size > 1073741824) {
                var size = (item.size / 1024 / 1024 / 1024).toFixed(2) + 'GB'
              }
            }
            this.tableData.push({name: item.name, time: item.mtime, img: item.img, size: size})
          })
        })


      },
      back(){
       // console.log( localStorage.getItem('path').split('/'))
        var str=localStorage.getItem('path').split('/')
        str.splice(0,1)
        str.splice(str.length-1,1)
        str.splice(str.length-1,1)
        var backpath='/'
        str.forEach(item=>{
          backpath+=item+'/'
        })
        this.path=backpath
        this.$http.post(this.$HOST + 'v2/filelist', this.$qs.stringify({
          sign: this.$sign,
          username:localStorage.getItem('name'),
          path:backpath

        })).then(res => {
          localStorage.setItem('path',backpath)
          this.tableData=[]
          res.data.data.dir.forEach(item => {
            if (item.size == '') {
              var size = '-'
            } else {
              if (item.size < 1048576) {
                var size = (item.size / 1024).toFixed(2) + 'KB'
              } else if (item.size > 1048576 && item.size < 1073741824) {
                var size = (item.size / 1024 / 1024).toFixed(2) + 'MB'
              } else if (item.size > 1073741824) {
                var size = (item.size / 1024 / 1024 / 1024).toFixed(2) + 'GB'
              }
            }
            this.tableData.push({name: item.name, time: item.mtime, img: item.img, size: size})
          })
          res.data.data.file.forEach(item => {
            if (item.size == '') {
              var size = '-'
            } else {
              if (item.size < 1048576) {
                var size = (item.size / 1024).toFixed(2) + 'KB'
              } else if (item.size > 1048576 && item.size < 1073741824) {
                var size = (item.size / 1024 / 1024).toFixed(2) + 'MB'
              } else if (item.size > 1073741824) {
                var size = (item.size / 1024 / 1024 / 1024).toFixed(2) + 'GB'
              }
            }
            this.tableData.push({name: item.name, time: item.mtime, img: item.img, size: size})
          })
        })

      }
      }
    }
</script>
<style scoped>
  /* 通用样式 */
  .bt {
    max-width: 100%;
    background-color: white;
    height: 40px;
    font: 12px/1.5 "Microsoft YaHei", arial, SimSun, "宋体";
    line-height: 30px;
  }

  .nav {
    max-width: 100%;
    background-color: white;
    height: 20px;
    font-size: 8px;
    line-height: 20px;
  }

  .el-table-column {
    max-height: 48px;
    line-height: 48px;
  }

  .el-table {
    max-width: 100%;
    font: 12px/1.5 "Microsoft YaHei", arial, SimSun, "宋体";
  }

  #search {
    width: 315px;
    border-radius: 33px;
    background-color: #f7f7f7;
    float: right;
    text-align: center;
    height: 32px;
    line-height: 32px;
  }

  .search {
    border: none;
    background-color: #f7f7f7;
    height: 30px;
    width: 248px;
  }

  img {
    width: 30px;
    height: 30px;
  }

  a {
    color: #424e67;
    text-decoration: none;
  }

  a:hover {
    color: #09AAFF;
  }

  /* 特定样式 */
  .el-icon-delete {
    color: #F56C6C;
  }
</style>
