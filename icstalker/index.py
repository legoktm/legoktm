#!/usr/bin/python
import cgitb; cgitb.enable()

import sys, os, cgi, 

form="""/
<h2>Login</h2>
<form name="input" action="/cgi-bin/index.py" method="post">

Username: <input type="text" name="username">

<br />
Passcode: <input type="password" name="password">
<br />
<input type="submit" value="login">
</form>
"""



