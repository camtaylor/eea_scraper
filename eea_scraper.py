import requests
import time
import re
import smtplib
import getpass

if __name__ == "__main__":
  # Time in seconds till next check
  REFRESH_TIME = 10
  # Latest list of companies
  current_companies = []
  # Number of companies currently in EEA plus 1 (EEA is a company)
  with open("current_companies.txt", "r") as f:
    companies_list = f.readlines()
    current_companies = [company.strip() for company in companies_list]
  num_companies = len(companies_list)
  # Contact email to send in event of change.
  email = raw_input("Email:").strip() 
  password = getpass.getpass().strip()
  server = smtplib.SMTP( "smtp.gmail.com", 587 )
  server.starttls()
  server.login( email, password)
  
  # Email string
  email_string = """
  Subject: New EEA companies on website 
 
  New companies added: 
  
  """
  # Infinite scrape 
  while True:
    # Get html from eea site
    try:
      eea_html = requests.get("http://entethalliance.org/").text
    except Exception as e:
      print e
      time.sleep(REFRESH_TIME)
      continue
    # Using logo naming convention to pull companies
    companies_list = list(set([company.replace("-logo.png", "") for company in re.findall("[^/]*-logo.png", eea_html)]))
    # A new company has been added
    if len(companies_list) > num_companies:
      print "New companies added to EEA."
      companies_string =  "\n".join([company for company in companies_list if company not in current_companies])
      num_companies = len(companies_list)
      print companies_string
      server.sendmail(email, email, email_string + companies_string)
      # Update current companies file for later
      with open("current_companies.txt", "w") as f:
        [f.write("{}\n".format(company)) for company in companies_list]
      current_companies = companies_list[:]
    # Wait before checking again 
    time.sleep(REFRESH_TIME) 
    print "-- Checking site --"
    
