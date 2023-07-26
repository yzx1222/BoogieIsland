<template>
  <div>

    <div class="row">
      <div class="col-xs-offset-2 col-xs-8">
        <div class="page-header"><h1>隐蔽通信系统</h1></div>
      </div>
    </div>

    <div class="row">

      <div class="col-xs-2 col-xs-offset-2">
        <div class="list-group">

					<!-- Vue中借助router-link标签实现路由的切换 -->
          <router-link class="list-group-item" active-class="active" to="/LoginForm">LoginForm</router-link>
          <!-- <router-link class="list-group-item" active-class="active" to="/upload">Upload</router-link>
          <router-link class="list-group-item" active-class="active" to="/download">Download</router-link>
					<router-link class="list-group-item" active-class="active" to="/logout">Logout</router-link>
          <router-link class="list-group-item" active-class="active" to="/posts">posts</router-link> -->
          <router-link class="list-group-item" active-class="active" to="/SignupForm">SignupForm</router-link>

        </div>
      </div>

      <div class="col-xs-6">
        <div class="panel">
          <div class="panel-body">

            <!-- 此处到底展示什么组件，得看用户点击的是哪个导航项 -->
						<!-- 指定组件的呈现位置 -->
            <keep-alive include="Upload">
              <router-view></router-view>
            </keep-alive>
          </div>
        </div>
      </div>

    </div>

  </div>

</template>

<script>
	export default {
		name:'App',
	}
</script>

<style>
.row {
  margin-bottom: 20px; /* 添加底部间距 */
}

.list-group {
  height: 20px;
  background-color: #87CEFA; /* 设置背景颜色 */
  border: 1px solid #ddd; /* 设置边框样式 */
  border-radius: 5px; /* 设置边框圆角 */
  padding: 20px; /* 添加内边距 */
}

.list-group-item {
  
  padding-left: 10px;
  padding-right: 10px;
  font-size: 20px;
}

.list-group-item:hover {
  background-color: #B0C4DE; /* 设置鼠标悬停时的背景颜色 */
}

.list-group-item.active {
  background-color: #337ab7; /* 设置选中项的背景颜色 */
  color: #fff; /* 设置选中项的文本颜色 */
}

.router-link-exact-active{
  text-decoration: none;
}

</style>

