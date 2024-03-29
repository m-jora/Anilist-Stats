import time
import requests

url = 'https://graphql.anilist.co'

LISTQUERY = '''
  query ($id: Int, $page: Int) {
    Page (page: $page) {
      pageInfo{
        hasNextPage
      }
      mediaList (userId: $id, type: ANIME, status_not: PLANNING) {
        mediaId
      }
    }
  }
'''


USERQUERY = '''
 query ($id: Int, $page: Int, $search: String) {
  Page (page: $page, perPage: 1) {
    users (id: $id, search: $search) {
      name
      id
    }
  }
}
'''

GENREQUERY = '''
query ($ids: [Int], $page: Int, $search: String, $type: MediaType) {
          Page (page: $page) {
            pageInfo{
              hasNextPage
            }
            media (id_in: $ids, search: $search, type: $type) {
              title {
                  english
                  romaji
              }
              genres
          }
      }
  }

'''



TAGQUERY = '''
        query ($ids: [Int], $page: Int, $search: String, $type: MediaType) {
          Page (page: $page) {
            pageInfo{
              hasNextPage
            }
            media (id_in: $ids, search: $search, type: $type) {
              title {
                  english
                  romaji
              }
              tags {
                name
              }
          }
      }
  }
  '''

def GrabUser(username):
  variables = {
    'search' : username
  }

  response = requests.post(url, json = {'query' : USERQUERY, 'variables': variables}).json()
  userid = response['data']['Page']['users'][0]['id']
  return userid



def ListGrab(UserID):
  nextPage = True
  pageNo = 0
  AllIds = []
  while nextPage:
    pageNo += 1
    variables = {
      'page' : pageNo, 
      'id': UserID
    }

    response = requests.post(url, json = {'query' : LISTQUERY, 'variables': variables}).json()

    nextPage = response['data']['Page']['pageInfo']['hasNextPage']
    Ids = response['data']['Page']['mediaList']
    for x in Ids:
      AllIds.append(x['mediaId'])

  return AllIds


def ShowInfo(AllIds):
  ShowInfoList = {}
  nextPage = True
  pageNo = 0

  while nextPage:
    pageNo += 1
    variables = {
      'ids' : AllIds,
      'page' : pageNo,
      'type' : 'ANIME'
    }

    response = requests.post(url, json = {'query': TAGQUERY, 'variables': variables}).json()
    nextPage = response['data']['Page']['pageInfo']['hasNextPage']
    TitleList = response['data']['Page']['media']#[0]['title']['romaji']

    for x in TitleList:
      Title = x['title']['romaji']
      Tags = x['tags']
      ShowInfoList[Title] = [tag['name'] for tag in Tags]

  return ShowInfoList


def GenreInfo(AllIds):
  ShowInfoList = {}
  nextPage = True
  pageNo = 0

  while nextPage:
    pageNo += 1
    variables = {
      'ids' : AllIds,
      'page' : pageNo,
      'type' : 'ANIME'
    }

    response = requests.post(url, json = {'query': GENREQUERY, 'variables': variables}).json()
    nextPage = response['data']['Page']['pageInfo']['hasNextPage']
    #print(response)
    TitleList = response['data']['Page']['media']#[0]['title']['romaji']

    for x in TitleList:
      Title = x['title']['romaji']
      Genres = x['genres']
      ShowInfoList[Title] = Genres

  return ShowInfoList



def Count(tag, ShowsList):
  result = []
  num = 0
  for key in ShowsList:
    if tag in ShowsList[key]:
      result.append(key)
      num +=1 

  return result, num


def specific_genre():
  user = input('Input Username: ')
  tag = input('Input Genre: ')

  UserID = GrabUser(user)
  AllIds = ListGrab(UserID)
  ShowsList = GenreInfo(AllIds)

  result, num = Count(tag, ShowsList)
  print()
  print('Number of Shows that Match: ', num, '\n')
  print('Shows that match given genre:')
  for x in result:
    print(x)


def specific_tag():
  user = input('Input Username: ')
  tag = input('Input Tag: ')

  UserID = GrabUser(user)
  AllIds = ListGrab(UserID)
  ShowsList = ShowInfo(AllIds)

  result, num = Count(tag, ShowsList)
  print()
  print('Number of Shows that Match: ', num, '\n')
  print('Shows that match given tag:')
  for x in result:
    print(x)



print('Please Select an Option:')
print('1. Manga Stats')
print('2. Anime Stats')
value = int(input('Enter Selection: '))
print()

if value == 1:
  print('Please Select an Option:')
  print('1. Specific Tag Stats')
  print('2. Specific Genre Stats')
  print('3. Top Tags')
  print('4. Top Genres')
  value = int(input('Enter Selection: '))
  print()

  if value == 1:
    pass

  if value == 2:
    pass

  if value == 3:
    pass
  
  if value == 4:
    pass



if value == 2:
  print('Please Select an Option:')
  print('1. Specific Tag Stats')
  print('2. Specific Genere Stats')
  print('3. Top Tags')
  print('4. Top Genres')
  value = int(input('Enter Selection: '))
  print()


  if value == 1:
    specific_tag()

  if value == 2:
    specific_genre()

  if value == 3:
    pass

  if value == 4:
    pass 
