# moodle-attedance
Python program which automatically submit attendances to moodle.

## Prerequisites
Make sure you have installed all of the following prerequisites on your machine:
* Git - [Download](https://git-scm.com/downloads)
* Python3 - [Download](https://www.python.org/downloads/)

After installing Python install html5lib5, requests and bs4 packages using pip:
```bash
$ pip install requests bs4 html5lib
```
## Downloading Code
There are two ways to download the code:

### Cloning The GitHub Repository
The recommended way to get thecode is to use git to directly clone the moodle-attendance repository:

```bash
$ git clone url
```

This will clone the latest version of the repository to a **moodle-attendance** folder.

### Downloading The Repository Zip File
Another way is to download a zip copy of the repository from the [main branch on GitHub](moodle-attendance.zip).

## Configuring Code
Edit the **login_values.py** file by filling the login details and the domain address like given below:
```python
username = 'user05@gmail.com'

password = 'pass123'

domain = 'moodle.example.com'
```

## Running the program

Run the script using python:

```bash
$ python3 ./moodle-attendance.py
```
