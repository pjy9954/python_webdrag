from distutils.core import setup
import py2exe, sys, os
 
sys.argv.append('py2exe')

includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs',
            'Tkconstants', 'Tkinter']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 
                'tk84.dll', 'w9xpopen.exe']

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
	<trustInfo xmlns="urn:schemas-microsoft-com:asc.v3">
		<security>
			<requestedPrivileges>
				<requestedExcutionLevel level='asInvoker' uiAccess='false' />
			</requestedPrivileges>
		</security>
	</trustInfo>
	<dependency>
		<dependentAssembly>
			<assemblyIdentity
				type='win32'
				name='Microsoft.VC90.CRT'
				version='9.0.21022.8'
				processorArchitecture='*'
				publickeyToken='1fc8b3b9a1e18e3b' />
		</dependentAssembly>
	</dependency>
	<dependency>
		<dependentAssembly>
			<assemblyIdentity
				type="win32"
				name="Microsoft.Windows.Common-Controls"
				version="6.0.0.0"
				processorArchitecture="*"
				publicKeyToken="6595b64144ccf1df"
				language="*" />
	    </dependentAssembly>
	</dependency>
</assembly>
"""

setup(
	options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
    zipfile = None,
    windows = [
        {
            "script": "ImgCrawlr_rev.pyw",
#            "icon_resources": [(1, "yourapplication.ico")],
#            "other_resources": [(24,1,manifest)]
        }
    ]#,
#      data_files=["yourapplication.ico"]
)