# Markov Generator

Usage:
```
python markov.py -t https://my-tenant.beekeeper.io -a MY_BOT_TOKEN -c CONVERSATION_ID -u USER_ID

python markov.py -f my-model-file.json

python markov.py -m my-raw-text-file.txt
```

Currently this requires the beekeeper-sdk package which is only available on Beekeeper internal repository. If you have the Nexus read token, you can install the requirements with:
```
pip install -i https://pypi-group:${NEXUS_TOKEN}@nexus.internal.beekeeper.io/repository/pypi-group/simple -r requirements.txt
```
