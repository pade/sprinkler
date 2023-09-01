import os
import tempfile
import unittest
from importlib import reload
from pathlib import PurePath


class TestConfig(unittest.TestCase):
    
    def test_01_new_config(self):
        """ Create new config file """
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['SPRINKLER_CONFIG_DIR'] = tmpdir
            import services.config
            reload(services.config)
            debug = services.config.config.getboolean('main', 'debug')
            self.assertEqual(debug, False)
            
    def test_02_existing_config(self):
        """ Existing config file """
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = PurePath(tmpdir, 'sprinkler.ini')
            with open(filename.as_posix(), 'w') as fd:
                fd.writelines(['[main]\n', 'foo = bar\n'])
            os.environ['SPRINKLER_CONFIG_DIR'] = tmpdir
            import services.config
            reload(services.config)
            foo = services.config.config.get('main', 'foo', fallback='Not found')
            self.assertEqual(foo, 'bar')
            
            
if __name__ == '__main__':
    unittest.main()

        
