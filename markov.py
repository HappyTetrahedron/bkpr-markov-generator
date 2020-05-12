import beekeeper_sdk
import os

from markovchain import Parser
from markovchain.text import MarkovText


def main(options):
    if options.modelfile:
        markov = load_model(options.modelfile)
        username = os.path.splitext(os.path.basename(options.modelfile))[0]

    else:
        if options.messagefile:
            messages = load_messages(options.messagefile)
            username = os.path.splitext(os.path.basename(options.messagefile))[0]
        else:
            sdk = beekeeper_sdk.BeekeeperSDK(options.tenant, options.token)
            user = sdk.profiles.get_profile(options.user)
            username = user.get_name()
            messages = fetch_messages(sdk, options.conversation, user)

        corpus = assemble_corpus(messages)
        markov = compile_model(corpus, username)

    print_samples(markov)


def load_messages(message_file):
    with open(message_file) as file:
        return file.readlines()


def fetch_messages(sdk, conversation, user):
    conversation = sdk.conversations.get_conversation(conversation)

    messages = ["{}\n".format(message.get_text().replace('\n', ' ').replace('\r', ''))
                for message in conversation.retrieve_messages_iterator(reversed_order=True)
                if message.get_user_id() == user.get_id() and message.get_text()]
    with open("{}.txt".format(user.get_name()), 'w') as file:
        file.writelines(messages)
    return messages


def assemble_corpus(messages):
    return messages


def load_model(model_file):
    markov = construct_model()
    return markov.from_file(model_file)


def compile_model(corpus, username):
    markov = construct_model()
    for line in corpus:
        markov.data(line, part=True)
    markov.save("{}.json".format(username))

    return markov


def construct_model():
    return MarkovText(parser=Parser([3]))


def print_samples(markov):
    print()
    print(markov())
    print()
    print(markov())
    print()
    print(markov())


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-a', '--auth-token', dest='token', type='string', help="Auth token")
    parser.add_option('-t', '--tenant', dest='tenant', type='string', help="Tenant URL")
    parser.add_option('-c', '--conversation', dest='conversation', type='string', help="Conversation ID")
    parser.add_option('-u', '--user', dest='user', type='string', help="User ID")
    parser.add_option('-m', '--messagefile', dest='messagefile', type='string', default=None, help="Message file to restore from")
    parser.add_option('-f', '--modelfile', dest='modelfile', type='string', default=None, help="Model file to restore from")
    (opts, args) = parser.parse_args()
    main(opts)

