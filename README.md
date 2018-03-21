# SAP_Concur Coding Challenge Bookmarks

Language : Python3

### How to test:
1. Clone the repository
2. Install all the modules using following command: 
   ```
   pip3 install requests
   ```
3. Run using command:
   ```
   python3 bookmark.py
   ```

### Brief Summary of the code

- The program is taking inputs from the text files that are present.
- Python reads the text file line by line.
- Created a dictionary of all the links present in the files
- Used requests module to send request.
- Send request until you receive status code as 200.
- Made a new dictionary where key is the original urls and the values corresponds to the redirecting urls.
- In the first sort original links are given preference.
- In the second sort smaller links are given preference.
- In the third sort "https" is given preference over "http".
- Validations are done if the url entered is invalid.

### Sample Input present in the txt files:
safari.txt,chrome.txt, firefox.txt

### Sample Output Screent-Shoot
![alt text](https://github.com/prathmesh-parmar/SAP_concur/blob/master/output.png)

