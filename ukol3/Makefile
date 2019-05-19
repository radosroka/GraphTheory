default:
	echo "#!/bin/sh" >> car
	echo "#!/bin/sh" >> server
	echo "#!/bin/sh" >> race
	echo "exec src/car.py" >> car
	echo "exec src/server.py" >> server
	echo "exec src/race.py" >> race

	chmod -R 777 *
pack:
	zip -r xsroka.zip  src/ report.pdf Makefile

clean:
	rm -rf car server race *.zip
