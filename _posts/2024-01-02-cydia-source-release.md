---
title: 制作自己的 Cydia 源
tags: cydia ios/re
---

<style>
cr { color: Red }
co { color: Orange }
cg { color: Green }
cb { color: Blue}
</style>


# 0x01 目标

托管自己的 Cydia 源发布到 Github Pages

<!--如何托管Cydia™存储库-->

<br />



# 0x02 具体步骤

## 1. 打包

[Theos](https://theos.dev/docs/) 打 Release 包很简单，一条命令：

```bash
make package FINALPACKAGE=1
```

不过要注意里面 `control` 文件的填写，下面的步骤会用到这个文件的信息。



## 2. 安装测试

安装到越狱手机可以通过下面一些方式：

- 使用 Theos 的命令 `make install`
- 把 deb 包传到手机，用 Filza 安装
- 把 deb 包传到手机，用 dpkg 命令安装



测试没问题后可以继续下面的步骤了



## 3. 创建存储库

接下来就是把你本地多个 deb 包制作成一个仓库，可以让别人查看和安装。具体步骤如下：



### 3.1 [apt-ftparchive](https://manpages.ubuntu.com/manpages/xenial/en/man1/apt-ftparchive.1.html) 生成索引文件

```bash
apt-ftparchive packages ./debfiles/ > ./Packages;
```

命令的意思是把 debfiles 目录下的 deb 包文件的信息全部整合到一个叫做 Packages 的文件中。

要注意的是： `apt-ftparchive` 本来只有 Linux 版本的，后来网上有人共享了 [macOS 的版本](https://github.com/crystall1nedev/signing-apt-repo-faq?tab=readme-ov-file)，所以后面说到的一键脚本也可以在 mac 上面直接运行。

<br>

[dpkg-scanpackages](https://manpages.ubuntu.com/manpages/xenial/en/man1/dpkg-scanpackages.1.html) 这个命令应该也没问题，具体我没有测试。



### 3.2 bzip2 压缩成 Packages.bz2 文件

```bash
bzip2 -c9k ./Packages > ./Packages.bz2;
```

命令的意思是把 Packages 文件压缩变成 Packages.bz2



### 3.3 制作 Release 文件 (Metadata, 可选)

```bash
printf "Origin: codwam's Repo\n ... > Release;
```

命令的意思是输出内容到 Release 文件中，具体可以看 [update.sh](https://github.com/codwam/codwam.github.io/blob/8e76c9fe7780206570d0a36f9784b4517c5747ed/iosre/update.sh#L15)



<co>这文件网上说是可选的，但我建议做。</co>



### 3.4 制作 all.packages 文件 (网页数据文件, 可选)

```bash
ls -t ./debfiles/ | ... > all.packages;
```

命令的意思是输出所有的 deb 包文件信息到到 all.packages 文件中，由首页 `(index.html)` 文件使用，具体可以看 [update.sh](https://github.com/codwam/codwam.github.io/blob/8e76c9fe7780206570d0a36f9784b4517c5747ed/iosre/update.sh#L30)



<!-- 
<p style="color:orange">这文件是用来网页显示的，可以不做。</p>
-->
<co>这文件是用来网页显示提取的数据，可以不做。</co>



### 3.6 其他一些文件

其他的文件，比如：**gpg** ... ，都是可选的，这里就不再说明了。



## 4. 发布到 Github Pages
这个基本上属于 Github Pages 的专属内容了，可以看看 [GitHub Pages 搭建教程
]( https://sspai.com/post/54608)  或者网上其他的教程。

制作好了之后就可以打开自己的仓库看看了，比如我的：https://codwam.github.io/iosre/
我用一个子目录来制作的，首页用来做博客。

可以添加的 Cydia 里面看看，是否有自己的 deb 包。如果有那就成功了。

<br>

# 0x04 一键脚本

### 4.1 脚本

[脚本](https://github.com/codwam/codwam.github.io/blob/master/iosre/update.sh) 在可以一键生成 Cydia 仓库所需要的文件，另外还生成了仓库介绍的网页需要的数据，可以直接打开[链接](https://codwam.github.io/iosre/)看看。

在 mac 和 Linux 上面测试都没有问题，Windows 不支持。使用方法：

```bash
# clone 仓库
git clone git@github.com:codwam/codwam.github.io.git
# 然后执行脚本
cd codwam.github.io.git/iosre
chmod +x ./update.sh
./update.sh
```



### 4.2 脚本不能帮你做的

在执行脚本之前，需要做下面一些事情：

1. 把 *.deb 包文件放到 debfiles 目录里面
2. packageInfo 目录下面要对应有相关 bundleID 的文件描述，这里是用来显示详情的，iosre 网页上和 Cydia 的详情也是在这里取数据。每个 deb 包文件都必须包含 [数据链接](https://github.com/codwam/codwam.github.io/blob/master/iosre/packageInfo/com.codwam.surgetweak)，相关的网页显示 [网页链接](https://codwam.github.io/iosre/description.html?id=com.codwam.surgetweak)。<co>（这个跟脚本无关的了，但是要记得更新，不然详情显示不出来）</co>



### 4.3 最终的文件目录结构

<details>
	<summary>执行 tree 命令</summary>

  ```bash
  ~/Development/GitHub/codwam.github.io/iosre git:(master) ±4 >> tree
  .
  ├── CydiaIcon.png 
  ├── Packages 
  ├── Packages.bz2 
  ├── README.md 
  ├── Release 
  ├── all.packages 
  ├── apt-ftparchive 
  ├── debfiles 
  │   ├── com.codwam.surgetweak_0.1_iphoneos-arm.deb
  │   └── com.codwam.surgetweak_0.2_iphoneos-arm.deb
  ├── debimages 
  │   ├── surge-5.5.3-cracked.PNG
  │   └── surge-5.5.3-hijacking.PNG
  ├── description.html 
  ├── donate 
  │   ├── css
  │   │   ├── asProgress.min.css
  │   │   └── normalize.css
  │   ├── index_.html
  │   ├── index_progress.html
  │   ├── js
  │   │   └── jquery-asProgress.min.js
  │   └── progress.now
  ├── files 
  │   ├── Addons (Flipswitch).png
  │   ├── Addons.png
  │   ├── DarkMode-Dark.png
  │   ├── DarkMode-Light.png
  │   ├── Development.png
  │   ├── Multimedia.png
  │   ├── Networking.png
  │   ├── Themes.png
  │   ├── Tweaks.png
  │   ├── Utilities.png
  │   ├── alipay.png
  │   ├── back.png
  │   ├── btc.png
  │   ├── cydia7.png
  │   ├── description.js
  │   ├── github.png
  │   ├── ios7.min.css
  │   ├── ios7dark.css
  │   ├── ipawind.png
  │   ├── ltc.png
  │   ├── main.css
  │   ├── package.png
  │   ├── patreon.png
  │   ├── pp.png
  │   ├── reddit.png
  │   ├── saily.png
  │   ├── sileo.png
  │   ├── twitter.png
  │   ├── wechatpay.png
  │   └── zebra.png
  ├── index.html 
  ├── packageInfo
  │   └── com.codwam.surgetweak
  ├── update.bat
  └── update.sh

  8 directories, 52 files
  ```
</details>
<!-- typora 还不支持折叠：https://github.com/typora/typora-issues/issues/499 -->

<br>
文件按照使用类型，可以分为以下这些部分：
1. **网页内容**：index.html `(首页)`, description.html `(详情页面)` ...
2. **Cydia App 使用**：CydiaIcon.png `(Cydia App的软件源图标)` ...
3. **脚本自动生成**：Packages, Packages.bz2 ...
4. **软件**：apt-ftparchive
5. **脚本命令**：update.bat `(windows)`, update.sh `(macOS & Linux)`

如果有兴趣，可以 fork 我的仓库 [codwam.github.io](https://github.com/codwam/codwam.github.io)，进去 iosre 的文件夹里面看看。

<br>




# 0x05 FAQ
## 5.1 同时安装多个相同包名的 deb 包
本地安装了调试的 surgetweak.deb 包，然后添加自己的 Cydia 源加进去之后发现没有找到 surgetweak 包。我一直在想是发布的哪个步骤出错了，一直检查都觉得没问题。

直到后面在 Cydia 里面搜索出来后，才发现安装相同包名的就不会重复出现在仓库列表了。<co>（可能已经被其他的仓库占据了） </co>

这个问题困扰了我一天。



## 5.2 [repo.me](https://github.com/uchks/repo.me)

这也是个很不错的模板，可以直接使用



<br />



# 0x04 Thanks
[How to Host a Cydia™ Repository](https://www.saurik.com/id/7)



<br />