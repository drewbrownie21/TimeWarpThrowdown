import requests
from bs4 import BeautifulSoup

def scrape_team_record(team : str, year: int):
    # Check that year is in int
    if not isinstance(year, int):
        raise TypeError("Year must be an integer.")
    
    # Construct the URL for the team's stats page on Baseball Reference
    url = f"https://www.baseball-reference.com/teams/{team}/{year}.shtml"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    response.raise_for_status()

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element with "Record:"
    record_element = soup.find('strong', string='Record:')

    # Check if the element is found before accessing its sibling
    if record_element and record_element.next_sibling:
        # Extract the text from the next sibling element
        record_text = record_element.next_sibling.get_text(strip=True)
        record = record_text.split(',')[0]

        # Extract the team record (assuming the format is "W-L-T" or "W-L")
        wins, losses, ties = map(int, record.split('-'))

        team_record_dict = {
            "Team"   : team,
            "Year"   : year, 
            "Wins"   : wins,
            "Losses" : losses,
            "Ties"   : ties,
        }

        return team_record_dict
    
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def compare_teams(team_one : dict, team_two: dict):
    team_one_w_prcnt = round(team_one['Wins'] / (team_one['Wins'] + team_one['Losses'] + team_one['Ties']) *100, 2)
    team_two_w_prcnt = round(team_two['Wins'] / (team_two['Wins'] + team_two['Losses'] + team_two['Ties']) *100, 2)

    if team_one_w_prcnt > team_two_w_prcnt:
        return "Team one!"
    elif team_two_w_prcnt > team_one_w_prcnt:
        return "Team two!"
    else:
        return "Tie...."

if __name__ == "__main__":
    # Team abbreviations can be found on Baseball Reference
    NYY = scrape_team_record('NYY', 1938)
    SFG = scrape_team_record('SFG', 2012)

    results = compare_teams(NYY, SFG)
    print(results)
