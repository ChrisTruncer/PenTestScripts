#!/usr/bin/env python3

#remove comments from PowerShell scripts
currently_code = True

with open('/root/Downloads/powersql.ps1', 'r') as readtest:
	psup_contents = readtest.readlines()

with open('/root/Downloads/stripped.ps1', 'w') as removed:
	for line in psup_contents:
		line = line.lstrip()

		if line.startswith("#") and not line.startswith("#>"):
			pass

		elif line.startswith("<#"):
			currently_code = False
		
		elif line.startswith('\n'):
			pass

		elif line.startswith("#>"):
			currently_code = True

		else:
			if currently_code:
				removed.write(line)

