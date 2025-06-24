docker rm -f $(docker ps -aq --filter="name=collocate_results") 2>/dev/null 1>/dev/null
docker rm -f $(docker ps -aq --filter="name=itemset_generation") 2>/dev/null 1>/dev/null
docker rm -f $(docker ps -aq --filter="name=rule_generation") 2>/dev/null 1>/dev/null
echo "Previous containers are removed"
cd $(pwd)/deployment/apriori

./gradlew run | tee /dev/tty | stdbuf -o0 -i0 sed -n "/apollo_output/p" | stdbuf -o0 -i0 sed "s/Enactment result\: {\"apollo_output\"\:\"//" | stdbuf -o0 -i0 sed "s/..$//" | stdbuf -o0 -i0 sed "s/'\([^']*\)':/\"\1\":/g" | stdbuf -o0 -i0 sed "s/\([0-9]\):/\"\1\":/g" | stdbuf -o0 -i0 sed "s/',)/\"/g" | stdbuf -o0 -i0 sed "s/('/\"/g" | stdbuf -o0 -i0 sed "s/')/\"/g" | stdbuf -o0 -i0 sed "s/'//g" | stdbuf -o0 -i0 sed "s/}, {/}\", \"{/g" | stdbuf -o0 -i0 sed "s/\[{/[\"{/g" | stdbuf -o0 -i0 sed "s/}]/}\"]/g" > ../../output.json
