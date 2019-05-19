default:
	echo "#!/bin/sh" >> information
	echo "#!/bin/sh" >> fusion
	echo "#!/bin/sh" >> chemistry
	echo "exec src/information.py" >> information
	echo "exec src/fusion.py" >> fusion
	echo "exec src/chemistry.py" >> chemistry

	chmod -R 777 *
pack:
	zip -r xsroka.zip src/ report.pdf Makefile

clean:
	rm -rf information fusion chemistry *.zip
