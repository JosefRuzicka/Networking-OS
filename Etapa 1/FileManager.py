import os
import csv
import queue

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

  # Writes a line to a file.
  def csv_write_file(self, file, messageToBeWritten):
    # open the file in the write mode
    with open(file, 'a+', newline='') as fileToBeWrittenOn:

      # split message.
      messageToBeWritten = messageToBeWritten.split(",")

      # create the csv writer
      writer = csv.writer(fileToBeWrittenOn, escapechar=',', quoting=csv.QUOTE_NONE)

      # write a row to the csv file
      writer.writerow([messageToBeWritten[0], messageToBeWritten[1], messageToBeWritten[2], messageToBeWritten[3]])

      # close the file
      fileToBeWrittenOn.close()

  # returns true if a given line (data) exists in a given file
  def csv_find_data(self, file, data):
    with open(file, 'r') as csv_file:
      dataFound = False
      lines = csv_file.readlines()
      for line in lines:
        if line == data + '\n' or line == data:
          dataFound = True
    return dataFound

  # create a list of the lines of a given file.
  def csv_list_lines(self, file) :
    list = []
    with open(file) as csv_file:
      lines = csv_file.readlines()
      for line in lines:
        list.append(line.strip('\n'))
    return list

  # create a list of the lines of a given file.
  def csv_enqueue_lines(self, file) :
    new_queue = queue.Queue()
    with open(file) as csv_file:
      lines = csv_file.readlines()
      for line in lines:
        if (line != '' and line != '\n') :
          new_queue.put(line.strip('\n'))

    return new_queue

  # Create a file of a given name.
  def create_file(self, fileName) :
    file = open(fileName, 'a+')
