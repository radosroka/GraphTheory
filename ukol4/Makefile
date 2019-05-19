default:
	echo "#!/bin/sh" >> groups
	echo "#!/bin/sh" >> parking
	echo "exec src/groups.py" >> groups
	echo "exec src/parking.py" >> parking

	chmod -R 777 *
pack:
	zip -r xsroka.zip  src/ tests/ report.pdf Makefile

clean:
	rm -rf groups parking *.zip
