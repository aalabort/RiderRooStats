from __future__ import print_function
import httplib2
import os

import GetMessage
import obtainallthreads
from collections import Counter
import pandas

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json because if not the previous ones will keep being used instead of the new ones.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows different stats obtained from the mails sent by Deliveroo for each drop.

    Creates a Gmail API service object and obtain all Threads of the user's mailbox matching the query. After that, scrap the useful data in the mails such as the value of the tip, the name of the restaurant, the delivery Time and then make some statistics with these data.

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    threads = obtainallthreads.ListThreadsMatchingQuery(service, 'me', query='from:(noreply@deliveroo.co.uk) subject:(Order #) after:2016/8/21 before:2016/9/4')

    drops = len(threads)

    tip = []
    restaurant = []
    deliveryTime = []
    i = 0
    for thread in threads:
        messageId = thread['id']
        message = GetMessage.GetMessageBody(service, 'me', str(messageId))
        tipIndex = message.index("Credit Card Tip:")
        tipLine = message[tipIndex:]
        tipRaw = tipLine.split()
        tip.append(float(tipRaw[3]))

        restaurantAddressIndex = message.index("Restaurant Address:")
        restaurantAdressLine = message[restaurantAddressIndex:]
        restaurantIndex = message.index("Restaurant:")
        restaurantLine = message[restaurantIndex:restaurantAddressIndex]
        restaurantRaw = restaurantLine.split()
        restaurantRaw.pop(0)
        restaurantRaw = ' '.join(restaurantRaw)
        restaurant.append(restaurantRaw)

        deliveryTimeIndex = message.index("Delivery Time:")
        deliveryTimeLine = message[deliveryTimeIndex:]
        deliveryTimeRaw = deliveryTimeLine.split()
        deliveryTime.append(deliveryTimeRaw[2] + ' ' + deliveryTimeRaw[3])

        i += 1


    tipsTotal = sum(tip)

    tableRestaurant = pandas.Series(Counter(restaurant))
    index = restaurant
    tableTipsRestaurant = pandas.Series(0., index=tableRestaurant.keys())
    for i in xrange(len(tip)):
        print(restaurant[i])
        print(tip[i])
        tableTipsRestaurant.ix[restaurant[i]] += tip[i]
    print("\nTips per restaurant:\n%s " %tableTipsRestaurant.sort_values())

    #print(tableRestaurant.sort_values())
    #print(tableTipsRestaurant.values)
    #print(tableRestaurant.values)
    AvgTableTipsRestaurant = pandas.Series(tableTipsRestaurant.values/tableRestaurant.values, index=tableRestaurant.keys())
    print("\nAverage Tips per restaurant:\n%s " % AvgTableTipsRestaurant.sort_values())

    print("\ndrops: %s " % drops)
    print("\nOrder Comission: %s " % (int(drops)*4.0))
    #print(tip)
    print("\nTotal Tips: %s " % tipsTotal)

if __name__ == '__main__':
    main()
