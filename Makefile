CC = gcc
CFLAGS = -Wall -Wextra

hello: hello.c
	$(CC) $(CFLAGS) -o hello hello.c

clean:
	rm -f hello

.PHONY: clean
