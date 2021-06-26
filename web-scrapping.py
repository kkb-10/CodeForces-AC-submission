from bs4 import BeautifulSoup  
import requests  
import os

########### SCRIPT TO SAVE ALL AC SUBMISSION OF YOUR CF PROFILE #########

# Provide the below details for your codeforces profile

cf_handle=""                   # Your cf handle
no_of_pages=10                 # No of submission pages in your profile
path="D:\code\Code-Library\ "  # Path where you want to save all AC submssion in your local repo
partymemberid="9614927"        # Inspect element any submission id from your profile and get your partymemberid from there
start_page= 1                  # The submission page number from where you want to start scraping the solutions
  
############# NOW THE MAGIC BEGINS - BY Kirti Kunj Bajpai ###############

url="https://codeforces.com/submissions/" + cf_handle + "/page/"

print("Scrapping the AC Solutions of "+cf_handle + "...........", end="\n\n\n")


for i in range (start_page,no_of_pages+1):
    print("Scrapping Page " + str(i) + "......")
    print("***********************************",end="\n\n")
    req_url =url + str(i)

    while(1):
        try:
            html_content = requests.get(req_url).text  
            break
        except requests.exceptions.ConnectionError:
            print("No response from server. Trying to reconnect....",end="\n")
    
    soup = BeautifulSoup(html_content, "html5lib")  


    table=soup.find_all("tr",{"partymemberids":";"+partymemberid+";"})
    for row in table:
        row_container=row.find_all("td")
        submission_id=(row_container[0].text.strip())
        submission_link=(row_container[0].a['href'])
        subm_url="https://codeforces.com"+submission_link
        subm_type=row_container[4].text.strip()[:2]
        
        if(subm_type=="GN"):
            subm_type="cpp"
        elif(subm_type=="Py"):
            subm_type="py"
        elif(subm_type=="Ja"):
            subm_type="java"

        subm_verdict=row_container[5].text.strip()      
        problem_name="cf-"+(row_container[3].text.strip())

        if(subm_verdict=="Accepted"):   # if we get an AC submission 

            while(1):
                try:
                    html_c = requests.get(subm_url)
                    break
                except requests.exceptions.ConnectionError:
                    print("No response from server. Trying to reconnect....",end="\n")
                    
            soup_final = BeautifulSoup(html_c.content, "html5lib")  
            code_line=soup_final.find_all("pre")
            code=code_line[0].text

            # Storing into the local repo

            final_path = path + "problem - " + submission_id  + " - code.txt"
            
            if not os.path.exists(path + "problem - " + submission_id + " - code." + subm_type): # If that file name already exists, then it doesn't add it to repo
                file = open(final_path, "w+") 
                file.write(code)
                file.close()

                # converting the file
                base = os.path.splitext(final_path)[0]
                ext="." + subm_type
                os.rename(final_path, base + ext)

            print(problem_name)
            print("Saving file at: " + path + "problem - " + submission_id + " - code." + subm_type ,end="\n\n")

