default:
	echo "#!/bin/sh" >> power
	echo "#!/bin/sh" >> reset
	echo "#!/bin/sh" >> weakness
	echo "#!/bin/sh" >> avltree
	echo "exec src/power.py" >> power
	echo "exec src/reset.py" >> reset
	echo "exec src/weakness.py" >> weakness
	echo "exec src/avltree.py" >> avltree

	chmod -R 777 *
pack:
	zip -r xsroka.zip src/* report.pdf Makefile

clean:
	rm -rf power reset weakness avltree  *.zip

test: clean default
	chmod 755 ./src/tests/run.pl
	./src/tests/run.pl
