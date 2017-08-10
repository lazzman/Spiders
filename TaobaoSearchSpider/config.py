MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'products'

# 设置PhantomJS的参数，1.禁止加载所有内联图像 2.忽略SSL错误，例如过期或自签名证书错误 3. WebDriver记录级别
PHANTOM_ARGS = ['--load-images=false', '--ignore-ssl-errors=true','--webdriver-loglevel=ERROR']
# 更多命令参数请看http://phantomjs.org/api/command-line.html