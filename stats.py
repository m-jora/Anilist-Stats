import time
import requests

url = 'https://graphql.anilist.co'

QUERY1 = '''
  query ($id: Int, $page: Int, $search: String) {
  Page (page: $page, perPage: 10) {
    users (id: $id, search: $search) {
      name
      id
      statistics {
        anime {
          scores {
            mediaIds
          }
        }
      }
    }
  }
}
'''

QUERY2 = '''
        query ($id: Int, $page: Int, $perPage: Int, $search: String, $type: MediaType) {
          Page (page: $page, perPage: $perPage) {
            media (id: $id, search: $search, type: $type) {
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



def IDGrab(username):
  variables = {
    'search' : username,
    'page' : 1
  }

  response = requests.post(url, json = {'query' : QUERY1, 'variables': variables}).json()
  Ids = response['data']['Page']['users'][0]['statistics']['anime']['scores']

  AllIds = []

  for x in Ids:
    AllIds.extend(x['mediaIds'])

  return AllIds


def ShowInfo(AllIds):
  requestCount = 0
  ShowInfoList = {}

  for ID in AllIds:
    if requestCount == 89:
      time.sleep(65)
      requestCount = 0

    variables = {
      'id' : ID,
      'page' : 1,
      'type' : 'ANIME'
    }

    fail=False
    try:
      response = requests.post(url, json = {'query' : QUERY2, 'variables': variables}).json()
    
    except:
      fail = True

    if not fail:
      Titles = response['data']['Page']['media'][0]['title']['romaji']
      ShowTags = response['data']['Page']['media'][0]['tags']
      Tags=[]

      for x in ShowTags:
        Tags.append(x['name'])

      ShowInfoList[Titles] = Tags
    
    requestCount+=1
  return ShowInfoList


def Count(tag, ShowsList):
  result = []
  num = 0
  for key in ShowsList:
    if tag in ShowsList[key]:
      result.append(key)
      num +=1 

  return result, num

user = input('Input Username: ')
tag = input('Input Tag: ')



AllIds = IDGrab(user)
time.sleep(60)
ShowsList = ShowInfo(AllIds)

result, num = Count(tag, ShowsList)

for x in result:
  print(x)

print(num)
