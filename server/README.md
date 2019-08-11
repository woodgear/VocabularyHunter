# VocabularyHunter
find the word you unknow
# how to audio
http://ssl.gstatic.com/dictionary/static/sounds/oxford/english--_gb_1.mp3
https://www.zhihu.com/question/65581548
# dict
https://github.com/skywind3000/ECDICT
因为数据文件太大所有把ecdict的所有数据文件给ignore掉了 需要自己下载 还要自己生成一个stardict.sqlite放在ECDICT文件夹下

# TODO
- [x] dict 类 通过ECDICT获取给定单词定义 描述单词定义类型 初始化默认值
- [] 重构 解析类 根据词典(词干信息 单词变形信息) 重新生成生词
- [] 调研语音api 获取单词发音(url)
- [] 自定义 信息 收藏文章 (elasticsearch?)
- [] 同义词 wordnet信息接口
- [] 短语解析  重构 解析类 根据词典(短语信息) 重新生成生词
- [] 词根词缀 爬虫(ecdict中好像有)
- [] 信息补全 字幕信息 剧本信息 补全 爬虫 (预制数据库)
- [] 信息补全 支持豆瓣信息导入
- [] 生词 anki web 同步
- [] 爬虫下载给定单词音频 (在常用单词表上的单词 先爬下来)
- [] 音频接口

# 重构
- dbmodel 是否单例?