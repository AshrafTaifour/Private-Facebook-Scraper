from unittest import TestCase, main
import sys
import os
# hacky fix to get parent directory
sys.path.append(os.getcwd() + '/..')

#import our file that has user login and the path to the tor and chrome drivers
from secretDirectory import secret
from post import post
from main import loginToFacebook

class Test(TestCase):
    def test_post(self, pathToTor = secret.linuxPath, email = secret.EMAIL, passw = secret.passw):
        driver = loginToFacebook(pathToTor, email, passw)
        friendUsername="abdullah.arif115"
        message="The best things in life take patience"
        post(driver, friendUsername, message)


if __name__ == '__main__':
    main()