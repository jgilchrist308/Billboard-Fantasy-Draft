'''
This is a very serious program designed to run our very serious Billboard Hot 100 Fantasy League(TM)
'''
from bs4 import BeautifulSoup as soup
import billboard
import requests
import copy

DEBUG = True

def feature_split(weeklypoints, check_features):

    ''' This function splits the features and cobillings into independent entries for easy adding of points. Features are designated if they contain one of 
        the following keywords in the artist listed by Billboard: "Featuring", "With", "&", "_X_", or "AND". Returns a tuple of four dictionaries.

        Args:
            weeklypoints: A dictionary containing the artist and points values from entries that contain no features of any kind

            check_features: A dictionary containing artist and point values from entries that contain features. These point values have not been distributed or weighted yet

        Returns:
            copiedpoints: The new dictionary containing artists and their point totals for the week. This function will have added the points of features to this total, but only for the main artist.

            halfCreditFeatures: A dictionary containing artists and their half-point totals based on true features. These need to be added manually to the total.

            fullCreditFeatures: A dictionary containing artists and their full-point totals based on co-billings. These also need to be manually added.

            tylerCheck: A dictionary containing chart entries that contain a feature keyword AND a comma. This will filter out songs with more than one featured 
                        artist, or Tyler, the Creator and his stupid comma-containing stage name.
    '''
    # Copy weeklypoints for testing
    copiedpoints = copy.deepcopy(weeklypoints)

    # Create empty dictionaries
    halfCreditFeatures = {}
    fullCreditFeatures = {}
    tylercheck = {}

    # Create list of artists with features from the weeklypoints dictionary
    featureKeys = check_features.keys()
    
    for key in featureKeys:
        currfeature = str(key).upper()

        # Tyler Check
        if ", " in currfeature:
            tylercheck[currfeature] = check_features[key]

        # Check half credit features
        elif (" FEATURING " in currfeature):
            splitfeature = currfeature.split(" FEATURING ")
            if splitfeature[0] not in copiedpoints:
                copiedpoints[splitfeature[0]] = (check_features[key])
            else:
                copiedpoints[splitfeature[0]] += (check_features[key])

            # Add to half credit features
            if splitfeature[1] not in halfCreditFeatures:
                halfCreditFeatures[splitfeature[1]] = (check_features[key] // 2)
            else:
                halfCreditFeatures[splitfeature[1]] += (check_features[key] // 2)

        # Check for "WITH"
        elif (" WITH " in currfeature):
            splitfeature = currfeature.split(" WITH ")
            if splitfeature[0] not in copiedpoints:
                copiedpoints[splitfeature[0]] = (check_features[key])
            else:
                copiedpoints[splitfeature[0]] += (check_features[key])

            # Add to half credit features
            if splitfeature[1] not in halfCreditFeatures:
                halfCreditFeatures[splitfeature[1]] = (check_features[key] // 2)
            else:
                halfCreditFeatures[splitfeature[1]] += (check_features[key] // 2)

        # Check full credit features
        else:

            # Check for " X "
            if " X " in currfeature:
                splitfeature = currfeature.split(" X ")
                if splitfeature[0] not in copiedpoints:
                    copiedpoints[splitfeature[0]] = (check_features[key])
                else:
                    copiedpoints[splitfeature[0]] += (check_features[key])

                if splitfeature[1] not in fullCreditFeatures:
                    fullCreditFeatures[splitfeature[1]] = (check_features[key])
                else:
                    fullCreditFeatures[splitfeature[1]] += (check_features[key])

            # Check for " & "
            elif  " & " in currfeature:
                splitfeature = currfeature.split(" & ")
                if splitfeature[0] not in copiedpoints:
                    copiedpoints[splitfeature[0]] = (check_features[key])
                else:
                    copiedpoints[splitfeature[0]] += (check_features[key])

                if splitfeature[1] not in fullCreditFeatures:
                    fullCreditFeatures[splitfeature[1]] = (check_features[key])
                else:
                    fullCreditFeatures[splitfeature[1]] += (check_features[key])

            # Check for "AND"
            elif " AND " in currfeature:
                    splitfeature = currfeature.split(" AND ")
                    if splitfeature[0] not in copiedpoints:
                        copiedpoints[splitfeature[0]] = (check_features[key])
                    else:
                        copiedpoints[splitfeature[0]] += (check_features[key])

                    if splitfeature[1] not in fullCreditFeatures:
                        fullCreditFeatures[splitfeature[1]] = (check_features[key])
                    else:
                        fullCreditFeatures[splitfeature[1]] += (check_features[key])

    # Return 
    return copiedpoints, halfCreditFeatures, fullCreditFeatures, tylercheck

def printdata(chartdata):
    ''' This function prints the data to the terminal for easy reading. if DEBUG is set to True, additional data will be printed.'''
    
    weeklypoints = chartdata[0]
    check_features = chartdata[1]
    newpoints = chartdata[2]
    halfCreditFeatures = chartdata[3]
    fullCreditFeatures = chartdata[4]
    tylercheck = chartdata[5]

    if DEBUG:
        # Print the original dictionary with no features added.
        print(f"\nWeekly Points")
        print(weeklypoints)

        # Print the dictionary of songs with features on them
        print(f"\nFeature check")
        print(check_features)

        # Print the dictionary of points after adding the values obtained from features to the totals of artists with top billing
        print(f"\nWeekly Points with top billing features added to artist total")
        print(newpoints)

    # Print the updated dictionary ordered alphabetically
    print(f"\nSorted Points")
    sortedpoints = dict(sorted(newpoints.items()))
    print(sortedpoints)

    # Print the half credit features dictionary. These are already halved, but have not been added to the weekly points totals
    print(f"\nHalf Credit Features (Already halved)")
    print(halfCreditFeatures)

    # Print the full credit features dictionary. These have not been added to the weekly points totals
    print(f"\nFull Credit Features")
    print(fullCreditFeatures)

    # Print the results of the Tyler Check. None of these artists have had points added to the totals, including top billing
    print(f"\nTyler Check")
    print(tylercheck)


def create_data():
    '''Initializes "chart" - an object generated using the Billboard scraper containing the chart data of the Billboard Hot-100. This data is then processed into points. Number 1 is worth 100, number 2 - 99, etc...
    Different dictionaries are created containing various groups of data and returned

    Args:
        None

    Returns:
        weeklypoints: A dictionary containing the artist and points values from entries that contain no features of any kind

        check_features: A dictionary containing artist and point values from entries that contain features. These point values have not been distributed or weighted yet

        newpoints: A dictionary containing artist and points values with points from top billing features added. None of the featured artists have received credit for their secondary appearances

        halfCreditFeatures: A dictionary containing artists and their half-point totals based on true features. These need to be added manually to the total.

        fullCreditFeatures: A dictionary containing artists and their full-point totals based on co-billings. These also need to be manually added.

        tylerCheck: A dictionary containing chart entries that contain a feature keyword AND a comma. This will filter out songs with more than one featured artist, or Tyler, the Creator and his stupid comma-containing stage name.

    '''

    # Create Chart
    chart = billboard.ChartData('hot-100')

    # Create Dictionary
    weeklypoints = {}
    check_features = {}

    # Loop through chart
    for i in range(len(chart)):
        currsong = chart[i]

        # Convert artist name to uppercase for easier parsing
        currartist = str(currsong.artist).upper()

        # Sort out features
        if ("&" in currartist) or (" WITH " in currartist.upper()) or ("FEATURING " in currartist.upper()) or (" X " in currartist.upper()) or ("AND " in currartist.upper()):
            check_features[currartist] = (100 - i)

        # Add new key if artist not already in the dictionary
        elif currartist not in weeklypoints:
            weeklypoints[currartist] = (100 - i)

        # Add to existing artist
        else:
            weeklypoints[currartist] += (100 - i)
    

    # Run the feature_split() function and assign its returned tuple to "features"
    features = feature_split(weeklypoints, check_features)

    # Assign the dictionary of updated points
    newpoints = features[0]

    # Assign the dictionary of half-credit features
    halfCreditFeatures = features[1]

    # Assign the dictionary of full-credit features
    fullCreditFeatures = features[2]

    # Assign the dictionary of comma flagged entries
    tylercheck = features[3]

    # Return the 6 dictionaries
    return [weeklypoints, check_features, newpoints, halfCreditFeatures, fullCreditFeatures, tylercheck]

def main():

    # Create chart data
    chartdata = create_data()

    # Print the chart data to console
    printdata(chartdata)

main()