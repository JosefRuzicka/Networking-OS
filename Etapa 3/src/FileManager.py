import os
import csv

class FileManager:

  def init(self):
	  0
    
  def open_file(file_title, ext):
    file_title = file_title + ext
    if(os.path.exists(file_title)):
     file = open(file_title, "r")
    return file

  def close_file(file):
     file.close()

  def extract_filelines(file):
    lines = file.readlines()
    return lines

  # returns line count of a file.
  def csv_get_lineCount(self, file):
    with open(file) as csv_file:
      line_count = sum(1 for _ in file)
    return line_count

  # returns true if a given line (data) exists in a given file
  def csv_find_data(self, file, data):
    with open(file, 'r') as csv_file:
      line_words = []
      dataFound = False
      lines = csv_file.readlines()
      for line in lines:
        line_words = line.split(',')
        if line_words[0] == data:
          dataFound = True
          break
    return dataFound, line_words

  # create a list of the lines of a given file.
  def csv_list_lines(self, file) :
    list = []
    with open(file) as csv_file:
      lines = csv_file.readlines()
      for line in lines:
        list.append(line.strip('\n'))
    return list

  # Create a file of a given name.
  def create_file(self, fileName) :
    file = open(fileName, 'a+')

  def list_neighbors_lines(self,file,data):
    server_list = []
    client_list = []
    with open(file, 'r') as csv_file:
        lines = csv_file.readlines()
        for line in lines:
            line_words = line.split(',')
            #print(line_words[0])
            #print(line_words[1])
            if line_words[0] == data:
                server_list.append(line.strip('\n'))
            if line_words[1] == data:
                client_list.append(line.strip('\n'))
    return server_list, client_list
