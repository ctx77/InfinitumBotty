"""

This module takes an integer sequence spaced by ' ' or ',' as input and queries https//:oeis.org for entries, prints the
first 3 in chat.

September 2025, Skadi Wiesemann

"""

import requests
import re

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class OeisObserver(PrivMsgObserverPrototype):


    @staticmethod
    def cmd():
        return ['.oeis']

    @staticmethod
    def help():
        return '.oeis - Befragt oeis.org nach einer Integersequenz'

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].startswith('.oeis'):

            #get input
            eingabe = data['message'].split(' ', 1)
            # process input
            dings = eingabe[1].replace(' ', '%2C')

            # https request
            contents = requests.get(f'https://oeis.org/search?q={dings}&fmt=json')
            content = str(contents.content)
            status = contents.status_code

            if status == 200:
                # find oeis ids (eg. '"number" : 27'
                ids = re.findall('"number": [0-9]+', content)
                # choose first three
                idsOnlyThree = ids[0:3]
                # cleanup
                ids_clean = [s.replace('"number": ', '') for s in idsOnlyThree]


                # convert numbers in id format from e.g. 27 to A000027
                a_ids = []
                for indices in ids_clean:
                    indices = 'A{:06d}'.format(int(indices))
                    a_ids.append(indices)

                    # get content for each id
                    idContents = requests.get(f'https://oeis.org/{indices}')
                    idContent = str(idContents.content)

                    #clean up of title
                    name = (idContent.replace('<div class=seqname>\\n', '~').replace(
                                             '\\n\\n</div>\\n</div>\\n<div class=scorerefs>',
                                            '~')
                                            .split('~'))

                    name2 = name[1].replace('\\n', '~').split('~')
                    name_final = name2[0].strip(' ')

                    #send back data
                    connection.send_back(indices, data)
                    connection.send_back(name_final, data)
                    connection.send_back(f'https://oeis.org/{indices}', data)

            else:
                connection.send_back(f"Fehler: Statuscode: {status}", data)