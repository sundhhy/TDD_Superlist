from selenium import webdriver
#下面两种写法都可以
chromedriver = '../../../tools/chromedriver'
#chromedriver = "F:\TDD_with_python_WEB\\tools\chromedriver"
browser = webdriver.Chrome(chromedriver)
browser.get('http://localhost:8000')
#browser.get('https://www.baidu.com/index.php?tn=56060048_5_pg&ch=15')
assert 'Django' in browser.title

