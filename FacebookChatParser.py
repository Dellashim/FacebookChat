#!/usr/bin/env

from lxml import etree as ET
from datetime import datetime as dt
import csv

# TODO: support output to other formats, message statistics, etc
class FacebookChatParser(object):
    def __init__(self, filename):
        self.parse_file(filename)
        
    def parse_file(self, filename):
        tree = ET.parse(filename)
        self.data = []
        for element in tree.find("/body/div[@class='thread']"):
            if element.tag == "div" and element.get("class") == "message":
                user = element.find(".//span[@class='user']").text
                # TODO: parse into proper datetime object
                datetime = element.find(".//span[@class='meta']").text
                # TODO: parse in reaction data
                #self.data.append([user, datetime, "", []])
                self.data.append([user, datetime, ""])
            elif element.tag == "p":
                text = element.text
                # TODO: the native csv writer can't handle unicode, so for now we do a string encode, which yields unideal results
                if text is not None:
                    text = text.encode('utf-8')
                self.data[-1][2] = text
            # TODO: parse in reaction data
            # elif element.tag == "ul":
            #     print('here')
            #     for li in element.find("li"):
            #         self.data[-1][3].append(li.text)

    def to_csv(self, outfilename):
        with open(outfilename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for row in self.data:
                writer.writerow(row)

    def get_data(self):
        return self.data

if __name__ == "__main__":
    parser = FacebookChatParser("C:\\Users\\Alex\\Downloads\\151.html")
    parser.to_csv("chat_history.csv")