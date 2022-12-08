# Assignment 3: Universities Ranking by Sajeiv Ravichandran

# This is the function that will collect information on a country and write information into the output.txt file
# The three parameters would include the country selected by the user and the two files csv that contain needed info
def getInformation(selectedCountry,rankingFileName,capitalsFileName):
    # Variables needed for later steps were declared at the top
    selectedCountry = selectedCountry.title().strip()
    # USA was hardcoded to work for selected country because all the letters have to be capitalized not title formatted
    if selectedCountry == "Usa":
        selectedCountry = "USA"
    outputText = open("output.txt", "w", encoding="utf8")
    universityCount = 0
    capitalCount = 0
    availableCountries = []
    availableContinents = []

    # Two try-excepts were written to see if any of the needed files were not found, in which case an error message is written on the output file and program is ended
    try:
        open(rankingFileName, "r", encoding="utf8")
    except FileNotFoundError:
        outputText.write("file not found")
        quit()

    try:
        open(capitalsFileName, "r", encoding="utf8")
    except FileNotFoundError:
        outputText.write("file not found")
        quit()

    # University Count
    # The ranking file is opened and strip is used to remove any empty spaces or columns that are not used
    # Non empty spaces in the topUni file will be counted as it represents the amount of universities available in the csv
    with open(rankingFileName, "r", encoding="utf8") as topUni:
        for uniCount in topUni:
            if uniCount.strip():
                universityCount += 1
    # The university count is updated to the number of lines that contain contents in topUni.csv file
    # This can also represent the amount of universities there are in the file minus the first row of categories in the csv file
    universityCount -= 1
    # After university count was determined, the function will write about this on the output.txt file
    outputText.write("Total number of universities => " + str(universityCount) + "\n")

    # Available Countries
    # A while loop is used to loop through the amount of lines in the topUni csv(same as university count + 1)
    # The loop will read each line in this csv, split it by the comma and then append the 3rd index (country) onto a list
    with open(rankingFileName, "r", encoding="utf8") as topUni:
        i = 0
        while i < universityCount+1:
            lineContent = topUni.readline().split(",")
            if lineContent[2].upper() not in availableCountries:
                availableCountries.append(lineContent[2].upper())
            i += 1
        # The first element of this list is popped because it is a header that is not needed for the country list
        availableCountries.pop(0)

    # The determined available countries are written onto the output.txt file
        outputText.write("Available countries => ")
        for countries in availableCountries:
            outputText.write(countries + ", ")
        outputText.write("\n")

    # Available Continents
    # The amount of non-blank lines of the capitals.csv was determined with for loop and strip
    with open(capitalsFileName, "r", encoding="utf8") as capitals:
        for capCount in capitals:
            if capCount.strip():
                capitalCount += 1
    with open(capitalsFileName, "r", encoding="utf8") as capitals:
        i = 0
        # A dictionary is made to hold the country as a key and then the continent for each country
        countryDict = {}
        # This continent list will be needed for the output file and further steps
        continentList = []
        # While i is less than the number of non-empty lines in capitals.csv, each line will be split by the comma and the country(index) will be used as a key holding its respective continent
        while i < capitalCount:
            capitalsLineContent = capitals.readline().strip().split(",")
            if capitalsLineContent[0].upper() not in countryDict:
                countryDict[capitalsLineContent[0].upper()] = capitalsLineContent[5].upper()
            i += 1
        # Country Name is popped because it is a header
        countryDict.pop("COUNTRY NAME")

        # a for loop is used to loop through the country list and see if their respective continent is in the continent list or not
        # If the continent is already in the list, it won't be added. This is a good way to get the corresponding order needed for the output
        for country in availableCountries:
            if country.upper() == "USA":
                if "NORTH AMERICA" not in continentList:
                    continentList.append("NORTH AMERICA")
            else:
                if countryDict[country.upper()] not in continentList:
                    continentList.append(countryDict[country.upper()])

    # The available continent list is then looped through and written onto the output file
    outputText.write("Available continents => ")
    for continents in continentList:
        outputText.write(continents + ", ")
    outputText.write("\n")


    # Top International Rank & National Rank
    # A nested dictionaries was created to help answer and determine the info needed for the future parts of the assignment
    # This nested dictionary will have the following order : Country - University Name - (International Rank, National Rank, University Score)
    with open(rankingFileName, "r", encoding="utf8") as topUni:
        i = 0
        uniRankDict = {}
        while i < universityCount + 1:
            # each line in the TopUni file is split to and then indexed accordingly to make the planned dictionary
            lineContent = topUni.readline().strip().split(",")
        # lineContent[2] is the country which contains another dictionary of lineContent[1] which is university name which then contains the two ranks and scores according to the corresponding lineContent[] index
        # if the country is not listed in the dictionary it will make a new key for it
            if lineContent[2] not in uniRankDict:
                uniRankDict[lineContent[2]] = {lineContent[1]: {"iRank": lineContent[0], "nRank": lineContent[3], "uniScore": lineContent[8]}}
        # if the country is listed in the dictionary, it will continue to add all the country's universities to it during the loop
            else:
                uniRankDict[lineContent[2]][lineContent[1]] = {"iRank": lineContent[0], "nRank": lineContent[3], "uniScore": lineContent[8]}
            i += 1
        # The Country header is popped
        uniRankDict.pop("Country")

        # Start of finding the best school in the selected country with iRank or internation rank
        # Current Rank variable is a list where the first element will hold the university name for top international uni from the country and then the second element being the international rank
        # A for loop is used to run through the uniRank dictionary made for the selected country and the iRank is compared to the current rank[1] which is initially set to 999 so there would be no interference with starting values
        # If the Irank is less than the second element of current rank, it will replace the number as a "better" international rank
        currentRank = ['', 999]
        selectedCountry = selectedCountry.title()
        if selectedCountry == "Usa":
            selectedCountry = "USA"
        for universityIter in uniRankDict[selectedCountry]:
            if int(uniRankDict[selectedCountry][universityIter]["iRank"]) < currentRank[1]:
                currentRank = [universityIter, int(uniRankDict[selectedCountry][universityIter]["iRank"])]

        # These two values held in the variables will be used in the output.txt file
        selectedIRank = currentRank[1]
        selectedIUni = currentRank[0]

        # Start of finding the best school in the selected country with nRank or national rank
        # For national rank the same dictionary and loop will be used but instead of comparing iRank, it will be nRank this time
        currentRank = ['', 999]
        for universityIter in uniRankDict[selectedCountry]:
            if int(uniRankDict[selectedCountry][universityIter]["nRank"]) < currentRank[1]:
                currentRank = [universityIter, int(uniRankDict[selectedCountry][universityIter]["nRank"])]

        # Best national rank and corresponding university will be reported to the output.txt file
        selectedNRank = currentRank[1]
        selectedNUni = currentRank[0]

    # Both highest international rank and the name of the university is reported for the selected country
    outputText.write("At international rank => " + str(selectedIRank) + " the university name is => " + str(selectedIUni) + "\n")
    # Both highest national rank and the name of the university is reported for the selected country
    outputText.write("At national rank => " + str(selectedNRank) + " the university name is => " + str(selectedNUni) + "\n")

    # Average Score
    # A for loop is used to go through the uniRank dictionary to collect the score of each university from the selected country which is then added to the universitySum variable. A university number loop counter is used
    universitySum = 0
    universityNumber = 0
    with open(rankingFileName, "r", encoding="utf8") as topUni:
        for universityIter in uniRankDict[selectedCountry]:
            universitySum += float(uniRankDict[selectedCountry][universityIter]["uniScore"])
            universityNumber += 1
    # Average score would be the university score sum divided by the number of universities rounded to two decimal places
    averageScore = round(universitySum/universityNumber, 2)
    # This average score is then written onto the output.txt file
    outputText.write("The average score => " + str(averageScore) + "\n")

    # Relative Score
    # This variable will hold the name of the continent that is in relation to the selected country
    continentRelative = ""
    # This variable will hold the max university score within the continent where the selected country resides in
    continentMaxValue = 0

    # if the selected country is an existing key within the first country dictionary, it will set the continent where the country resides in
    if selectedCountry.upper() in countryDict.keys():
        continentRelative = countryDict[selectedCountry.upper()]
    # using a for loop if the continent value in the first dictionary matches to the set continent, it will loop through all the universities in that country and compare the uniScore to the max continent value
    for country in uniRankDict.keys():
        if countryDict[country.upper()] == continentRelative:
            for university in uniRankDict[country]:
                score = uniRankDict[country][university]["uniScore"]
                if float(score) > continentMaxValue:
                    continentMaxValue = float(score)

    # Relative score is the average score determined in the previous part divided by the max continent value times 100. This answer is then rounded to 2 decimal places
    relativeScore = round((averageScore/continentMaxValue)*100, 2)
    # Relative score is written onto the output.txt file
    outputText.write("The relative score to the top university in " + continentRelative + " is => " + str(averageScore) + "/" + str(continentMaxValue) + " x 100% = " + str(relativeScore) + "%" + "\n")

    # Selected Country Capital
    # Similar to the first dictionary made called countryDict, the same method is used to create a capital dict which has the country key and then the capital name
    with open(capitalsFileName, "r", encoding="utf8") as capitals:
        i = 0
        capitalDict = {}
        while i < capitalCount:
            capitalsLineContent = capitals.readline().strip().split(",")
            if capitalsLineContent[0].upper() not in capitalDict:
                capitalDict[capitalsLineContent[0].upper()] = capitalsLineContent[1].upper()
            i += 1
        # Once the capital dictionary is made, a quick search by index can be used to set the selected capital value in respects to the selected country
        selectedCapital = capitalDict[selectedCountry.upper()]

    outputText.write("The capital is => " + selectedCapital + "\n")

    # Universities holding the capital name
    # A loop is used to go through the uniRank dictionary at the university name level and see if the name contains the capital name, if it does it is added to a list
    capitalUniversities = []
    if selectedCountry.title() == "Usa":
        for universities in uniRankDict["USA"]:
            if selectedCapital.lower() in universities.lower():
                capitalUniversities.append(universities.upper())
    else:
        for universities in uniRankDict[selectedCountry.title()]:
            if selectedCapital.lower() in universities.lower():
                capitalUniversities.append(universities.upper())

    # The univeristy names with capital cities are contained within a list which is used to write this information onto the output.txt file
    outputText.write("The universities that contain the capital name =>")

    i = 1
    for universities in capitalUniversities:
        outputText.write("\n" + "     #" + str(i) + " " + universities)
        i += 1
    outputText.close()
