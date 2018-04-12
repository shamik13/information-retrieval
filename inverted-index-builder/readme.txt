
                                                            ASSIGNMENT 2 README
                                                           ---------------------


OS: Ubuntu 16.04
______________________________________________________
______________________________________________________

Following packages are needed to run the program:

1. BeautifulSoup
   Terminal command: sudo pip install bs4

2. Matplotlib
   Terminal command: sudo pip install matplotlib

3. NLTK
   Terminal command: sudo pip install nltk

4. Numpy
   Terminal command: sudo pip install numpy

* In case pip is not already installed in the system, run this command to install pip first:

  sudo easy_install pip.

* All the thousands text files generated in the previous assignment are saved under crawlDir directory. 
_______________________________________________________
_______________________________________________________

To execute the program:
Terminal command: python indexer.py
_______________________________________________________
_______________________________________________________

Output:

Section 1:

4 files I1, I2, I3 and I4 will be generated in the same directory containing inverted indexes created in Step 1, Step 2, Step 3 and Step 4 respectively. Also in terminal, following 5 stats will be printed for each inverted index:
1. Number of Terms
2. Maximum Length of Postings List
3. Minimum Length of Postings List
4. Average Length of Postings List
5. Size of the file that stores the inverted index


Section 2:

Most frequent, median and least frequent K words, Postings List size for each of the K words and For each of these words, average gap between documents in the Postings List are printed in terminal. The value of K can be changed by changing the variable K inside source code.

Section 3:

A png file containing the graph for log of the rank of the term vs log of collection frequency of the term  will be generated in the same directory.

Section 4:

A png file containing the graph for log of the number of tokens already seen vs log of the vocabulary size will be generated in the same directory.





