echo PYTHON: $(which python)
echo env
## do nothing until you get STOP signal, then kill process
while :; do :; done & kill -STOP $! && wait $!