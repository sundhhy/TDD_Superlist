from selenium import webdriver
import unittest

#下面两种写法都可以
#chromedriver = "F:\TDD_with_python_WEB\\tools\chromedriver"
chromedriver = '../../../../tools/chromedriver'

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(chromedriver)
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #伊迪丝听说有一个很酷的在线代办事项应用
        #她去看了这个应用的首页
        self.browser.get('http://localhost:8000')

        #她注意到网页的标题和头部都包含"To-Do"这个词
        print(self.browser.title)
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish teh test!')

        #应用要求她输入一个代办事项

        #她在一个文本框中输入了"Buy peacock feathers"(购买孔雀羽毛
        #伊迪丝的爱好是使用假蝇做饵钓鱼

        #她按回车键后，页面更新了
        #代办实现表格显示了“1： Buys peacock feathers"

        #页面中又显示了一个文本框，可以输入其他的代办事项
        #她输入了“Use peacock feathers to make a fly”

        #伊迪丝做事很有条理

        #页面再次更新，他的清单中显示了两个代办事项

        #伊迪丝想知道这个网站是否会记住她的清单

        #她看到网站为她生成了唯一的URL
        #而且页面中有一些文字解说这个功能

        #她访问那个URL，发现她的代办实现列表还在

        #她很满意，去睡觉了




if __name__ == '__main__':
    unittest.main(warnings='ignore')





