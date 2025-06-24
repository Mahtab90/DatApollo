
# ./preprocessing.py 0.5 1 8
min_support=${1:-0.5}
min_confidence=${2:-1}
max_length=${3:-8}

./preprocessing.py $min_support $min_confidence $max_length

./deploy.sh
