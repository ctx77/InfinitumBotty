"""

This module takes a topic as input and queries the PubMed Database for entries. Prints the first three in chat

September 2025, Skadi Wiesemann

"""


import requests

from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class PubmedObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".pubmed"]

    @staticmethod
    def help():
        return ".pubmed <term> - fragt Pub Med zu <term> ab. Achte auf Groß und kleinschreibung und auf Rechtschreibung"

    def update_on_priv_msg(self, data, connection):

        if data['messageCaseSensitive'].find('.pubmed') == -1:
            return

        #split incoming message in '.pubmed' and '<term>'
        message = data['messageCaseSensitive'].split(' ', 1)

        #request ids from Pubmed with <term>
        search = message[1]
        contents = requests.get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={search}')

        #use build in tools to extract content and status code for further processing
        contentStr = str(contents.content)
        status = int(contents.status_code)

        #format content for better readability
        replaced = contentStr.replace('<Id>', '').replace('</Id>\\n', ' ').replace('<IdList>\\n', " ")  #
        split = replaced.split(" ")
        onlyFive = split[10:13]

        if status == 200:
            for indices in onlyFive:
                try:
                    #get content with ids
                    IdContents = requests.get(
                        f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={indices}&version=2.0')
                    IdContentsStr = str(IdContents.content)

                    #format xml to extract Title
                    Title = IdContentsStr.replace('<Title>', '~').replace('</Title>', '~')
                    TitleArr = Title.split('~')
                    indexErrorTestTitle = TitleArr[1]

                    #format xml to extract doi
                    doi = IdContentsStr.replace('<ELocationID>', "~").replace('</ELocationID>', '~')
                    doiArr = doi.split('~')
                    indexErrorTestDoi = doiArr[1]

                    #send back data
                    connection.send_back(TitleArr[1], data)
                    connection.send_back(doiArr[1],data)
                    connection.send_back(f'https://pubmed.ncbi.nlm.nih.gov/{indices}',data)
                    connection.send_back(' ',data)

                #when theres only 1 or 2 results, a index error is raised
                except IndexError:
                    connection.send_back("Fehler, bitte mit anderem Suchbegriff versuchen",data)
                    return

        else:
            connection.send_back("Dafür hab ich keinen Eintrag gefunden")
