import unittest
import zipfile
import genwgtu


class GenWtguTestCase(unittest.TestCase):
	"""Test for genwgtu.py"""

	def setUp(self):
		pass

	def tearDown(self):
		pass


	def test_generateXml(self):
		expected = \
'''<?xml version="1.0" encoding="utf-8"?>
<wgtu appid="FAPPID">
	<basis version="1.0"/>
</wgtu>
'''
		self.assertEqual(expected, genwgtu.generateXml("FAPPID", "1.0", []))


		expected = \
'''<?xml version="1.0" encoding="utf-8"?>
<wgtu appid="FAPPID">
	<basis version="1.0"/>
	<remove>
		<item path="image/icon5.png"/>
		<item path="cache/"/>
	</remove>
</wgtu>
'''
		self.assertEqual(expected, genwgtu.generateXml("FAPPID", "1.0", ["image/icon5.png", "cache/"]))

	def test_compareWgt(self):
		oldZf = zipfile.ZipFile("test/old.wtg", "r")
		newZf = zipfile.ZipFile("test/new.wtg", "r")

		addList, delList, modList = genwgtu.compareWgt(oldZf, newZf)
		expectedAddList = ['js/new.txt', 'app/auth/logout.html', 'app/about.html', 'new.html']
		expectedDelList = ['image/auth-title.jpg', 'js/comm.js', 'image/icon/img.txt', \
						'app/content/content.html', 'image/icon/winphone/', 'fonts/', 'image/icon/android/']
		expectedModList = ['index.html', 'manifest.json', 'css/mui.css']

		self.assertListEqual(expectedAddList, addList)
		self.assertListEqual(expectedDelList, delList)
		self.assertListEqual(expectedModList, modList)

		oldZf.close()
		newZf.close()


if __name__ == "__main__":
	unittest.main()


